from pydantic import BaseModel
from datetime import  date, time

class OllamaPrompt(BaseModel):
    model: str
    prompt : str
    stream: bool = True
    clear_chat: bool = False
    