
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from mediatr import Mediator
from qna_api.answers.controller import AnswerController
from qna_api.answers.service import AnswerService
from qna_api.auth.controller import AuthController
from qna_api.auth.auth_service import AuthService
from qna_api.core import constants
from qna_api.core.database import get_db, init_db
from qna_api.core.logging import get_logger
from qna_api.questions.controller import QuestionController
from qna_api.questions.repository import QuestionRepository
from qna_api.questions.service import QuestionService
from qna_api.user.controller import UserController
from qna_api.user.repository import UserRepository
import debugpy
import os
import uvicorn

from qna_api.user.service import UserService


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield



def create_app(
        mediator=None,
        question_service=None,
        answer_service=None,
        auth_service=None):
    app = FastAPI(
        title="API",
        description="API Description",
        version="0.1",
        contact={},
        license_info={},
        swagger_ui_parameters={},
        lifespan=lifespan
    )

    db = next(get_db())

    user_repository = UserRepository.instance()

    if not mediator:
        mediator = Mediator()
    if not question_service:
        question_service = QuestionService(db)
    if not answer_service:
        answer_service = AnswerService(db)
    if not auth_service:
        auth_service = AuthService(user_repository)

    auth_controller = AuthController(auth_service)
    user_controller = UserController(mediator)
    question_controller = QuestionController(question_service)
    answer_controller = AnswerController(answer_service)

    app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
    app.include_router(user_controller.router, prefix="/user", tags=["user"])
    app.include_router(question_controller.router, prefix="/question", tags=["question"])
    app.include_router(answer_controller.router, prefix="/answer", tags=["answer"])

    return app

app = create_app()


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():    
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    if os.getenv("DEBUG_MODE") == "true":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)
