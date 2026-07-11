"""
database.py

Sets up the connection to our SQLite database and provides
a session object that the rest of the app uses to talk to it.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file will be created in the project folder as todo.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """
    Dependency function used by FastAPI routes.
    Opens a database session, gives it to the route,
    then closes it afterward (even if an error happens).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
 
