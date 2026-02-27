# =====================================
# Models - Database Tables
# =====================================

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database import Base


# =====================================
# Analysis Table
# =====================================

class Analysis(Base):
    """
    Stores financial document analysis results.
    """

    __tablename__ = "analysis"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Uploaded file name or path
    filename = Column(String, nullable=False)

    # User query
    query = Column(String, nullable=False)

    # CrewAI output result
    result = Column(Text, nullable=True)

    # processing | completed | failed
    status = Column(String, default="processing")

    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Optional completion time
    completed_at = Column(
        DateTime,
        nullable=True
    )

    def __repr__(self):
        return f"<Analysis id={self.id} status={self.status}>"