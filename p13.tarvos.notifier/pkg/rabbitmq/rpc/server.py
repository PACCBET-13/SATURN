from typing import Type

import aio_pika
from aio_pika.patterns.rpc import JsonRPC

from pkg.rabbitmq.rpc import RPCRouter


class RPCServer(object):  # noqa: WPS230

    def __init__(self, url: str, rpc: Type[JsonRPC] = JsonRPC) -> None:
        self.url = url
        self.RPC = rpc
        self.router = RPCRouter()

    def set_event_loop(self, loop) -> None:
        self.loop = loop

    def include_router(self, router: RPCRouter, *, prefix: str = '') -> None:
        self.router.include_router(router, prefix=prefix)

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(
            self.url, loop=self.loop, client_properties={
                'connection_name': 'Read connection',
            },
        )
        self.channel = await self.connection.channel()
        self.rpc = await self.RPC.create(self.channel)

        for route in self.router.routes:
            await self.rpc.register(
                route['path'].lstrip('_'),
                route['endpoint'],
                **route['kwargs'],
            )
