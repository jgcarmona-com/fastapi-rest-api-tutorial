import logging
import os
import debugpy
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from qa_api import constants
from qa_api.routes import router
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=constants.TITLE,
    description=constants.DESCRIPTION,
    version=os.environ.get("API_VERSION", "Not found"),
    contact=constants.CONTACT,
    license_info=constants.LICENSE_INFO,
    swagger_ui_parameters=constants.SWAGGER_UI_PARAMETERS,
)

app.include_router(router)

@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():    
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    if os.getenv("DEBUG_MODE") == "true":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)