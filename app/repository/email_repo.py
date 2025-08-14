from app.repository.base_repo import BaseRepository
from app.models.email_model import Email as EmailModel
from app.schema.email_dto import Email as EmailDTO
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
import json
import asyncio

class Email(BaseRepository[EmailModel]):
    def __init__(self):
        super().__init__(EmailModel)

    def load_smtp_config(self):
        with open('app/configs/mail_config.json', 'r') as file:
            return json.load(file)

    def emailConfig(self):
        smtp_config = self.load_smtp_config()
        conf = ConnectionConfig(
            MAIL_USERNAME = smtp_config.get('MAIL_USERNAME'), # "AIProxyBots@gmail.com",
            MAIL_PASSWORD = smtp_config.get('MAIL_PASSWORD'),  # "uawcdjqovodpinsu",  # App password from Step 1
            MAIL_FROM = smtp_config.get('MAIL_FROM'),  #"AIProxyBots@gmail.com",
            MAIL_PORT = smtp_config.get('MAIL_PORT'),  #465,
            MAIL_SERVER = smtp_config.get('MAIL_SERVER'), #"smtp.gmail.com",
            MAIL_STARTTLS = smtp_config.get('MAIL_STARTTLS'), #False,   # For port 465, SSL/TLS is True
            MAIL_SSL_TLS = smtp_config.get('MAIL_SSL_TLS'), #True,     
            USE_CREDENTIALS = smtp_config.get('USE_CREDENTIALS'),  #True,
            VALIDATE_CERTS = smtp_config.get('VALIDATE_CERTS') #True
        )
        return conf

    async def sendEmail(self, email: EmailDTO):
        message = MessageSchema(
            subject = email.subject,
            recipients = email.email,
            body = email.message,
            subtype="html"
        )
        
        conf = self.emailConfig()
        fa = FastMail(conf)
        await fa.send_message(message)

        return {"message": "Email sent successfully"}
    
    def sendEmailBackground(self, email: EmailDTO):
        asyncio.create_task(self.sendEmail(email))
        return {"message": "Email sent successfully"}