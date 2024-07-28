
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from qna_api.auth.routes import AuthController
from qna_api.auth.service import AuthService
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

# Initialize the database and create tables
init_db()

# Create repository and service instances
db = next(get_db())

user_repository = UserRepository(db)
auth_service = AuthService(user_repository)
question_service = QuestionService(db)

# Create controller instances
auth_controller = AuthController(auth_service)
user_controller = UserController(auth_service)
question_controller = QuestionController(question_service, auth_service)



app.include_router(auth_controller.router, prefix="", tags=["auth"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(question_controller.router, prefix="/questions", tags=["questions"])


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():    
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    if os.getenv("DEBUG_MODE") == "true":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)
