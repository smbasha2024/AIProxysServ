from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import json

from app.services.ollama_serv import OllamaStreamChat as OllamaServ
from app.repository.ollama_repo import OllamaStreamChat as OllamaRepo
from app.schema.ollama_dto import OllamaPrompt as OllamaDTO

from app.configs.dependencies import get_service_factory

aiAgentsRoutes = APIRouter(prefix="/aiagents", tags=["aiagents"])
ollama_service_dep = get_service_factory(OllamaServ, OllamaRepo)

@aiAgentsRoutes.post("/generate")
async def stream_agentic_chat(aiPrompt: OllamaDTO, service: OllamaServ = Depends(ollama_service_dep)):
    """
    Stream chat response exactly like Ollama API
    Expects JSON payload with: {"model": "model_name", "prompt": "message", "stream": True}
    """
    try:
        # Parse request body
        #body = await request.json()
        prompt = aiPrompt.prompt  #body.get("prompt", "")
        model = aiPrompt.model or "deepseek-v3.1:671b-cloud" #body.get("model", ollama_client.model_name)
        stream = aiPrompt.stream #body.get("stream", True)
        #print("In Router - ", aiPrompt)
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Update model if different
        
        if model != service.model_name:
            service.model_name = model
        
        if not stream:
            # Handle non-streaming response (for compatibility)
            return await service.handle_non_streaming(prompt)
        
        # Create async generator for streaming
        """
        async def generate():
            async with aiohttp.ClientSession() as session:
                async for chunk in ollama_client.stream_chat(prompt, session):
                    yield chunk
        """
        
        return StreamingResponse(
            service.generate(aiPrompt),
            media_type="application/x-ndjson",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #result = service.sendEmail(email)
    #return result


@aiAgentsRoutes.post("/chatstream")
async def stream_chat_with_history(chatMsg: OllamaDTO, service: OllamaServ = Depends(ollama_service_dep)):
    """
    Enhanced streaming endpoint with conversation history
    Expects: {"message": "user message", "model": "model_name", "clear_history": false}
    """
    try:
        #body = await request.json()
        user_message = chatMsg.prompt #body.get("message", "")
        model = chatMsg.model #body.get("model", ollama_client.model_name)
        clear_history = chatMsg.clear_chat #body.get("clear_history", False)
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if clear_history:
            service.messages = []
        
        # Update model if different
        if model != service.model_name:
            service.model_name = model
        
        # Build prompt with history
        prompt = service._build_prompt(user_message)
            
        # Update conversation history after streaming completes
        # Note: In production, you might want to handle this differently
        # to avoid blocking the response
        
        return StreamingResponse(
            service.generate(chatMsg),
            media_type="application/x-ndjson",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@aiAgentsRoutes.post("/clearchat")
async def clear_chat_history(service: OllamaServ = Depends(ollama_service_dep)):
    """Clear conversation history"""
    service.messages = []
    return {"status": "History cleared"}

@aiAgentsRoutes.get("/chatmodel")
async def get_available_models(service: OllamaServ = Depends(ollama_service_dep)):
    """Get available models (you might want to fetch this from Ollama)"""
    return {
        "models": [
            {
                "name": service.model_name,
                "modified_at": "2024-01-01T00:00:00.000Z",
                "size": 0,  # You might want to get actual size
                "digest": "sha256:...",
                "details": {
                    "format": "gguf",
                    "family": "deepseek"
                }
            }
        ]
    }

@aiAgentsRoutes.get("/health")
async def health_check(service: OllamaServ = Depends(ollama_service_dep)):
    """Health check endpoint"""
    return await service.health_check()