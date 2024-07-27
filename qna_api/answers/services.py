from sqlalchemy.orm import Session
from qna_api.domain.answer import AnswerEntity
from qna_api.answers.models import AnswerCreate, AnswerResponse

def create_answer(db: Session, answer: AnswerCreate, user_id: int) -> AnswerResponse:
    db_answer = AnswerEntity(**answer.dict(), user_id=user_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return AnswerResponse.model_validate(db_answer)

def get_answer(db: Session, answer_id: int) -> AnswerResponse:
    db_answer = db.query(AnswerEntity).filter(AnswerEntity.id == answer_id).first()
    return AnswerResponse.model_validate(db_answer) if db_answer else None

def get_answers_for_question(db: Session, question_id: int) -> list[AnswerResponse]:
    db_answers = db.query(AnswerEntity).filter(AnswerEntity.question_id == question_id).all()
    return [AnswerResponse.model_validate(answer) for answer in db_answers]
