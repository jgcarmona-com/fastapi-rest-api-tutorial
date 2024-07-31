from mediatr import Mediator
from qna_api.features.user.repository import UserRepository
from qna_api.features.user.models import User
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class EnableUserCommand:
    def __init__(self, user_id: int):
        self.user_id = user_id

@Mediator.handler
class EnableUserCommandHandler:
    def __init__(self):
        self.user_repository = UserRepository.instance()

    def handle(self, command: EnableUserCommand) -> User:
        user = self.user_repository.get(command.user_id)
        if not user:
            raise ValueError(f"User with id {command.user_id} not found")
        if not user.disabled:
            raise ValueError(f"User with id {command.user_id} is already enabled")

        user.disabled = False
        self.user_repository.update(user)
        logger.info(f"User {user.username} has been enabled.")
        return User.model_validate(user, from_attributes=True)
