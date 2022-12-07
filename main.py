from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

import crud, models, schemas

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tid(db, telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Telegram ID already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, 
               db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int,
              db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users_by_tid/{telegram_id}", response_model=schemas.User)
def read_user(telegram_id: int,
              db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tid(db, telegram_id=telegram_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, 
                    db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)

@app.get("/questions/", response_model=list[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, 
                   db: Session = Depends(get_db)):
    questions = crud.get_questions(db=db, skip=skip, limit=limit)
    return questions

@app.get("/questions/{question_id}", response_model=schemas.Question)
def read_questions(question_id: int, 
                   db: Session = Depends(get_db)):
    db_question = crud.get_question_by_id(db=db, question_id=question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Could not find question")
    return db_quizquestion


@app.post("/quiz/", response_model=schemas.Quiz)
def create_quiz(quiz: schemas.QuizBase, 
                db: Session = Depends(get_db)):
    return crud.create_quiz(db=db, quiz=quiz)

@app.post("/quiz/add_question/{quiz_id}", response_model=schemas.Quiz)
def add_question_quiz(quiz_id: int,
                      question_id: int,
                      db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz_by_id(db, quiz_id=quiz_id)
    db_question = crud.get_question_by_id(db, question_id=question_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Could not find quiz")
    if not db_question:
        raise HTTPException(status_code=404, detail="Could not find question")
    return crud.add_question_to_quiz(db=db, 
                                     quiz_id=quiz_id, 
                                     question_id=question_id)

@app.get("/quiz/", response_model=list[schemas.Quiz])
def read_quizes(skip: int = 0, limit: int = 100, 
              db: Session = Depends(get_db)):
    quizes = crud.get_quizes(db=db, skip=skip, limit=limit)
    return quizes

@app.get("/quiz/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, 
              db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz_by_id(db, quiz_id=quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Could not find quiz")
    return db_quiz

@app.get("/quiz/active/", response_model=list[schemas.Quiz])
def read_active_quizes(skip: int = 0, limit: int = 100, 
                       db: Session = Depends(get_db)):
    quizes = crud.get_quizes_active(db=db, skip=skip, limit=limit)
    return quizes

@app.post("/user_responses/", response_model=schemas.QuestionResponse)
def create_question_response(question_response:schemas.QuestionResponse, 
                             db: Session = Depends(get_db)):
    res = crud.create_response(db=db, 
                               question_response=question_response)
    return res


@app.get("/responses/", response_model=list[schemas.QuestionResponse])
def read_question_response(skip: int = 0, limit: int = 100, 
                           db: Session = Depends(get_db)):
    responses = crud.get_responses(db=db, skip=skip, limit=limit)
    return responses

@app.get("/responses_by_user/{user_id}", response_model=list[schemas.QuestionResponse])
def read_question_response_by_user(user_id: int,
                                   skip: int = 0, limit: int = 100,
                                   db: Session = Depends(get_db)):
    responses = crud.get_responses_by_user(db=db, 
                                           user_id=user_id, 
                                           skip=skip, limit=limit)
    return responses

@app.get("/responses_by_question/{question_id}", response_model=list[schemas.QuestionResponse])
def read_question_response_by_question(question_id: int,
                                   skip: int = 0, limit: int = 100,
                                   db: Session = Depends(get_db)):
    responses = crud.get_responses_by_question(db=db, 
                                               user_id=user_id, 
                                               skip=skip, limit=limit)
    return responses
