
"""
schemas.py
Pydantic models define the "shape" of data going in and out of the API.
They are NOT the database models — they're used for validation and
serialization. Keeping them separate from models.py is standard practice.
"""
 
from pydantic import BaseModel
from typing import Optional
 
 
# ---------- Task schemas ----------
 
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
 
 
class TaskCreate(TaskBase):
    """Used when a client creates a new task."""
    pass
 
 
class TaskUpdate(BaseModel):
    """Used when a client updates a task. All fields optional."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
 
 
class TaskOut(TaskBase):
    """Used when sending a task back to the client."""
    id: int
    owner_id: int
 
    class Config:
        from_attributes = True  # allows Pydantic to read SQLAlchemy objects directly
 
 
# ---------- User schemas ----------
 
class UserCreate(BaseModel):
    username: str
    password: str
 
 
class UserOut(BaseModel):
    id: int
    username: str
 
    class Config:
        from_attributes = True
 
