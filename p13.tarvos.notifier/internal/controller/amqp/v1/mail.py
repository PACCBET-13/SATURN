from typing import Any

from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import ValidationError

from internal.config.settings import settings
from internal.dto.mail import MailSend
from pkg.rabbitmq.rpc import RPCRouter


router = RPCRouter()


@router.procedure('/send', durable=True, auto_delete=True)
async def send_mail(**kwargs: dict[str, Any]) -> None:
    try:
        dto = MailSend(**kwargs)
    except ValidationError as ex:
        raise Exception(str(ex))  # noqa: WPS454

    if not dto.recipients:
        return

    mail = FastMail(settings.SMTP_CONFIG)
    await mail.send_message(MessageSchema(
        recipients=dto.recipients,
        subject=dto.subject,
        body=dto.body,
        subtype=MessageType.plain
    ))
