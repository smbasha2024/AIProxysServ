from fastapi import APIRouter, Depends
from app.schema.email_dto import Email as EmailDTO
from app.services.email_serv import Email as EmailServ
from app.configs.dependencies import get_email_service

emailRoutes = APIRouter(prefix="/emails", tags=["emails"])

@emailRoutes.post("/")
async def send_email(email: EmailDTO, service: EmailServ = Depends(get_email_service)):
    result = service.sendEmail(email)
    return result
