from sqlalchemy.orm import Session
from qna_api.questions.models import QuestionCreate, QuestionResponse
from qna_api.domain.question import QuestionEntity

class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    def create_question(self, question: QuestionCreate, user_id: int) -> QuestionResponse:
        db_question = QuestionEntity(
            title=question.title,
            description=question.description,
            user_id=user_id
        )
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return QuestionResponse.from_orm(db_question)

    def get_question(self, question_id: int) -> QuestionResponse:
        db_question = self.db.query(QuestionEntity).filter(QuestionEntity.id == question_id).first()
        if db_question is None:
            return None
        return QuestionResponse.from_orm(db_question)

    def get_all_questions(self) -> list[QuestionResponse]:
        questions = self.db.query(QuestionEntity).all()
        return [QuestionResponse.from_orm(q) for q in questions]
