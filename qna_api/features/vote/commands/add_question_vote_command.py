from mediatr import Mediator
from qna_api.domain.vote import VoteEntity
from qna_api.features.vote.models import VoteCreate, Vote
from qna_api.features.vote.repository import VoteRepository
from qna_api.features.questions.repository import QuestionRepository

class AddQuestionVoteCommand:
    def __init__(self, vote: VoteCreate, user_id: int, question_id: int):
        self.vote = vote
        self.user_id = user_id
        self.question_id = question_id

@Mediator.handler
class AddQuestionVoteCommandHandler:
    def __init__(self):
        self.vote_repository = VoteRepository.instance()
        self.question_repository = QuestionRepository.instance()

    def handle(self, command: AddQuestionVoteCommand) -> Vote:
        vote_entity = VoteEntity(
            user_id=command.user_id,
            question_id=command.question_id,
            vote_value=command.vote.vote_value
        )
        self.vote_repository.create(vote_entity)

        question = self.question_repository.get(command.question_id)
        question.score += command.vote.vote_value
        self.question_repository.update(question)

        return Vote.model_validate(vote_entity, from_attributes=True)