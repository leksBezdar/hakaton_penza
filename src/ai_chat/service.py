import g4f
from g4f.Provider import GeekGpt

class AIChat:
    def __init__(self):
        self.messages = []

    @staticmethod
    def _ask_gpt(messages: list) -> str:
        
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
            provider=GeekGpt,
        )
        
        while len(response) < 1:
            
            response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
            provider=GeekGpt,
        )
        
        return response

    def get_ai_advice(self, prompt: list) -> str:
        
        self.messages.append(prompt)

        gpt_response = self._ask_gpt(messages=self.messages)
        self.messages.append({"role": "assistant", "content": gpt_response})

        return gpt_response



class AIManager:

    def __init__(self) -> None:
        self.ai_chat = AIChat()

    