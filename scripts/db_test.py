"""数据库连接测试"""

import asyncio
from sqlalchemy import select, insert
from db.models import Demo
from db import async_session_local


async def test_insert(row: dict = {'name': '測試', 'type': '測試', 'mark': '測試'}):
    async with async_session_local() as session:
        async with session.begin():
            _exec = insert(Demo).values(row)
            await session.execute(_exec)
            await session.commit()


async def test_select_first():
    async with async_session_local() as session:
        async with session.begin():
            _exec = select(Demo).where(Demo.id == 1)
            result = (await session.execute(_exec)).scalar()
            if result:
                print(dict(result))


async def test_select_by_pk(pk: int):
    async with async_session_local() as session:
        async with session.begin():
            if (result := await session.get(Demo, pk)) is not None:
                print(dict(result))


async def test_select_top(n: int):
    async with async_session_local() as session:
        async with session.begin():
            _exec = select(Demo).limit(n)
            result = (await session.execute(_exec)).scalars().all()
            print(list(map(dict, result)))


async def main():
    """
    使用 `asyncio.run` 结束时抛出 `RuntimeError: Event loop is closed` 是Windows平台上常见且可以忽略的异常
    """
    await test_insert()
    await test_insert()
    await test_select_first()
    await test_select_by_pk(2)
    await test_select_top(10)


if __name__ == '__main__':
    asyncio.run(main())
