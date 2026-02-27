# =====================================
# Celery Worker
# =====================================

from celery_app import celery_app
from crew_runner import run_crew

from database import SessionLocal
from models import Analysis

from datetime import datetime
import time


# =====================================
# Background Analysis Task
# =====================================

@celery_app.task(bind=True)
def analyze_document_task(self, query: str, file_path: str):
    """
    Background task executed by Celery Worker.
    Saves analysis lifecycle in database.
    """

    print(f"🔥 START ANALYSIS → {file_path}")

    db = SessionLocal()

    # ---------------------------------
    # Create DB Record (Processing)
    # ---------------------------------
    record = Analysis(
        filename=file_path,
        query=query,
        status="processing",
        created_at=datetime.utcnow()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    try:
        # Simulate heavy job (optional)
        time.sleep(5)

        # ---------------------------------
        # Run CrewAI workflow
        # ---------------------------------
        result = run_crew(query, file_path)

        # ---------------------------------
        # Update Success Result
        # ---------------------------------
        record.result = str(result)
        record.status = "completed"
        record.completed_at = datetime.utcnow()

        db.commit()

        print(f"✅ COMPLETED → {file_path}")

        return {
            "analysis_id": record.id,
            "status": "completed",
            "result": str(result)
        }

    except Exception as e:

        # ---------------------------------
        # Update Failure
        # ---------------------------------
        record.status = "failed"
        record.result = str(e)
        record.completed_at = datetime.utcnow()

        db.commit()

        print(f"❌ FAILED → {file_path}")

        raise e

    finally:
        db.close()