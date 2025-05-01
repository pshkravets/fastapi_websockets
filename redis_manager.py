from redis.asyncio import Redis
from config import REDIS_CHANNEL, REDIS_CLIENTS_KEY, REDIS_HOST, REDIS_PORT


class RedisManager:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.clients_key = REDIS_CLIENTS_KEY
        self.channel = REDIS_CHANNEL

    async def increment_clients(self):
        await self.redis.incr(self.clients_key)

    async def decrement_clients(self):
        await self.redis.decr(self.clients_key)

    async def get_client_count(self) -> int:
        count = await self.redis.get(self.clients_key)
        return int(count) if count else 0

    async def publish(self, message: str):
        await self.redis.publish(self.channel, message)

    async def subscribe(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.channel)
        return pubsub

    async def close(self):
        await self.redis.close()
