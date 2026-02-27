# =====================================
# Imports
# =====================================

import os
from dotenv import load_dotenv

load_dotenv()

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader


# =====================================
# Search Tool
# =====================================

search_tool = SerperDevTool()


# =====================================
# Financial Document Tool
# =====================================

class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = (
        "Reads uploaded financial PDF documents and extracts text content."
    )

    def _run(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                return f"File not found: {path}"

            loader = PyPDFLoader(path)
            docs = loader.load()

            # ✅ LIMIT CONTENT SIZE (CRITICAL FIX)
            MAX_CHARS = 8000   # prevents token overflow

            full_report = ""

            for page in docs:
                content = page.page_content

                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")

                full_report += content + "\n"

                # stop when limit reached
                if len(full_report) > MAX_CHARS:
                    break

            return full_report

        except Exception as e:
            return f"Error reading PDF: {str(e)}"