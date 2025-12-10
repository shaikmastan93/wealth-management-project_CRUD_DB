# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Base class for all models
Base = declarative_base()

# USER TABLE
class User(Base):
    __tablename__ = "users"  # table name

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
