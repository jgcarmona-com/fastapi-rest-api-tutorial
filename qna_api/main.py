import logging
import os
import debugpy
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from qna_api.core import constants
from qna_api.auth.routes import router as auth_router
from qna_api.core.database import init_db
from qna_api.questions.routes import router as questions_router
from qna_api.answers.routes import router as answers_router
from qna_api.core.logging import get_logger
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

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(questions_router, prefix="/questions", tags=["questions"])
app.include_router(answers_router, prefix="/answers", tags=["answers"])



@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():    
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    if os.getenv("DEBUG_MODE") == "true":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)
