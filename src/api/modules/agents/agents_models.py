from pydantic import BaseModel, ConfigDict, PrivateAttr
from pydantic.alias_generators import to_camel, to_snake
from typing import List, Any, Optional
from sqlalchemy import Column, Text, ForeignKey
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class InteractionRequest(BaseModel):
    conversationi_id: str

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_snake,
        schema_generator=to_camel
    )


class LLMConfig(BaseModel):
    prompt: str
    tools: List[Any]
    max_tokens: int
    temperature: float

class AgentCreate(BaseModel):
    _user_id: Optional[uuid.UUID] = PrivateAttr()
    agent_name: str
    agent_description: Optional[str]

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        schema_generator=to_camel
    )

class AgentPublic(BaseModel):
    agent_id: str
    user_id: str
    agent_name: str
    agent_description: Optional[str]

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        schema_generator=to_camel
    )

class AgentUpdate(BaseModel):
    agent_name: Optional[str]
    agent_description: Optional[str]

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_snake,
        schema_generator=to_camel
    )


class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(Text, nullable=False)
    agent_description = Column(Text, nullable=True)
