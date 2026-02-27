# =====================================
# Load Environment
# =====================================

from dotenv import load_dotenv
load_dotenv()

# =====================================
# CrewAI Imports
# =====================================

from crewai import Agent, LLM
from tools import FinancialDocumentTool


# =====================================
# LLM Configuration
# =====================================

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.2,
)


# =====================================
# Financial Analyst Agent
# =====================================

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and provide investment insights.",
    backstory=(
        "You are an experienced CFA specializing in financial analysis, "
        "valuation, and investment research."
    ),
    verbose=True,
    memory=True,
    tools=[FinancialDocumentTool()],
    llm=llm,
    allow_delegation=False,
)


# =====================================
# Verifier Agent
# =====================================

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify uploaded document validity.",
    backstory="Expert in financial compliance and reporting validation.",
    verbose=True,
    llm=llm,
    allow_delegation=False,
)