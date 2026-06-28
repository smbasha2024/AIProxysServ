import os

from app.repository.base_repo import BaseRepository
from app.models.email_model import Email as EmailModel
from app.schema.email_dto import Email as EmailDTO
from app.schema.email_extra_dto import EmailExtra as EmailExtraDTO
from app.mappers.email_mapper import to_email_dto, extra_params_to_string

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

    async def sendEmail(self, email: EmailDTO, extras: str = ""):
        try:
            email.message = email.message + "<br/><br/>" + "--------<br/>" + "Customer Name: " + email.name + "<br/>" + "Customer Email: " + email.customer_email + "<br/>" + extras + "<br/>--------"
            message = MessageSchema(
                subject = email.subject,
                recipients = email.email,
                body = email.message,
                subtype="html"
            )
            
            conf = self.emailConfig()
            print(f"EMAIL CONFIG {conf}")
            fa = FastMail(conf)
            await fa.send_message(message)

            return {"message": "Email sent successfully"}
        except Exception as e:
            print("EMAIL ERROR")
            print(e)
            import traceback
            traceback.print_exc()
            return {"message": f"Error sending email: {str(e)}"}

    def sendEmailBackground(self, email: EmailDTO):
        try:
            asyncio.create_task(self.sendEmail(email))
            return {"message": "Email sent successfully"}
        except Exception as e:
            print("EMAIL ERROR")
            print(e)
            import traceback
            traceback.print_exc()
            return {"message": f"Error sending email: {str(e)}"}
    
    def sendEmailExtraBackground(self, email: EmailExtraDTO):
        try:
            extra_params: str = extra_params_to_string(email.extra_params)
            extra_params = extra_params
            email_dto: EmailDTO = to_email_dto(email)
            asyncio.create_task(self.sendEmail(email_dto, extras = extra_params))
            return {"message": "Email sent successfully"}
        except Exception as e:
            print("EMAIL ERROR")
            print(e)
            import traceback
            traceback.print_exc()
            return {"message": f"Error sending email: {str(e)}"}
    
    def contactThroughEmailBackground(self, email: EmailExtraDTO):
        import resend
        #import os
        try:
            smtp_config = self.load_smtp_config()
            resend.api_key = smtp_config.get("RESEND_API_KEY")
            #resend.api_key = os.getenv("RESEND_API_KEY")

            extra_params: str = extra_params_to_string(email.extra_params)
            extra_params = extra_params
            email_dto: EmailDTO = to_email_dto(email)
            #asyncio.create_task(self.sendEmail(email_dto, extras = extra_params))

            email_dto.message = email_dto.message + "<br/><br/>" + "--------<br/>" + "Customer Name: " + email_dto.name + "<br/>" + "Customer Email: " + email_dto.customer_email + "<br/>" + extra_params + "<br/>--------"

            html = (
                    email_dto.message
                )

            params = {
                "from": f'{smtp_config["RESEND_FROM_NAME"]} <{smtp_config["RESEND_FROM_EMAIL"]}>',
                "to": [smtp_config["RESEND_TO_EMAIL"]],
                "reply_to": email.customer_email,
                "subject": email.subject,
                "html": html
            }

            response = resend.Emails.send(params)
            print(f"Resend API response: {response}")
            
            return {"message": "Email sent successfully"}
        except Exception as e:
            print("EMAIL ERROR")
            print(e)
            import traceback
            traceback.print_exc()
            return {"message": f"Error sending email: {str(e)}"}