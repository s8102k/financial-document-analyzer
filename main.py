# =====================================
# Imports
# =====================================

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from celery.result import AsyncResult

import os
import uuid
from datetime import datetime

from worker import analyze_document_task
from celery_app import celery_app

from database import engine, SessionLocal
from models import Base, Analysis


# Create tables automatically
Base.metadata.create_all(bind=engine)


# =====================================
# FastAPI App
# =====================================

app = FastAPI(title="Financial Document Analyzer")


# =====================================
# Health Check
# =====================================

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


# =====================================
# Analyze Endpoint (STEP 6)
# =====================================

@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(
        default="Analyze this financial document for investment insights"
    ),
):

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    db = SessionLocal()

    try:
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query:
            query = "Analyze this financial document for investment insights"

        # ---------------------------------
        # Create DB Record (Processing)
        # ---------------------------------
        record = Analysis(
            filename=file.filename,
            query=query,
            status="processing",
            created_at=datetime.utcnow()
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        # ---------------------------------
        # Send task to Celery
        # ---------------------------------
        task = analyze_document_task.delay(
            query.strip(),
            file_path
        )

        return {
            "status": "processing",
            "task_id": task.id,
            "analysis_id": record.id,
            "message": "Analysis started in background",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}",
        )

    finally:
        db.close()


# =====================================
# Result Endpoint (Celery Result)
# =====================================

@app.get("/result/{task_id}")
def get_result(task_id: str):

    result = AsyncResult(task_id, app=celery_app)

    if result.ready():
        return {
            "status": "completed",
            "result": result.result,
        }

    return {
        "status": "processing",
        "task_id": task_id,
    }


# =====================================
# STEP 7 — History API
# =====================================

@app.get("/history")
def get_history():

    db = SessionLocal()

    records = db.query(Analysis).order_by(Analysis.created_at.desc()).all()

    response = [
        {
            "id": r.id,
            "filename": r.filename,
            "query": r.query,
            "status": r.status,
            "created_at": r.created_at,
            "completed_at": r.completed_at,
        }
        for r in records
    ]

    db.close()

    return response


# =====================================
# STEP 8 — Get Single Analysis
# =====================================

@app.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: int):

    db = SessionLocal()

    record = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()

    db.close()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "filename": record.filename,
        "query": record.query,
        "status": record.status,
        "result": record.result,
        "created_at": record.created_at,
        "completed_at": record.completed_at,
    }


# =====================================
# Run Server
# =====================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )