from pydantic import BaseModel, Field
from datetime import  date, time
from typing import Optional

class OllamaPrompt(BaseModel):
    model: Optional[str] = Field(default=None)
    prompt : str
    stream: bool = True
    clear_chat: bool = False
    