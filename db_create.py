"""创建空数据表

异步引擎db.async_egn无法直接使用db.metadata.create_all():
AttributeError: 'AsyncEngine' object has no attribute '_run_ddl_visitor'


如果无法自动创建, 可用以下代码生成创建表的SQL语句, 修改为所需方言再运行
```
    import inspect

    for name, table in inspect.getmembers(db.models, inspect.isclass):
        if inspect.getmodule(table).__name__ == 'db.models':
            print(table.__ddl__())
```

asyncio.run 报错RuntimeError: Event loop is closed 是正常现象
"""

import db
import asyncio


async def main():
    async with db.async_egn.begin() as conn:
        await conn.run_sync(db.metadata.create_all)

asyncio.run(main()) 
