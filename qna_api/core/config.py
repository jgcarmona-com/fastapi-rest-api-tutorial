from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./qna.db"
    initial_admin_username: str = "admin"
    initial_admin_email: str = "juan@jgcarmona.com"
    initial_admin_password: str = "P@ssw0rd!"
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
