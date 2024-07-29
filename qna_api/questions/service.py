from sqlalchemy.orm import Session
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.domain.answer import AnswerEntity
from qna_api.questions.models import FullQuestionResponse, QuestionCreate, QuestionResponse
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
        return QuestionResponse.model_validate(db_question)

    def get_question(self, question_id: int) -> QuestionResponse:
        db_question = self.db.query(QuestionEntity).filter(QuestionEntity.id == question_id).first()
        if db_question is None:
            return None
        return QuestionResponse.model_validate(db_question)
    
    def get_full_question(self, question_id: int) -> FullQuestionResponse:
        db_question = self.db.query(QuestionEntity).filter(QuestionEntity.id == question_id).first()
        if db_question is None:
            return None
        
        answers = db_question.answers  
        return FullQuestionResponse(
            id=db_question.id,
            title=db_question.title,
            description=db_question.description,
            user_id=db_question.user_id,
            answers=[AnswerResponse.model_validate(answer) for answer in answers]
        )

    def get_all_questions(self) -> list[QuestionResponse]:
        questions = self.db.query(QuestionEntity).all()
        return [QuestionResponse.model_validate(q) for q in questions]
    
    def update_question(self, question_id: int, question: QuestionCreate, user_id: int) -> QuestionResponse:
        db_question = self.db.query(QuestionEntity).filter(QuestionEntity.id == question_id, QuestionEntity.user_id == user_id).first()
        if db_question is None:
            return None
        for key, value in question.dict().items():
            setattr(db_question, key, value)
        self.db.commit()
        self.db.refresh(db_question)
        return QuestionResponse.model_validate(db_question)

    def delete_question(self, question_id: int, user_id: int) -> QuestionResponse:
        db_question = self.db.query(QuestionEntity).filter(QuestionEntity.id == question_id, QuestionEntity.user_id == user_id).first()
        if db_question is None:
            return None
        self.db.delete(db_question)
        self.db.commit()
        return QuestionResponse.model_validate(db_question)

    def add_answer(self, answer: AnswerCreate, user_id: int, question_id: int) -> AnswerResponse:
        db_answer = AnswerEntity(
            content=answer.content,
            user_id=user_id,
            question_id=question_id
        )
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        return AnswerResponse.model_validate(db_answer)
    
    def get_answers(self, question_id: int) -> list[AnswerResponse]:
        answers = self.db.query(AnswerEntity).filter(AnswerEntity.question_id == question_id).all()
        return [AnswerResponse.model_validate(a) for a in answers]
