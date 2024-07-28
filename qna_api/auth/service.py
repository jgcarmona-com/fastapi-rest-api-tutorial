from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pytest import Session
from qna_api.auth.models import TokenData
from qna_api.core import database
from qna_api.core.config import settings
from qna_api.domain.user import UserEntity
from qna_api.user.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, username: str, password: str) -> UserEntity | None:
        user = self.user_repo.get_by_username(username)
        if not user or not self._verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username, roles=payload.get("roles"))
        except JWTError:
            raise credentials_exception

        user_repo = UserRepository(db)
        user = user_repo.get_by_username(token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
