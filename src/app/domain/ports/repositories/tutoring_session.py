import abc
from typing import List

from src.app.domain.schemas import tutoring_session as tutoring_session_schema

class TutoringSessionRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, tutoring_session: tutoring_session_schema.TutoringSessionCreate):
        self._add(tutoring_session)
        self.seen.add(hash(tutoring_session.id))

    def get_tutoring_sessions_for_student(self, student_code: str) -> List[tutoring_session_schema.TutoringSessionPublic] | None:
        tutoring_sessions = self._get_tutoring_sessions_for_student(student_code)
        if tutoring_sessions:
            for session in tutoring_sessions:
                self.seen.add(hash(session.id))
        return tutoring_sessions

    def get_tutoring_sessions_for_teacher(self, teacher_code: str) -> List[tutoring_session_schema.TutoringSessionPublic] | None:
        tutoring_sessions = self._get_tutoring_sessions_for_teacher(teacher_code)
        if tutoring_sessions:
            for session in tutoring_sessions:
                self.seen.add(hash(session.id))
        return tutoring_sessions


    @abc.abstractmethod
    def _add(self, tutoring_session: tutoring_session_schema.TutoringSessionCreate):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tutoring_sessions_for_student(self, student_code: str) -> List[tutoring_session_schema.TutoringSessionPublic] | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tutoring_sessions_for_teacher(self, teacher_code: str) -> List[tutoring_session_schema.TutoringSessionPublic] | None:
        raise NotImplementedError

