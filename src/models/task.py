from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda:str(uuid.uuid4()))
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=False)  # False: pendiente, True: completada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)