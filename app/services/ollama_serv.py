import aiohttp
from app.schema.ollama_dto import OllamaPrompt as OllamaDTO
from app.repository.ollama_repo import OllamaStreamChat as OllamaRepo
from typing import AsyncGenerator, Dict, Any
import json

class OllamaStreamChat:
    def __init__(self, repo: OllamaRepo):
        ollama_config = self.load_ollama_config()
        #self.model_name = model_name
        self.model_name = ollama_config.get('DEFAULT_MODEL')
        #print("Config Default Model: ", ollama_config.get('DEFAULT_MODEL'))
        self.messages = []
        #self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_url = ollama_config.get('OLLAMA_API_URL') + "/api/generate"
    
    def load_ollama_config(self):
        with open('app/configs/ai_ollama_config.json', 'r') as file:
            return json.load(file)
        
    async def stream_chat(self, ollamaPrompt: OllamaDTO, session: aiohttp.ClientSession) -> AsyncGenerator[str, None]:
        """Stream chat response using REST API"""
        #print("In Service - ", ollamaPrompt)
        payload = {
            "model": self.model_name,
            "prompt": ollamaPrompt.prompt,
            "stream": True
        }
        #print("Ollama Service - Streaming chat with payload: ", payload)
        try:
            async with session.post(self.ollama_url, json=payload) as response:
                response.raise_for_status()
                
                async for line in response.content:
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line:
                            chunk = json.loads(decoded_line)
                            
                            if 'response' in chunk:
                                yield f"data: {json.dumps({'response': chunk['response']})}\n\n"
                            
                            if chunk.get('done', False):
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                
        except Exception as e:
            error_data = {"error": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"

    def _build_prompt(self, new_message: str) -> str:
        """Build prompt from conversation history"""
        if not self.messages:
            return new_message
        
        # Combine history with new message
        history = "\n".join(self.messages)
        return f"{history}\nYou: {new_message}\nAssistant:"
    
    async def handle_non_streaming(self, prompt: str) -> Dict[str, Any]:
        """Handle non-streaming requests"""
        async with aiohttp.ClientSession() as session:
            full_response = ""
            async for chunk in self.stream_chat(prompt, session):
                # Parse the SSE data
                if chunk.startswith("data: "):
                    data_str = chunk[6:].strip()
                    if data_str:
                        try:
                            data = json.loads(data_str)
                            if 'response' in data:
                                full_response += data['response']
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
            
            return {
                "model": self.model_name,
                "response": full_response,
                "done": True
            }

    # Create async generator for streaming
    async def generate(self, prompt:OllamaDTO):
        #print("Ollama Service - Generating stream response...", prompt)
        async with aiohttp.ClientSession() as session:
            async for chunk in self.stream_chat(prompt, session):
                yield chunk
    
    # Create async generator for streaming
    async def health_check(self):
        try:
            # Test connection to Ollama
            ollamaUrl = self.ollama_config.get('OLLAMA_API_URL') +  "/api/tags"
            async with aiohttp.ClientSession() as session:
                async with session.get(ollamaUrl) as response:
                    if response.status == 200:
                        return {"status": "healthy", "ollama": "connected"}
                    else:
                        return {"status": "degraded", "ollama": "unavailable"}
        except:
            return {"status": "unhealthy", "ollama": "disconnected"}