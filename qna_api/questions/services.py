from sqlalchemy.orm import Session
from qna_api.questions.models import QuestionCreate, QuestionResponse
from qna_api.questions.repositories import QuestionRepository
from qna_api.auth.models import User
from typing import List

class QuestionsService:
    def __init__(self, question_repo: QuestionRepository):
        self.question_repo = question_repo

    def create_question(self, question: QuestionCreate, user_id: int) -> QuestionResponse:
        return self.question_repo.create(question, user_id)

    def get_all_questions(self) -> List[QuestionResponse]:
        return self.question_repo.get_all()

    def get_question(self, question_id: int) -> QuestionResponse:
        return self.question_repo.get(question_id)
