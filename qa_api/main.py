from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from qa_api.routes import router
import uvicorn


app = FastAPI()

app.include_router(router)

@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)