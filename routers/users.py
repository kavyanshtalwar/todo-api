
"""
routers/users.py
Handles user registration and login routes.
"""
 
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from auth import hash_password, verify_password, create_access_token
 
router = APIRouter(tags=["Authentication"])
 
 
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Checks if username already exists, then hashes the password and saves.
    """
    # Check if username already taken
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
 
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken. Please choose another one."
        )
 
    # Hash the password before saving
    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
 
 
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login with username and password.
    Returns a JWT token that the user sends with every future request.
    """
    # Find the user in database
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
 
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
 
    # Create and return JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": f"Welcome back {user.username}!"
    }
 
