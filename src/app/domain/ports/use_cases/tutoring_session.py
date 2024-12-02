import abc
from typing import  Union

from src.app.domain.schemas import tutoring_session as tutoring_session_schema
from src.app.domain.ports.units_of_work.tutoring_session import TutoringSessionUnitOfWorkInterface
from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess


class TutoringSessionServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: TutoringSessionUnitOfWorkInterface):
        self.uow = uow

    async def create(self, tutoring_session: tutoring_session_schema.TutoringSessionCreate) -> ResponseSuccess | ResponseFailure:
        return await self._create(tutoring_session)


    def get_tutoring_sessions_for_student(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_tutoring_sessions_for_student(student_code)

    def get_tutoring_sessions_for_teacher(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_tutoring_sessions_for_teacher(teacher_code)

    @abc.abstractmethod
    async def _create(
            self, session: tutoring_session_schema.TutoringSessionCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tutoring_sessions_for_student(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tutoring_sessions_for_teacher(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
