from pydantic import BaseModel, EmailStr


class MailSend(BaseModel):

    recipients: list[EmailStr] | None

    subject: str
    body: str
