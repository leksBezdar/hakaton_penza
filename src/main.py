import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from src.auth.routers import router as auth_router
from src.recommendations.routers import router as recommendations_router
from src.films.routers import router as films_router
from src.reviews.routers import router as reviews_router
from src.comments.routers import router as comments_router
from src.user_actions.routers import router as user_action_router
from src.api_afisha.api_afisha import router as api_afisha_router
from src.gigachat.router import router as ai_gigachat_router

logger.add(f"/var/log/movie_rank_backend/log.log",
           format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
           encoding="utf-8",
           level="DEBUG",
           rotation="100 MB")


app = FastAPI(
    title='movieRank'
)


app.include_router(auth_router, tags=["Registration"])
app.include_router(films_router, tags=["Films"])
app.include_router(reviews_router, tags=["Reviews"])
app.include_router(comments_router, tags=["Comments"])
app.include_router(recommendations_router, tags=["Recommendations_router"])
app.include_router(user_action_router, tags=["user_actions"])
app.include_router(api_afisha_router)
app.include_router(ai_gigachat_router)


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

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("wss://www.backend.movie-rank.ru/ws/comment/create");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return f"""
#     <a href="{str(request.url)}docs"><h1>Documentation</h1></a><br>
#     <a href="{str(request.url)}redoc"><h1>ReDoc</h1></a>
#     """

if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)