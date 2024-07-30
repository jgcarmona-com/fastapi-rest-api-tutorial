from mediatr import Mediator
from qna_api.domain.vote import VoteEntity
from qna_api.features.vote.models import VoteCreate, VoteResponse
from qna_api.features.vote.repository import VoteRepository
from qna_api.features.answers.repository import AnswerRepository

class AddAnswerVoteCommand:
    def __init__(self, vote: VoteCreate, user_id: int, answer_id: int):
        self.vote = vote
        self.user_id = user_id
        self.answer_id = answer_id

@Mediator.handler
class AddAnswerVoteCommandHandler:
    def __init__(self):
        self.vote_repository = VoteRepository.instance()
        self.answer_repository = AnswerRepository.instance()

    def handle(self, command: AddAnswerVoteCommand) -> VoteResponse:
        vote_entity = VoteEntity(
            user_id=command.user_id,
            answer_id=command.answer_id,
            vote_value=command.vote.vote_value
        )
        self.vote_repository.create(vote_entity)

        answer = self.answer_repository.get(command.answer_id)
        answer.score += command.vote.vote_value
        self.answer_repository.update(answer)

        return VoteResponse.model_validate(vote_entity, from_attributes=True)