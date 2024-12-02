import datetime
from sqlmodel import SQLModel, Field

class TutoringSessionCreate(SQLModel):
    student_code: str = Field(max_length=8)
    teacher_code: str
    session_date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    notes: str | None


class TutoringSessionPublic(SQLModel):
    id: int
    student_code: str = Field(max_length=8)
    teacher_code: str
    session_date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    notes: str | None
