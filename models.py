

"""
models.py
These classes define our database tables using SQLAlchemy's ORM.
Each class = one table. Each attribute = one column.
"""
 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
 
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
 
    # This creates a link so user.tasks gives you all tasks owned by this user
    tasks = relationship("Task", back_populates="owner", cascade="all, delete")
 
 
class Task(Base):
    __tablename__ = "tasks"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
 
    # Foreign key linking this task to a specific user
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
 
