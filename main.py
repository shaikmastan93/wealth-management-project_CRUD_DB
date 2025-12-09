# main.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, User

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------------------
# DATABASE DEPENDENCY
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# PYDANTIC SCHEMA
# ---------------------------
class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str


# ---------------------------
# TEST ROUTE
# ---------------------------
@app.get("/hello")
def hello():
    return {"message": "FastAPI + DB connected!"}

@app.get("/welcome")
def welcome():
    return {"message": "API is working."}

# ---------------------------
# CREATE USER (C)
# ---------------------------
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------------------------
# GET ALL USERS (R)
# ---------------------------
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ---------------------------
# GET SINGLE USER BY ID (R)
# ---------------------------
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------------------
# UPDATE USER BY ID (U)
# ---------------------------
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_data.name
    user.email = updated_data.email

    db.commit()
    db.refresh(user)

    return user


# ---------------------------
# DELETE USER BY ID (D)
# ---------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
