import asyncio
import signal
from logger import logger
from connection_manager import ConnectionManager
from redis_manager import RedisManager

shutdown_triggered = False


def setup_signal_handler(manager: ConnectionManager, redis_manager: RedisManager, *tasks) -> None:
    loop = asyncio.get_event_loop()

    async def safe_shutdown():
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await redis_manager.close()

    async def shutdown_after_delay() -> None:
        logger.info('SIGINT/SIGTERM received. Waiting up to 30 minutes for clients to disconnect...')
        for seconds in range(1800):
            count = await manager.client_count()
            if count < 1:
                logger.info('No active clients. Shutting down now.')
                await redis_manager.close()
                await safe_shutdown()
                loop.stop()
            logger.info(f'{count} clients active. {1800 - seconds} seconds remaining until forced shutdown.')
            await asyncio.sleep(1)
        logger.info('Timeout reached. Shutting down.')
        await redis_manager.close()
        await safe_shutdown()
        loop.stop()

    def handler(signum, frame):
        nonlocal loop
        global shutdown_triggered
        if not shutdown_triggered:
            shutdown_triggered = True
            loop.create_task(shutdown_after_delay())

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)