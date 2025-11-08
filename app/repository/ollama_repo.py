#OllamaAgent

from app.repository.base_repo import BaseRepository
from app.models.ollama_model import OllamaAgent as OllamaModel
from app.schema.ollama_dto import OllamaPrompt as OllamaDTO

class OllamaStreamChat(BaseRepository[OllamaModel]):
    def __init__(self):
        super().__init__(OllamaModel)