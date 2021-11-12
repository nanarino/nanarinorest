"""数据库连接测试"""
from threading import Thread
import asyncio
from sqlalchemy import select
from db.models import Card
from db import async_session_local


async def test_select():
    async with async_session_local() as session:
        _orm = select(Card).where(Card.id == 1)
        result: Card = (await session.execute(_orm)).scalars().first()
        print(dict(result))


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def end_loop(timeout=15):
    await asyncio.sleep(timeout)
    loop = asyncio.get_event_loop()
    loop.stop()

new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()
asyncio.run_coroutine_threadsafe(test_select(), new_loop)
asyncio.run_coroutine_threadsafe(end_loop(3), new_loop)
t.join()
