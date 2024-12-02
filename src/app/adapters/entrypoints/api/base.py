from fastapi import APIRouter
from src.app.adapters.entrypoints.api.v1 import route_tutoring_session

api_router = APIRouter()
api_router.include_router(route_tutoring_session.router, prefix="/tutoring-session", tags=["tutoring-session"])
