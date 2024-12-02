from typing import Any, Callable

from sqlalchemy.orm import  Session

from src.app.adapters.repositories.tutoring_session import TutoringSessionDatabaseRepository
from src.app.domain.ports.units_of_work.tutoring_session import TutoringSessionUnitOfWorkInterface

class TutoringSessionDatabaseUnitOfWork(TutoringSessionUnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.tutoring_sessions = TutoringSessionDatabaseRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
