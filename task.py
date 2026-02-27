# =====================================
# Importing libraries
# =====================================

from crewai import Task

from agents import financial_analyst, verifier
from tools import FinancialDocumentTool


# =====================================
# Financial Analysis Task
# =====================================

analyze_financial_document = Task(
    description="""
Analyze the financial document located at {path}.

User request:
{query}

Provide:
1. Company financial health
2. Revenue & profit trends
3. Key risk factors
4. Investment recommendation
""",
    expected_output="""
Return structured financial insights.
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
)


# =====================================
# Investment Analysis Task
# =====================================

investment_analysis = Task(
    description="""
Based on financial analysis, provide responsible investment guidance
aligned with company fundamentals and risk exposure.
""",
    expected_output="""
Provide:
- Investment outlook
- Suggested strategy
- Risk level
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],   # ✅ FIXED
)


# =====================================
# Risk Assessment Task
# =====================================

risk_assessment = Task(
    description="""
Evaluate financial risks including liquidity risk,
market risk, operational risk, and debt exposure.
""",
    expected_output="""
Provide structured risk assessment explaining
major financial risks and mitigation strategies.
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],   # ✅ FIXED
)


# =====================================
# Document Verification Task
# =====================================

verification = Task(
    description="""
Verify whether the uploaded file is a valid financial document
before analysis begins.
""",
    expected_output="""
State whether the document is valid and suitable for financial analysis.
""",
    agent=verifier,
    tools=[FinancialDocumentTool()],   # ✅ FIXED
)