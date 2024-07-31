from mediatr import Mediator
from qna_api.features.user.repository import UserRepository
from qna_api.features.user.models import User
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class GetAllUsersQuery:
    pass

@Mediator.handler
class GetAllUsersQueryHandler:
    def __init__(self):
        self.user_repository = UserRepository.instance()

    def handle(self, query: GetAllUsersQuery) -> list[User]:
        users = self.user_repository.get_all()
        if not users:
            raise ValueError("No users found")

        return [User.model_validate(user, from_attributes=True) for user in users]
