# Financial Document Analyzer — CrewAI Debug Challenge

AI Internship Assignment Submission  
Built using **CrewAI + FastAPI + Celery + Redis + SQLAlchemy**

---

## Project Overview

The **Financial Document Analyzer** is an AI-powered backend system that analyzes uploaded financial PDF documents and generates structured investment insights.

This project fixes a broken CrewAI repository that contained:

- Deterministic bugs
- Dependency conflicts
- Incorrect tool implementations
- Inefficient / hallucinating prompts
- Blocking API execution
- Non-scalable architecture

The system has been fully debugged, optimized, and upgraded into a **production-ready AI backend service**.

---

## System Architecture

Client  
↓  
FastAPI API  
↓  
Celery Queue (Redis Broker)  
↓  
Background Worker  
↓  
CrewAI Agents  
↓  
LLM Analysis  
↓  
Database Storage  

---

## Features

### Core Features
- Upload financial PDF documents
- Multi-agent financial analysis using CrewAI
- Structured investment recommendations
- Risk assessment analysis
- Task tracking system
- Analysis history API

---

### Bonus Features Implemented

#### Queue Worker Model
- Celery background workers
- Redis message broker
- Concurrent request handling
- Non-blocking API responses

#### Database Integration
- Stores:
  - Uploaded file metadata
  - User query
  - Task status
  - Analysis results
  - Timestamps

---

## Tech Stack

| Component | Technology |
|------------|------------|
| AI Agents | CrewAI |
| Backend | FastAPI |
| Queue System | Celery |
| Message Broker | Redis |
| Database | SQLite + SQLAlchemy |
| LLM Layer | LiteLLM (Groq/OpenAI compatible) |
| PDF Parsing | LangChain PyPDFLoader |

---

## Bugs Found & Fixed

### 1. Broken CrewAI Imports
Updated deprecated imports to new CrewAI API.

### 2. Invalid Tool Implementation
Converted simple functions into proper `BaseTool` classes with `_run()` method.

### 3. Dependency Conflicts
Resolved:
- pydantic conflicts
- click version issues
- onnxruntime mismatches

### 4. Hallucinating / Unsafe Prompts
Rewrote agent prompts to produce:
- Professional financial analysis
- Structured output
- Safe investment recommendations

### 5. Blocking API Execution
Original repo executed AI inside FastAPI directly.

Fixed by:
- Implementing Celery queue worker
- Making analysis asynchronous

### 6. Circular Import Errors
Separated Crew execution logic into `crew_runner.py`.

### 7. File Handling Issues
Added:
- Safe directory creation
- File existence validation
- Cleanup handling

---

## Project Structure

financial-document-analyzer/
│
├── main.py # FastAPI server
├── worker.py # Celery worker
├── celery_app.py # Celery configuration
├── crew_runner.py # CrewAI execution logic
│
├── agents.py # AI agents
├── task.py # CrewAI tasks
├── tools.py # Custom CrewAI tools
│
├── database.py # DB connection
├── models.py # SQLAlchemy models
│
├── data/ # Uploaded PDFs
├── requirements.txt
└── README.md


---

## Installation & Setup

### 1️ Clone Repository

```bash
git clone <your-repo-link>
cd financial-document-analyzer

2️ Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

3️ Install Dependencies

pip install -r requirements.txt

4️ Setup Environment Variables

Create a .env file:

GROQ_API_KEY=your_key

5️ Start Redis
redis-server

6️ Start Celery Worker (Windows Compatible)
celery -A worker worker --pool=solo --loglevel=info

7️ Start FastAPI Server
uvicorn main:app --reload

8️ Open Swagger UI
http://127.0.0.1:8000/docs

API Endpoints
Health Check
GET /
Upload & Analyze
POST /analyze

Response:

{
  "status": "processing",
  "task_id": "...",
  "analysis_id": 11
}
Get Task Result
GET /result/{task_id}
Get Analysis History
GET /history
Get Single Analysis
GET /analysis/{analysis_id}

Concurrency Model

FastAPI handles incoming requests

Celery queues tasks

Redis distributes tasks

Workers process in background

Database stores results

Multiple financial documents can be processed without blocking the API.

🗄 Database Schema
Analysis Table
Field	Description
id	Analysis ID
filename	Uploaded file name
query	User query
status	processing / completed / failed
result	AI output
created_at	Start timestamp
completed_at	Completion timestamp

Testing Concurrency

Upload multiple PDFs quickly:

POST /analyze
POST /analyze
POST /analyze

Celery processes them asynchronously.

Learning Outcomes

Debugging AI systems

CrewAI agent orchestration

Async backend architecture

Queue workers & distributed processing





