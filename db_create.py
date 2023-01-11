"""创建空数据表"""

import db
import asyncio


async def test_create_all():
    """异步引擎db.async_egn无法直接使用db.metadata.create_all():

        AttributeError: 'AsyncEngine' object has no attribute '_run_ddl_visitor'
    """
    async with db.async_egn.begin() as conn:
        await conn.run_sync(db.metadata.create_all)


async def test_get_create_ddl():
    '''如果无法自动创建, 可用以下代码生成创建表的SQL语句, 修改为所需方言再运行'''
    import inspect

    for name, table in inspect.getmembers(db.models, inspect.isclass):
        if (node := inspect.getmodule(table)) is not None:
            if node.__name__ == 'db.models':
                print(table.__ddl__())


async def main():
    """
        使用`asyncio.run`结束时抛出`RuntimeError: Event loop is closed`
        是Windows平台上常见且可以忽略的异常
    """
    # await test_create_all()
    await test_get_create_ddl()

asyncio.run(main())
