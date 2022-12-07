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
        schema_extra = {
            "example": {
                "description": "What is liquid?",
                "answer1": "wood",
                "answer2": "ice",
                "answer3": "water",
                "answer4": "juice",
                "correct_answers": "3,4",
                "topics": "materials, common sense",
            }
        }


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
    
class QuestionDetailed(QuestionCreate):
    quizes: list[QuizBase] = []
    responses: list[QuestionResponse] = []


class Quiz(QuizBase):
    id: int
    questions: list[Question]

class UserBase(BaseModel):
    telegram_id: str

class UserCreate(UserBase):
    password: str
    topics: str

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True
        
class UserDetailed(User):
    responses: list[QuestionResponse] = []

