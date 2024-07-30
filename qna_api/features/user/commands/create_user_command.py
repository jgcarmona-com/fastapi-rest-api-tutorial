from mediatr import Mediator
from qna_api.features.auth.auth_service import AuthService
from qna_api.core.logging import get_logger
from qna_api.domain.role import Role
from qna_api.domain.user import UserEntity
from qna_api.features.user.models import UserCreate
from qna_api.features.user.repository import UserRepository

logger = get_logger(__name__)

class CreateUserCommand():    
    def __init__(self,user:UserCreate):
        self.user = user

@Mediator.handler
class CreateUserCommandHandler():
    def __init__(self):
        self.user_repository = UserRepository.instance()

    def handle(self, request: CreateUserCommand) -> UserEntity:   
        logger.info(f"Creating user: {request.user.username}")      
        user =  UserEntity(
                    username=request.user.username,
                    email=request.user.email,
                    full_name=request.user.full_name,
                    hashed_password=AuthService.get_password_hash(request.user.password),
                    disabled=False
                )
        user.set_roles([Role.USER])

        try:
            self.user_repository.create(user)
        except ValueError as e:
            raise ValueError(f"Error creating user: {str(e)}")
        
        return user