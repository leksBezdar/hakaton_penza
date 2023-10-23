import g4f

from sqlalchemy.ext.asyncio import AsyncSession

class AIChat:
    
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    @staticmethod
    def get_ai_advice(prompt: str) -> str:
        
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo_16k_0613,
            messages=[{"role": "user", "content": prompt}],
        )
        
        return response
    