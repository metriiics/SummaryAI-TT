from sqlalchemy import Integer, UUID, BIGINT, String, TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime
import uuid 

from dbs.database import Base

class SummaryGen(Base):
    __tablename__ = 'summary_gen'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )
    procedure_id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        TEXT,
        nullable=True
    )
    core_info: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    trace_id: Mapped[str] = mapped_column(
        String(255)
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False
    )