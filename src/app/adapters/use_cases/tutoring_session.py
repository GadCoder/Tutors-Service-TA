from typing import  Union

from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

from src.app.domain.models.tutoring_session import TutoringSession
from src.app.domain.schemas import  tutoring_session as tutoring_session_schema
from src.app.domain.ports.use_cases.tutoring_session import TutoringSessionServiceInterface
from src.app.domain.ports.units_of_work.tutoring_session import TutoringSessionUnitOfWorkInterface
from src.app.adapters.use_cases import utils

def _handle_response_failure(
        student_code_: str = None, teacher_code: str = None, message: dict[str, str] = None
) -> ResponseFailure:
    if message:
        return ResponseFailure(ResponseTypes.RESOURCE_ERROR, message=message)

    if teacher_code and student_code_:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"Student with code code {student_code_} and Teacher with code {teacher_code} not found"}
        )
    if student_code_:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"Student with code code {student_code_} not found"}
        )
    if teacher_code:
        return ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"Teacher with code code {teacher_code} not found"}
        )
    return ResponseFailure(
        ResponseTypes.RESOURCE_ERROR,
        message={"detail": f"ERROR"}
    )


class TutoringSessionService(TutoringSessionServiceInterface):
    def __init__(self, uow: TutoringSessionUnitOfWorkInterface):
        self.uow = uow

    async def _create(self, tutoring_session: tutoring_session_schema.TutoringSessionCreate) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                print(f"ON CREATE: {tutoring_session}")
                student_exist = utils.student_exists(student_code=tutoring_session.student_code)
                teacher_exist = utils.teacher_exists(teacher_code=tutoring_session.teacher_code)
                if not student_exist and not teacher_exist:
                    return _handle_response_failure(student_code_=tutoring_session.student_code, teacher_code=tutoring_session.teacher_code)
                if not student_exist:
                    return _handle_response_failure(student_code_=tutoring_session.student_code)
                if not teacher_exist:
                    return _handle_response_failure(teacher_code=tutoring_session.teacher_code)
                new_tutoring_session = TutoringSession(
                    student_code=tutoring_session.student_code,
                    teacher=tutoring_session.teacher_code,
                    start_date=tutoring_session.start_date,
                    end_date=tutoring_session.end_date,
                    )
                self.uow.tutoring_sessions.add(new_tutoring_session)
                self.uow.commit()
                return ResponseSuccess(
                    tutoring_session_schema.TutoringSessionPublic(
                        id=new_tutoring_session.id,
                        student_code=new_tutoring_session.student.student_code,
                        teacher_code=new_tutoring_session.teacher.teacher_code,
                        start_date=new_tutoring_session.start_date,
                        end_date=new_tutoring_session.end_date,
                        is_active=new_tutoring_session.is_active
                    )
                )
        except Exception as e:
            return _handle_response_failure(message={"detail": str(e)})


    def _get_tutoring_sessions_for_student(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            tutoring_sessions = self.uow.tutoring_sessions.get_tutoring_sessions_for_student(student_code)
            if tutoring_sessions:
                return ResponseSuccess(
                    tutoring_sessions
                )
            return _handle_response_failure(student_code_=student_code)

    def _get_tutoring_sessions_for_teacher(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            tutoring_sessions = self.uow.tutoring_sessions.get_tutoring_sessions_for_teacher(teacher_code)
            if tutoring_sessions:
                return ResponseSuccess(
                    tutoring_sessions
                )
            return _handle_response_failure(teacher_code=teacher_code)