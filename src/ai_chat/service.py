import g4f
from g4f.Provider import GeekGpt

class AIChat:
    def __init__(self):
        self.messages = []

    @staticmethod
    def _ask_gpt(messages: list) -> str:
        
        max_retries = 5
        num_retries = 0
        
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
            provider=GeekGpt,
        )
        
        # Иногда по непонятной причине возвращает пустой ответ, попытка уменьшить вероятность на пустой ответ.
        while num_retries < max_retries:
            
            num_retries += 1
            
            response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
            provider=GeekGpt,
        )
        
        return response

    def get_ai_advice(self, prompt: str) -> str:
        
        self.messages.append({"role": "user", "content": prompt})

        gpt_response = self._ask_gpt(messages=self.messages)
        
        self.messages.append({"role": "assistant", "content": gpt_response})

        return gpt_response



class AIManager:

    def __init__(self) -> None:
        self.ai_chat = AIChat()

    