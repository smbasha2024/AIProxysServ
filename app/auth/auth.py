from typing import List
from pathlib import Path
import secrets
import json
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schema.api_config_dto import APIKeyConfig

def verify_api_key():
    return True

def verify_token():
    return False

def authenticate_user():
    api = verify_api_key()
    token = verify_token()

    if api and token:
        return True
    else:
        return False
    



# Load configuration
def load_api_keys() -> List[APIKeyConfig]:
    config_path = Path("app/configs/api_key_config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Convert each API key dict to APIKeyConfig object
    api_keys = [APIKeyConfig(**key_data) for key_data in config.get("api_keys", [])]
    return api_keys


# Middleware to check API key for all requests
def auth_middleware(request: Request):
    api_key = request.headers.get("X-API-Key")
    
    missing_key = True
    if not api_key:
       return {"missing_key": missing_key, "valid_key": False, "key_config": None}
    
    # Check if the API key matches any of the stored keys
    missing_key = False
    valid_key = False
    key_config = None
    
    for stored_key in request.app.state.api_keys:
        if secrets.compare_digest(api_key, stored_key.key) and stored_key.enabled:
            valid_key = True
            key_config = stored_key
            break
    
    if not valid_key:
        return {"missing_key": missing_key, "valid_key": valid_key, "key_config": None}
    
    return {"missing_key": missing_key, "valid_key": valid_key, "key_config": key_config} #await call_next(request) 


async def auth_middleware_call(request: Request, call_next):
    # Skip auth for docs and openapi endpoints
    if request.method == "OPTIONS" or request.url.path in ["/docs", "/redoc", "/openapi.json", "/"]:
        return await call_next(request)
    
    response_config = auth_middleware(request)

    #print("Response Config:", response_config)
    # Raise Missing API Key error
    if response_config["missing_key"]:
        return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "API Key is missing"}
            )
    
    # Raise Invalid API Key error
    if not response_config["valid_key"]:
        return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid API Key"}
            )

    # Store the key configuration in the request state for later use
    request.state.api_key_config = response_config["key_config"]

    return await call_next(request)