from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON, Boolean, UniqueConstraint
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class CardStatus(str, enum.Enum):
    NOT_ACTIVATED = "not_activated"
    ACTIVATED = "activated"
    USED = "used"
    EXPIRED = "expired"

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String(20), unique=True, index=True, nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.NOT_ACTIVATED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    activated_at = Column(DateTime(timezone=True), nullable=True)
    expire_at = Column(DateTime(timezone=True), nullable=False)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String(20), unique=True, index=True, nullable=False)
    result_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    view_count = Column(Integer, default=0)
    last_view_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class InterpretationCache(Base):
    """
    存储不同解读模式的结果缓存
    """
    __tablename__ = "interpretation_caches"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String(20), index=True, nullable=False)
    mode = Column(String(20), index=True, nullable=False)
    result_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("card_id", "mode", name="uq_card_interpretation_mode"),
    )
