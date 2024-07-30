from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from mediatr import Mediator
from qna_api.features.answers.controller import AnswerController
from qna_api.features.auth.auth_service import AuthService
from qna_api.features.auth.controller import AuthController
from qna_api.core.database import get_db, init_db
from qna_api.crosscutting.logging import get_logger
from qna_api.features.questions.controller import QuestionController
from qna_api.features.user.controller import UserController
from qna_api.features.user.repository import UserRepository
import debugpy
import os
import uvicorn

from qna_api.features.vote.controller import VotesController

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

def create_app(
        mediator=None,
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

    user_repository = UserRepository.instance()

    if not mediator:
        mediator = Mediator()
    if not auth_service:
        auth_service = AuthService(user_repository)

    auth_controller = AuthController(auth_service)
    user_controller = UserController(mediator)
    question_controller = QuestionController(mediator)
    answer_controller = AnswerController(mediator)
    votes_controller = VotesController(mediator)

    app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
    app.include_router(user_controller.router, prefix="/user", tags=["user"])
    app.include_router(question_controller.router, prefix="/question", tags=["question"])
    app.include_router(answer_controller.router, prefix="/question", tags=["Answer"]) # Depends on question
    app.include_router(votes_controller.router, tags=["Vote"])

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
