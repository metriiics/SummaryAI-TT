from dbs.database import Base, session_factory
from dbs.models import SummaryGen

from uuid import uuid4, UUID
from datetime import datetime
import pytz

class Queries:
    @staticmethod
    def create_summary(
        proc_id: int, 
        us_id: int, 
        summary: str | None = None,
        core_info: dict | None = None,
        trace_id: str | None = None
    ) -> SummaryGen:
        with session_factory() as session:
            new_summary = SummaryGen(
                id=uuid4(),
                procedure_id=proc_id,
                user_id=us_id,
                status=False,
                summary=summary,
                core_info=core_info,
                trace_id=trace_id,
                created_at=datetime.now(pytz.timezone('Europe/Moscow'))
            )
            
            session.add(new_summary)
            session.commit()
            session.refresh(new_summary)
            return new_summary.id

    @staticmethod
    def update_summary(
        summary_id: UUID,
        **kwargs
    ) -> SummaryGen:
        with session_factory() as session:
            summary_obj = session.query(SummaryGen).filter(SummaryGen.id == summary_id).first()
            if not summary_obj:
                return None
            
            for key, value in kwargs.items():
                if hasattr(summary_obj, key):
                    setattr(summary_obj, key, value)

            session.commit()
            session.refresh(summary_obj)
            return summary_obj