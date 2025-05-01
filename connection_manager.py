import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
from redis_manager import RedisManager


class ConnectionManager:
    def __init__(self, redis_manager: RedisManager):
        self.connected_clients: Set[WebSocket] = set()
        self.redis_manager = redis_manager

    async def connect(self, websocket: WebSocket) -> None:
        self.connected_clients.add(websocket)
        await self.redis_manager.increment_clients()

    async def disconnect(self, websocket: WebSocket) -> None:
        self.connected_clients.discard(websocket)
        await self.redis_manager.decrement_clients()

    async def broadcast(self, message: str) -> None:
        coros = []
        for client in list(self.connected_clients):
            try:
                coros.append(client.send_text(message))
            except WebSocketDisconnect:
                await self.disconnect(client)
        await asyncio.gather(*coros, return_exceptions=True)

    async def client_count(self) -> int:
        return await self.redis_manager.get_client_count()

    async def test_message_broadcast(self) -> None:
        while True:
            await asyncio.sleep(10)
            if await self.client_count() > 0:
                await self.broadcast('Test broadcast message')

    async def publish_message(self, message: str) -> None:
        await self.redis_manager.publish(message)

    async def redis_listener(self):
        pubsub = await self.redis_manager.subscribe()
        async for message in pubsub.listen():
            if message['type'] == 'message':
                await self.broadcast(message['data'])
