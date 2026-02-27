from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as analyze_task


def run_crew(query: str, file_path: str):
    """
    Shared CrewAI execution logic.
    Used by both API and Celery worker.
    """

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "path": file_path
        }
    )

    return str(result)