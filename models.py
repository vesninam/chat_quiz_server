from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship

from database import Base


# Declare Classes / Tables

class QuizQuestions(Base):
    __tablename__ = 'quiz_questions'
    quiz_id = Column( ForeignKey('quizes.id'), primary_key=True)
    question_id = Column( ForeignKey('questions.id'), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    topics = Column(String)
    is_active = Column(Boolean, default=True)
    responses = relationship("QuestionResponse", back_populates="user")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    answer1 = Column(String)
    answer2 = Column(String)
    answer3 = Column(String)
    answer4 = Column(String)
    correct_answers = Column(String)
    topics = Column(String)
    responses = relationship("QuestionResponse", back_populates="question")
    quizes = relationship("Quiz", 
                          secondary="quiz_questions", 
                          back_populates="questions")

class QuestionResponse(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    response_time = Column(DateTime, unique=False, index=True)
    answer = Column(String)
    
    question = relationship("Question", back_populates="responses")
    user = relationship("User", back_populates="responses")

class Quiz(Base):
    __tablename__ = "quizes"
    id = Column(Integer, primary_key=True, index=True)
    creation_time = Column(DateTime, unique=False, index=True)
    start_time = Column(DateTime, unique=False, index=True)
    finish_time = Column(DateTime, unique=False, index=True)
    repeat_days = Column(Integer, unique=False, index=False)
    questions = relationship("Question", 
                             secondary="quiz_questions",
                             back_populates="quizes")

