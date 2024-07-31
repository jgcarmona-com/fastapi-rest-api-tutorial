from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from mediatr import Mediator
from qna_api.crosscutting.notification_service import NotificationService
from qna_api.features.admin.controller import AdminController
from qna_api.features.answers.controller import AnswerController
from qna_api.features.auth.auth_service import AuthService
from qna_api.features.auth.controller import AuthController
from qna_api.core.database import get_db, init_db
from qna_api.crosscutting.logging import get_logger
from qna_api.features.questions.controller import QuestionController
from qna_api.features.user.commands.signup_command import SignupCommand, SignupCommandHandler
from qna_api.features.user.controller import UserController
from qna_api.features.user.repository import UserRepository
from qna_api.core.constants import TITLE, DESCRIPTION, CONTACT, LICENSE_INFO, SWAGGER_UI_PARAMETERS, SWAGGER_FAVICON_URL

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
        auth_service=None,
        notification_service=None):
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version="0.1",
        contact=CONTACT,
        license_info=LICENSE_INFO,
        swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
        swagger_favicon_url=SWAGGER_FAVICON_URL,
        lifespan=lifespan
    )

    user_repository = UserRepository.instance()

    if not mediator:
        mediator = Mediator()
    if not auth_service:
        auth_service = AuthService(user_repository)

    # NOTE: This is an example on how to register handlers that has crosscurring dependencies:
    # if not notification_service:
    #     notification_service = NotificationService(constructor_params)
    #   mediator.register_handler(SignupCommandHandler(user_repository, notification_service)  # - Instantiate the class with its dependenices,
    #                                                 .handle,                                 # - Pass the method to be called
    #                                                  SignupCommand)                          # - Pass the Request class to be handled

    auth_controller = AuthController(auth_service)
    user_controller = UserController(mediator)
    question_controller = QuestionController(mediator)
    answer_controller = AnswerController(mediator)
    votes_controller = VotesController(mediator)
    admin_controller = AdminController(mediator)

    app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
    app.include_router(user_controller.router, prefix="/user", tags=["user"])
    app.include_router(question_controller.router, prefix="/question", tags=["question"])
    app.include_router(answer_controller.router, prefix="/question", tags=["Answer"]) 
    app.include_router(votes_controller.router, tags=["Vote"])
    app.include_router(admin_controller.router, prefix="/admin", tags=["admin"])

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
