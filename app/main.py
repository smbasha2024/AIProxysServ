from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import customer_router, user_router, demo_router, email_router
from app.configs import migration
import json

from app.auth.auth import load_api_keys, auth_middleware_call

app = FastAPI(
    title = "AIProxys Server",
    description = "AIProxys API Servrer.",
    version = "1.0.0"
)
app.include_router(user_router.userRoutes)
app.include_router(customer_router.customerRoutes)
app.include_router(demo_router.demoRoutes)
app.include_router(email_router.emailRoutes)

def load_api_server_config():
    with open('app/configs/api_server_config.json', 'r') as file:
        return json.load(file)
    
api_server_config = load_api_server_config()
origins = api_server_config.get('cors_ursl')

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    #allow_origins = ["*"]  # allow all origins
)

@app.on_event("startup")
async def startup_event():
    app.state.api_keys = load_api_keys()

# Middleware to check API key for all requests
app.middleware("http")(auth_middleware_call)

@app.get("/")
def root():
    return {"message": f"Welcome to {app.title} {app.version}. It's an {app.description}"}

# ----------------- Create Database and Tables if not exists --------------
migration.migrate()