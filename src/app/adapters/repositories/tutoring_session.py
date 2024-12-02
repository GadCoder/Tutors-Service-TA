from typing import List

from src.app.domain.models.tutoring_session import TutoringSession
from src.app.domain.schemas import tutoring_session as tutoring_session_schema
from src.app.domain.ports.repositories.tutoring_session import TutoringSessionRepositoryInterface


class TutoringSessionDatabaseRepository(TutoringSessionRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, tutoring_session: tutoring_session_schema.TutoringSessionCreate):
        self.session.add(tutoring_session)

    def _get_tutoring_sessions_for_student(self, student_code: str) -> List[tutoring_session_schema.TutoringSessionPublic] | None:
        return self.session.query(TutoringSession).filter(TutoringSession.student_code == student_code).all()

    def _get_tutoring_sessions_for_teacher(self, teacher_code: str) -> List[tutoring_session_schema.TutoringSessionPublic] | None:
        return self.session.query(TutoringSession).filter(TutoringSession.teacher_code == teacher_code).all()