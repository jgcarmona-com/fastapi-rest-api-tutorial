from mediatr import Mediator
from qna_api.features.user.repository import UserRepository
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class DeleteUserCommand:
    def __init__(self, user_id: int):
        self.user_id = user_id

@Mediator.handler
class DeleteUserCommandHandler:
    def __init__(self):
        self.user_repository = UserRepository.instance()

    def handle(self, command: DeleteUserCommand) -> None:
        logger.info(f"Deleting user with id: {command.user_id}")
        try:
            self.user_repository.delete(command.user_id)
        except Exception as e:
            raise ValueError(f"Error deleting user: {str(e)}")
