import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BASE_URL = "https://api.kinoafisha.info/export/"
API_KEY = os.environ.get("API_KEY")


html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Chat</title>
    <style>
        #chat-box {
            height: 300px;
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 10px;
        }

        #message-input {
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div id="chat-box"></div>
    <input type="text" id="message-input" placeholder="Type your message">
    <button onclick="sendMessage()">Send</button>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws/comment/all");

        // Отправка данных на сервер при подключении
        socket.addEventListener("open", (event) => {
            console.log("WebSocket connection opened");
            const requestData = {
                "film_id": 723,
                "offset": 0,
                "limit": 10,
            };
            socket.send(JSON.stringify(requestData));
        });

        // Обработка полученных данных от сервера
        socket.addEventListener("message", (event) => {
            const chatBox = document.getElementById("chat-box");
            const message = JSON.parse(event.data);
            const messageElement = document.createElement("div");
            messageElement.textContent = JSON.stringify(message);
            chatBox.appendChild(messageElement);
        });

        // Отправка сообщения на сервер
        function sendMessage() {
            const messageInput = document.getElementById("message-input");
            const message = messageInput.value;
            socket.send(message);
            messageInput.value = "";
        }
    </script>
</body>
</html>
"""