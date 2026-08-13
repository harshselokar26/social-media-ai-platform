import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class MetaConnection(Base):
    __tablename__ = "meta_connections"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    meta_user_id = Column(
        String,
        nullable=False,
        index=True,
    )

    meta_name = Column(
        String,
        nullable=True,
    )

    access_token = Column(
        String,
        nullable=False,
    )

    token_type = Column(
        String,
        nullable=True,
    )

    expires_in = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )