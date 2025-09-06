from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Task schema
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    created_at: datetime
    user_id: str
    
    class Config:
        orm_mode = True