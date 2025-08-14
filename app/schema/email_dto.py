from pydantic import BaseModel, EmailStr

class Email(BaseModel):
    email: list[EmailStr]
    subject: str
    message: str