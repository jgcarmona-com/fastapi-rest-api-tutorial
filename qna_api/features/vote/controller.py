from fastapi import APIRouter, Depends, HTTPException, status
from qna_api.features.vote.commands.add_answer_vote_command import AddAnswerVoteCommand
from qna_api.features.vote.commands.add_question_vote_command import AddQuestionVoteCommand
from qna_api.features.vote.models import VoteCreate, Vote
from qna_api.crosscutting.authorization import get_authenticated_user
from qna_api.crosscutting.logging import get_logger
from qna_api.features.user.models import User
from mediatr import Mediator

logger = get_logger(__name__)

class VotesController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/question/{question_id}/vote", response_model=Vote)(self.vote_on_question)
        self.router.post("/question/{question_id}/answer/{answer_id}/vote", response_model=Vote)(self.vote_on_answer)

    async def vote_on_question(self, question_id: int, vote: VoteCreate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is casting a vote on question {question_id}")
        try:
            response = await self.mediator.send_async(AddQuestionVoteCommand(vote, current_user.id, question_id))
            return response
        except ValueError as e:
            logger.error(f"Error casting vote: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def vote_on_answer(self, answer_id: int, vote: VoteCreate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is casting a vote on answer {answer_id}")
        try:
            response = await self.mediator.send_async(AddAnswerVoteCommand(vote, current_user.id, answer_id))
            return response
        except ValueError as e:
            logger.error(f"Error casting vote: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
