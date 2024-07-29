from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from qna_api.auth.auth_service import AuthService
from qna_api.core.config import settings
from qna_api.auth.models import TokenData
from fastapi import HTTPException, status

from qna_api.domain.user import UserEntity
from qna_api.user.models import UserCreate, UserUpdate
from qna_api.user.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_user(self, user_create: UserCreate) -> UserEntity:
        hashed_password = AuthService.get_password_hash(user_create.password)
        db_user = UserEntity(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            disabled=False
        )
        return self.user_repo.create(db_user)
    
    def update_user(self, user_id: int, user_update: UserUpdate, current_user: UserEntity) -> UserEntity:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if user.id != current_user.id and 'admin' not in [role.value for role in current_user.get_roles()]:
            return None  # Current user is not allowed to update this user
        user.username = user_update.username or user.username
        user.email = user_update.email or user.email
        user.full_name = user_update.full_name or user.full_name
        user.disabled = user_update.disabled if user_update.disabled is not None else user.disabled
        if user_update.password:
            user.hashed_password = AuthService._get_password_hash(user_update.password)
        return self.user_repo.update(user)
