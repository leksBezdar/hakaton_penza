from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.auth.routers import router
from src.films.routers import router as films_router

app = FastAPI(
    title='AsQi'
)

app.include_router(router, tags=["Registration"])
app.include_router(films_router, tags=["Films"])



@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs"><h1>Documentation</h1></a><br>
    <a href="http://127.0.0.1:8000/redoc"><h1>ReDoc</h1></a>
    """