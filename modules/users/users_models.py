from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from core.database.db_models import Base 
import uuid

class UserCreate(BaseModel):
    email: str
    password: str
    code: int

class UserResponse(BaseModel):
    userId: uuid.UUID
    email: EmailStr


    class Config:
        orm_mode = True

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)