from sqlalchemy.orm import Session
from qna_api.domain.question import QuestionEntity
from qna_api.questions.models import QuestionCreate, QuestionResponse

def create_question(db: Session, question: QuestionCreate, user_id: int) -> QuestionResponse:
    db_question = QuestionEntity(**question.dict(), user_id=user_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return QuestionResponse.model_validate(db_question)

def get_question(db: Session, question_id: int) -> QuestionResponse:
    db_question = db.query(QuestionEntity).filter(QuestionEntity.id == question_id).first()
    return QuestionResponse.model_validate(db_question) if db_question else None

def get_all_questions(db: Session) -> list[QuestionResponse]:
    db_questions = db.query(QuestionEntity).all()
    return [QuestionResponse.model_validate(question) for question in db_questions]
