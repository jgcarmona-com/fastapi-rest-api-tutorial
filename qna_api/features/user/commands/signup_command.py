from mediatr import Mediator
from qna_api.crosscutting.notification_service import NotificationService
from qna_api.features.auth.auth_service import AuthService
from qna_api.crosscutting.logging import get_logger
from qna_api.domain.role import Role
from qna_api.domain.user import UserEntity
from qna_api.features.user.models import SignupModel
from qna_api.features.user.repository import UserRepository

logger = get_logger(__name__)

class SignupCommand():    
    def __init__(self, user: SignupModel):
        self.user = user
        
@Mediator.handler
class SignupCommandHandler():
    def __init__(self):
        self.user_repository = UserRepository.instance()
        self.notification_service = NotificationService.from_env_vars()
        self.auth_service = AuthService(self.user_repository)

    async def handle(self, request: SignupCommand) -> UserEntity:   
        logger.info(f"Creating user: {request.user.username}")      
        user = UserEntity(
            username=request.user.username,
            email=request.user.email,
            full_name=request.user.full_name,
            hashed_password=AuthService.get_password_hash(request.user.password),
            disabled=True
        )
        user.set_roles([Role.USER])

        try:
            self.user_repository.create(user)
            verification_token = self.auth_service.create_verification_token(user.id)
            verification_url = f"http://localhost:8000/user/validate?token={verification_token}"
            await self.notification_service.send_email_verification(user.email, verification_url)
        except ValueError as e:
            raise ValueError(f"Error creating user: {str(e)}")
        
        return user
