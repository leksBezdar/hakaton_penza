import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.auth.routers import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from src.films.routers import router as films_router
from src.user.routers import router as user_router


app = FastAPI(
    title='AsQi'
)

app.include_router(auth_router, tags=["Registration"])
app.include_router(films_router, tags=["Films"])
app.include_router(user_router, tags=["User actions"])


origins = [
    "*"
]

# Добавление middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs"><h1>Documentation</h1></a><br>
    <a href="http://127.0.0.1:8000/redoc"><h1>ReDoc</h1></a>
    """


if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)