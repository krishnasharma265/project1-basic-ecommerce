from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.logging import logger
from app.data.connection import get_write_db,get_read_db
from app.models.user import User
from app.schema.user import UserCreate, UserLogin
from app.services.auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_write_db)):
    existing = db.query(User).filter(User.username == user.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_read_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.username})
    logger.info(f"User logged in: {user.username}")
    return {"access_token": token}