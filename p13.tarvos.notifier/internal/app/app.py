from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.config import events, settings
from internal.controller.amqp.router import rpc_router
from pkg.rabbitmq.rpc import RPCClient, RPCServer


def create_app() -> FastAPI:  # noqa: WPS213
    app = FastAPI(
        title=settings.PROJECT_NAME,
        swagger_ui_parameters=settings.SWAGGER_UI_PARAMETERS
    )
    server = RPCServer(settings.RABBITMQ_URI)
    client = RPCClient(settings.RABBITMQ_URI, app.state)

    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin)
                for origin in settings.CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    server.include_router(rpc_router, prefix=settings.RPC)

    app.add_event_handler(settings.STARTUP, events.startup_rpc_server(server))
    app.add_event_handler(settings.STARTUP, events.startup_rpc_client(client))
    app.add_event_handler(settings.SHUTDOWN, events.shutdown_rpc_client(client))

    return app
