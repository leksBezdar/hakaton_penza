import g4f
from g4f.Provider import GeekGpt
from time import perf_counter

from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession

class AIChat:
    def __init__(self):
        self.messages = []

    @staticmethod
    def _ask_gpt(messages: list) -> str:
        start = perf_counter()
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
            provider=GeekGpt,
        )
        end = perf_counter()
        print(end - start)
        return response

    def get_ai_advice(self, prompt: str, response: Response) -> str:
        
        self.messages.append({"role": "user", "content": "Разговаривай со мной только на русском"})
        self.messages.append({"role": "user", "content": prompt})

        gpt_response = self._ask_gpt(messages=self.messages)
        self.messages.append({"role": "assistant", "content": gpt_response})

        print(gpt_response)

        response.set_cookie(
        'gpt_response_context',
        gpt_response,
        max_age=60 * 60 * 24,
        httponly=True
    )

        print(self.messages)

        return response



class AIManager:

    def __init__(self) -> None:
        self.ai_chat = AIChat()

    