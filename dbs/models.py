from sqlalchemy import Integer, UUID, BIGINT, String, TEXT, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime
import uuid 

from dbs.database import Base

class SummaryGen(Base):
    __tablename__ = 'summary_gen'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False
    )
    procedure_id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        TEXT,
        nullable=True
    )
    core_info: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True
    )

    trace_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False
    )