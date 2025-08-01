from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import List, Any, Optional
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class AiConfigBase(BaseModel):
    agent_id: uuid.UUID
    system_prompt: str
    max_tokens: int
    temperature: float
    api_key: str

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel
    )

class AiConfigPublic(AiConfigBase):
    ai_config_id: uuid.UUID
    api_key: str = Field(exclude=True)

   
class AiConfigUpdate(BaseModel):
    system_prompt: Optional[str]
    max_tokens: Optional[int]
    temperature: Optional[float]
    api_key: Optional[str]

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel
    )


class AIConfig(Base):
    __tablename__ = 'ai_config'
    ai_config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    system_prompt = Column(Text, nullable=False)
    max_tokens = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    api_key = Column(Text, nullable=False)

    agent = relationship("Agent", back_populates="ai_config", passive_deletes=True)