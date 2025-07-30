from pydantic import BaseModel
from typing import List, Any
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class AIConfig(Base):
    __tablename__ = 'ai_config'
    ai_config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    system_prompt = Column(Text, nullable=False)
    max_tokens = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)

    agent = relationship("Agent", back_populates="ai_config", passive_deletes=True)