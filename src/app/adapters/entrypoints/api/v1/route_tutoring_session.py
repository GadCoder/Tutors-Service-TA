import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.app.configurator.containers import Container
from src.app.domain.models.tutoring_session import TutoringSession
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES
from src.app.domain.schemas import  tutoring_session as tutoring_session_schema
from src.app.domain.ports.use_cases.tutoring_session import TutoringSessionServiceInterface


router = APIRouter()

@router.post("/create")
@inject
async def create_tutoring_session(
        tutoring_session: tutoring_session_schema.TutoringSessionCreate,
        tutoring_session_service: TutoringSessionServiceInterface = Depends(Provide[Container.tutoring_session_service]),
):
    response = await tutoring_session_service.create(tutoring_session=tutoring_session)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/get-sessions-for-student")
@inject
def get_session_for_student(
        student_code: str,
        tutoring_session_service: TutoringSessionServiceInterface = Depends(Provide[Container.tutoring_session_service]),
):
    response = tutoring_session_service.get_tutoring_sessions_for_student(student_code=student_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )

@router.get("/get-sessions-for-teacher")
@inject
def get_sessions_for_teacher(
        teacher_code: str,
        tutoring_session_service: TutoringSessionServiceInterface = Depends(Provide[Container.tutoring_session_service]),
):
    response = tutoring_session_service.get_tutoring_sessions_for_teacher(teacher_code=teacher_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
   )
