"""数据库连接测试"""
from threading import Thread
import asyncio
from sqlalchemy import select, insert
from db.models import Demo
from db import async_session_local


async def test_select():
    async with async_session_local() as session:
        _orm = select(Demo).where(Demo.id == 1)
        result: Demo = (await session.execute(_orm)).scalars().first()
        print(dict(result))


async def test_select_by_pk():
    async with async_session_local() as session:
        if (result := await session.get(Demo, 2)) is not None:
            print(dict(result))


async def test_insert():
    async with async_session_local() as session:
        _orm = insert(Demo).values(name='插入测试')
        await session.execute(_orm)
        await session.commit()


async def test_insert_get_new_id_by_autocommit():
    async with async_session_local() as session:
        async with session.begin():# 配合session.flush()
            new_demo = Demo(name='test_insert_get_new_id_by_autocommit')
            session.add(new_demo)
            await session.flush()
            print(new_demo.id)

async def test_insert_get_new_id():
    async with async_session_local() as session:
        new_demo = Demo(name='test_insert_get_new_id')
        session.add(new_demo)
        await session.flush()
        print(new_demo.id)
        await session.commit()  # 不自动提交就得开启async with session.begin


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
asyncio.run_coroutine_threadsafe(test_insert_get_new_id(), new_loop)
asyncio.run_coroutine_threadsafe(test_insert_get_new_id_by_autocommit(), new_loop)
asyncio.run_coroutine_threadsafe(end_loop(3), new_loop)
t.join()
