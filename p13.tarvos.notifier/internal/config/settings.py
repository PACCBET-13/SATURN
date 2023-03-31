from typing import Any

from fastapi_mail import ConnectionConfig
from pydantic import (
    AmqpDsn,
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    validator
)


class Settings(BaseSettings):

    API: str = '/api'
    RPC: str = '/rpc'
    STARTUP: str = 'startup'
    SHUTDOWN: str = 'shutdown'

    PROJECT_NAME: str = 'Tarvos Notifier'
    PROJECT_DESCRIPTION: str = 'Tarvos Notifier'
    PROJECT_VERSION: str = '0.0.1'

    SWAGGER_UI_PARAMETERS: dict[str, bool] = {
        'displayRequestDuration': True,
        'filter': True
    }

    CORS_ORIGINS: list[AnyHttpUrl] = []

    RABBITMQ_HOST: str
    RABBITMQ_PORT_INTERNAL: str
    RABBITMQ_NAME: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_URI: AmqpDsn | None = None

    @validator('RABBITMQ_URI', pre=True)
    def assemble_rabbitmq_connection(
        cls, value: str | None, values: dict[str, Any]
    ) -> str:
        if isinstance(value, str):
            return value

        return AmqpDsn.build(
            scheme='amqp',
            user=values.get('RABBITMQ_USER'),
            password=values.get('RABBITMQ_PASSWORD'),
            host=values.get('RABBITMQ_HOST'),
            port=values.get('RABBITMQ_PORT_INTERNAL'),
            path='/{0}'.format(values.get('RABBITMQ_NAME')),
        )

    SMTP_USERNAME: EmailStr
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_FROM_NAME: str
    SMTP_STARTTLS: bool = False
    SMTP_SSL_TLS: bool = True
    SMTP_CONFIG: ConnectionConfig | None = None

    @validator('SMTP_CONFIG', pre=True)
    def assemble_smtp_connection(cls, _: None, values: dict[str, Any]) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_FROM=values.get('SMTP_USERNAME'),
            MAIL_FROM_NAME=values.get('SMTP_FROM_NAME'),
            MAIL_USERNAME=values.get('SMTP_USERNAME'),
            MAIL_PASSWORD=values.get('SMTP_PASSWORD'),
            MAIL_SERVER=values.get('SMTP_SERVER'),
            MAIL_PORT=values.get('SMTP_PORT'),
            MAIL_STARTTLS=values.get('SMTP_STARTTLS'),
            MAIL_SSL_TLS=values.get('SMTP_SSL_TLS')
        )


settings: Settings = Settings()
