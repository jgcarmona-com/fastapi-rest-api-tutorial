
from mediatr import Mediator
from fastapi import HTTPException, status
from qna_api.features.auth.auth_service import AuthService
from qna_api.features.user.repository import UserRepository
from qna_api.features.user.models import User

class ValidateUserCommand:
    def __init__(self, token: str):
        self.token = token

@Mediator.handler
class ValidateUserCommandHandler:
    def __init__(self):
        self.user_repository = UserRepository.instance()
        self.auth_service = AuthService(self.user_repository)

    def handle(self, request: ValidateUserCommand) -> User:
        try:
            payload = self.auth_service.decode_verification_token(request.token)
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
            user = self.user_repository.get(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            user.disabled = False
            self.user_repository.update(user)
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))