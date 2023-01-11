"""数据库连接测试"""
import asyncio
from sqlalchemy import select, insert
from db.models import Demo
from db import async_session_local


async def test_select():
    async with async_session_local() as session:
        async with session.begin():
            _orm = select(Demo).where(Demo.id == 1)
            result: Demo = (await session.execute(_orm)).scalars().first()
            print(dict(result))


async def test_select_by_pk(pk):
    async with async_session_local() as session:
        async with session.begin():
            if (result := await session.get(Demo, pk)) is not None:
                print(dict(result))


async def test_insert(name='插入测试'):
    async with async_session_local() as session:
        async with session.begin():
            _orm = insert(Demo).values(name=name)
            await session.execute(_orm)
            await session.commit()


async def main():
    """
        使用`asyncio.run`结束时抛出`RuntimeError: Event loop is closed`
        是Windows平台上常见且可以忽略的异常
    """
    await test_select()
    await test_select_by_pk(2)
    await test_insert()

asyncio.run(main())
