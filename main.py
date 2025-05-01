import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
from shutdown_handler import setup_signal_handler
from redis_manager import RedisManager


app = FastAPI()

redis_manager = RedisManager()
connection_manager = ConnectionManager(redis_manager)


@app.websocket('/ws')
async def notifications(websocket: WebSocket) -> None:
    await websocket.accept()
    await connection_manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await connection_manager.publish_message(message)
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)


@app.on_event('startup')
async def startup():
    broadcast_task = asyncio.create_task(connection_manager.test_message_broadcast())
    redis_task = asyncio.create_task(connection_manager.redis_listener())
    setup_signal_handler(connection_manager, redis_manager, broadcast_task, redis_task)
