from pydantic import BaseModel
from datetime import datetime

class QuestionCreate(BaseModel):
    description: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    correct_answers: str 
    topics: str
    
    class Config:
        orm_mode = True


class QuizBase(BaseModel):
    start_time: datetime
    finish_time: datetime
    creation_time: datetime
    repeat_days: int

    class Config:
        orm_mode = True

class QuestionResponse(BaseModel):
    question_id: int 
    user_id: int
    response_time: datetime 
    answer: str 

    class Config:
        orm_mode = True


class Question(QuestionCreate):
    id: int
    quizes: list[QuizBase] = []
    responses: list[QuestionResponse] = []


class Quiz(QuizBase):
    id: int
    questions: list[QuestionCreate]

class UserBase(BaseModel):
    telegram_id: str

class UserCreate(UserBase):
    password: str
    topics: str

class User(UserBase):
    id: int
    is_active: bool
    responses: list[QuestionResponse] = []

    class Config:
        orm_mode = True
