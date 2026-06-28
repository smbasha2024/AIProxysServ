from fastapi import APIRouter, Depends
from app.schema.email_dto import Email as EmailDTO
from app.schema.email_extra_dto import EmailExtra as EmailExtraDTO
from app.repository.email_repo import Email as EmailRepo
from app.services.email_serv import Email as EmailServ
from app.configs.dependencies import get_service_factory

emailRoutes = APIRouter(prefix="/emails", tags=["emails"])

email_service_dep = get_service_factory(EmailServ, EmailRepo)

@emailRoutes.post("/semail/")
async def send_email(email: EmailDTO, service: EmailServ = Depends(email_service_dep)):
    result = service.sendEmail(email)
    return result

@emailRoutes.post("/")
async def send_email_extra(email: EmailExtraDTO, service: EmailServ = Depends(email_service_dep)):
    result = service.sendEmailExtras(email)
    return result

@emailRoutes.get("/smtp-test")
async def smtp_test():
    try:
        import asyncio
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection("smtp.gmail.com", 587),
            timeout=10,
        )

        writer.close()
        await writer.wait_closed()

        return {"status": "Connected"}

    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e),
            "type": type(e).__name__,
        }

@emailRoutes.get("/smtp-test-465")
async def smtp_test():
    try:
        import asyncio
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection("smtp.gmail.com", 465),
            timeout=20,
        )

        writer.close()
        await writer.wait_closed()

        return {"status": "Connected"}

    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e),
            "type": type(e).__name__,
        }

@emailRoutes.get("/google-test")
async def google_test():
    try:
        import asyncio
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection("google.com", 443),
            timeout=10,
        )

        writer.close()
        await writer.wait_closed()

        return {"status": "Connected"}

    except Exception as e:
        return {
            "status": "Failed",
            "type": type(e).__name__,
            "error": str(e),
        }
