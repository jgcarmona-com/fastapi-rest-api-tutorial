from sqlalchemy.orm import Session
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.answers.repositories import AnswerRepository
from typing import List

class AnswersService:
    def __init__(self, answer_repo: AnswerRepository):
        self.answer_repo = answer_repo

    def create_answer(self, answer: AnswerCreate, user_id: int) -> AnswerResponse:
        return self.answer_repo.create(answer, user_id)

    def get_answers_for_question(self, question_id: int) -> List[AnswerResponse]:
        return self.answer_repo.get_by_question_id(question_id)

    def get_answer(self, answer_id: int) -> AnswerResponse:
        return self.answer_repo.get(answer_id)
