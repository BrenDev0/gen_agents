from pydantic import BaseModel, EmailStr, ConfigDict, PrivateAttr
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from src.api.core.database.db_models import Base 
import uuid


class UserCreate(BaseModel):
    email: EmailStr
    _email_hash: str = PrivateAttr()
    password: str
    code: int
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str

class UserUpdate(BaseModel):
    new_password: str
    old_password: str

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel
    )

class UserPublic(BaseModel):
    user_id: str
    email: EmailStr

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel
    )
    
    
class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    email_hash = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

