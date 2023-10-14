from datetime import datetime

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import psycopg2
from starlette.responses import JSONResponse

from project.database import get_db
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from project.questions.models import Question
import urllib.request
import json
from sqlalchemy import desc


def get_questions(questions_num: int):
    URL = f"https://jservice.io/api/random?count={questions_num}"
    with urllib.request.urlopen(URL) as response_data:
        data = response_data.read()
        return json.loads(data)


class QuestionCreate(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
    added_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class QuestionsNum(BaseModel):
    questions_num: int = 1


def create_app() -> FastAPI:
    app = FastAPI()

    from project.questions import questions_router

    app.include_router(questions_router)

    # @app.post("/questions/", response_model=QuestionCreate)
    @app.post("/questions/", )
    def load_and_return_question(questions_num: QuestionsNum, db: Session = Depends(get_db)) -> QuestionCreate:

        question = db.query(Question).order_by(desc(Question.added_at)).first()

        url_data = get_questions(questions_num.questions_num)
        while url_data:
            url_answer = url_data.pop()
            id = url_answer['id']
            if not bool(db.query(Question).filter_by(id=id).all()):
                db_question = Question(id=url_answer['id'],
                                       question=url_answer['question'].replace("\"", "\'"),
                                       answer=url_answer['answer'].replace("\"", "\'"),
                                       created_at=url_answer['created_at'])
                db.add(db_question)
            else:
                url_data.append(get_questions(1)[0])
            db.commit()

        if not question:
            return JSONResponse(status_code=200,
                                content={'id': None, 'question': None, 'answer': None, 'created_at': None,
                                         'added_at': None})

        return question

    return app
