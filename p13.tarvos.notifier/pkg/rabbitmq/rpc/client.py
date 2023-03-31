import asyncio
from typing import Type

import aio_pika
from aio_pika.patterns.rpc import JsonRPC
from fastapi.datastructures import State


class RPCClient(object):  # noqa: WPS230

    def __init__(
        self,
        url: str,
        state: State,
        rpc: Type[JsonRPC] = JsonRPC,
    ) -> None:
        self.url = url
        self.RPC = rpc
        self.state = state

    def set_event_loop(self, loop) -> None:
        self.loop = loop

    async def connect(self, **kwargs) -> JsonRPC:
        self.connection = await aio_pika.connect_robust(
            self.url, loop=self.loop, client_properties={
                'connection_name': 'Write connection',
            },
        )
        self.channel = await self.connection.channel()
        self.rpc = await self.RPC.create(self.channel, **kwargs)
        return self.rpc

    async def __aenter__(self) -> JsonRPC:
        self.set_event_loop(asyncio.get_event_loop())
        return await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rpc.close()
        await self.connection.close()
