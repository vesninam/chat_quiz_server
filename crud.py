from sqlalchemy.orm import Session
from datetime import datetime

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_tid(db: Session, telegram_id: str):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash(user.password)
    db_user = models.User(telegram_id=user.telegram_id, 
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()

def get_question_by_id(db: Session, 
                       question_id: int):
    res = db.query(models.Question). \
           filter(models.Question.id == question_id).first()
    return res

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_quizes(db: Session, 
               skip: int = 0, limit: int = 100):
    res = db.query(models.Quiz).\
        offset(skip).limit(limit).all()
    return res

def get_quizes_active(db: Session, 
                      skip: int = 0, limit: int = 100):
    _now = datetime.now()
    res = db.query(models.Quiz).filter(models.Quiz.start_time <= _now). \
                                filter(models.Quiz.finish_time >= _now).all()
    return res


def get_quiz_by_id(db: Session, 
                   quiz_id: int):
    res = db.query(models.Quiz). \
           filter(models.Quiz.id == quiz_id).first()
    return res

def create_quiz(db: Session, quiz: schemas.Quiz):
    db_quiz = models.Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def add_question_to_quiz(db: Session, quiz_id: int, question_id: int):
    db_quiz = get_quiz_by_id(db, quiz_id)
    db_question = get_question_by_id(db, question_id)
    if db_question in db_quiz.questions:
        pass
    else:
        db.add(models.QuizQuestions(quiz_id=quiz_id, question_id=question_id))
    db.commit()
    db.refresh(db_quiz)
    return db_quiz
    

def create_response(db: Session,
                    question_response: schemas.QuestionResponse):
    resp = question_response.dict()
    resp["response_time"] = datetime.now()
    db_response = models.QuestionResponse(**resp)
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_responses(db: Session, 
                  skip: int = 0, limit: int = 100):
    res = db.query(models.QuestionResponse). \
        offset(skip).limit(limit).all()
    return res

def get_responses_by_user(db: Session, user_id: int, 
                          skip: int = 0, limit: int = 100):
    res = db.query(models.QuestionResponse). \
        filter(models.QuestionResponse.user_id == user_id). \
        offset(skip).limit(limit).all()
    return res

def get_responses_by_question(db: Session, question_id: int, 
                              skip: int = 0, limit: int = 100):
    res = db.query(models.QuestionResponse). \
        filter(models.QuestionResponse.question_id == question_id). \
        offset(skip).limit(limit).all()
    return res
