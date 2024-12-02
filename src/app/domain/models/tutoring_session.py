import datetime
from sqlmodel import  SQLModel, Field


class TutoringSession(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    student_code: str = Field(max_length=8, unique=True)
    teacher_code: str = Field(unique=True)
    session_date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    notes: str | None
