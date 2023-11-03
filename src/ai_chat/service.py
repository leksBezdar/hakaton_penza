import re
import g4f
from g4f.Provider import GeekGpt

from requests.exceptions import HTTPError

class AIChat:
    def __init__(self):
        self.messages = []

    def _ask_gpt(self, messages: list) -> str:
        
        try:
             # Иногда по непонятной причине возвращает пустой ответ, попытка уменьшить вероятность на пустой ответ.
            for _ in range(5):

                response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                provider=GeekGpt
            )

                if len(response) > 1 and self._has_russian_letters(response):
                
                    return response
                
        except HTTPError as e:
            
            error_message = "Something went wrong... Please, try again"
            
            return error_message
        
    def get_ai_advice(self, prompt: str) -> str:
        
        self.messages.append({"role": "user", "content": prompt})

        gpt_response = self._ask_gpt(messages=self.messages)
        
        self.messages.append({"role": "assistant", "content": gpt_response})

        return gpt_response

    @staticmethod
    def _has_russian_letters(response: str):
        return bool(re.search('[а-яА-Я]', response))


class AIManager:

    def __init__(self) -> None:
        self.ai_chat = AIChat()

    