import logging
import os
import debugpy
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from qna_api.answers.repositories import AnswerRepository
from qna_api.answers.services import AnswersService
from qna_api.auth.repositories import UserRepository
from qna_api.auth.services import AuthService
from qna_api.core import constants
from qna_api.auth.routes import AuthController, get_auth_service
from qna_api.core.database import get_db, init_db
from qna_api.questions.repositories import QuestionRepository
from qna_api.questions.routes import QuestionsController
from qna_api.answers.routes import AnswersController
from qna_api.core.logging import get_logger
import uvicorn

from qna_api.questions.services import QuestionsService


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Inicializa la base de datos
    yield

app = FastAPI(
    title=constants.TITLE,
    description=constants.DESCRIPTION,
    version=os.environ.get("API_VERSION", "Not found"),
    contact=constants.CONTACT,
    license_info=constants.LICENSE_INFO,
    swagger_ui_parameters=constants.SWAGGER_UI_PARAMETERS,
    lifespan=lifespan
)

# Create REPOSITORIES with the DATABASE dependencies
def get_user_repository(db=Depends(get_db)):
    return UserRepository(db)

def get_question_repository(db=Depends(get_db)):
    return QuestionRepository(db)

def get_answers_repository(db=Depends(get_db)):
    return AnswerRepository(db)

# Create SERVICES with the REPOSITORIES dependencies
def get_auth_service(user_repo=Depends(get_user_repository)):
    return AuthService(user_repo)

def get_questions_service(question_repo=Depends(get_question_repository)):
    return QuestionsService(question_repo)

def get_answers_service(answers_repo=Depends(get_answers_repository)):
    return AnswersService(answers_repo)

# Create the CONTROLLERS with the SERVICES dependencies
def get_auth_controller(auth_service=Depends(get_auth_service)):
    return AuthController(auth_service)

def get_questions_controller(questions_service=Depends(get_questions_service), auth_service=Depends(get_auth_service)):
    return QuestionsController(questions_service, auth_service)

def get_answers_controller(answers_service=Depends(get_answers_service), auth_service=Depends(get_auth_service)):
    return AnswersController(answers_service, auth_service)

user_repo = UserRepository(get_db())
auth_service = get_auth_service(user_repo)
auth_controller = AuthController(auth_service)

app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(get_questions_controller().router, prefix="/questions", tags=["questions"])
app.include_router(get_answers_controller().router, prefix="/answers", tags=["answers"])


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():    
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    if os.getenv("DEBUG_MODE") == "true":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)
