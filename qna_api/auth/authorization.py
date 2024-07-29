
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import JWTError, jwt
from qna_api.auth.models import TokenData
from qna_api.core.config import settings
from qna_api.user.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_authenticated_user(token: str = Depends(oauth2_scheme), user_repo: UserRepository = Depends(UserRepository.instance)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username, roles=payload.get("roles"))
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_admin_user(token: str = Depends(oauth2_scheme), user_repo: UserRepository = Depends(UserRepository.instance)):
    user = get_authenticated_user(token, user_repo)
    if 'admin' not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions",
        )
    return user