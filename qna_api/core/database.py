from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from qna_api.core.config import settings
from passlib.context import CryptContext

from qna_api.domain.role import Role

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from qna_api.domain.user import UserEntity
    from qna_api.domain.question import QuestionEntity
    from qna_api.domain.answer import AnswerEntity
    from qna_api.features.auth.auth_service import AuthService
    from qna_api.features.user.repository import UserRepository

    Base.metadata.create_all(bind=engine)

    # Create an initial admin user if none exists
    db = SessionLocal()
    user_repo = UserRepository(db)

    if not user_repo.get_by_username(settings.initial_admin_username):
        admin_user = UserEntity(
            username=settings.initial_admin_username,
            email=settings.initial_admin_email,
            full_name="API Admin",
            hashed_password=pwd_context.hash(settings.initial_admin_password),
            disabled=False
        )
        admin_user.set_roles([Role.ADMIN, Role.USER])
        user_repo.create(admin_user)
    db.close()
