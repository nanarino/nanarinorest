"""demo系列api"""

from datetime import datetime
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from db import db_session, AsyncSession
from db.models import Demo
from sqlalchemy import func, select
from . import schemas
# from fastapi_limiter.depends import RateLimiter # demo接口不限制频率

demo = APIRouter(tags=['demo'])  # 和文件名一样方便导出


@demo.get('/demo/{id}', summary='指定获取单条')
async def get_demo(
    id: int, dbs: AsyncSession = Depends(db_session)
) -> Optional[schemas.demo]:
    demo: Annotated = await dbs.get(Demo, id)
    return demo


@demo.post('/demo', summary='新增单条')
async def create_demo(
    data: schemas.demo_data, dbs: AsyncSession = Depends(db_session)
) -> Optional[schemas.msg]:
    new_demo = Demo(create_at=datetime.now(), is_active=1, **data.model_dump())
    async with dbs.begin():
        dbs.add(new_demo)
        await dbs.flush()  # flush后可以拿到新增的行的id
        id: int = new_demo.id
        await dbs.commit()
    return schemas.msg(msg='新增成功', id=id)


@demo.delete('/demos', summary='删除指定多条')
async def delete_demos(
    id: set[int] = Query(..., min_items=1, max_items=5),
    dbs: AsyncSession = Depends(db_session),
) -> Optional[schemas.msg]:
    async with dbs.begin():
        _exec = select(Demo).where(Demo.id.in_(id))
        demos_qs = (await dbs.execute(_exec)).scalars().all()
        for d in demos_qs:
            d.is_active = 0
        await dbs.commit()
    return schemas.msg(msg='删除成功')


@demo.put('/demo/{id}', summary='修改单条')
async def update_demo(
    id: int, data: schemas.demo_data, dbs: AsyncSession = Depends(db_session)
) -> Optional[schemas.msg]:
    async with dbs.begin():
        _exec = select(Demo).where(Demo.id == id)
        this_demo = (await dbs.execute(_exec)).scalars().first()
        if this_demo is None:
            raise HTTPException(status_code=404)
        for k, v in data.model_dump().items():
            setattr(this_demo, k, v)
        await dbs.commit()
    return schemas.msg(msg='更新成功')


@demo.get('/demos', summary='分页获取多条')
async def get_demos(
    limit: int = Query(5, ge=5, le=100),  # limit 5~100
    offset: int = Query(0, ge=0),  # offset >= 0
    dbs: AsyncSession = Depends(db_session),
) -> schemas.demos_sliced:
    # 总数据条数
    total_exec = select(func.count(Demo.id)).where(Demo.is_active == 1)
    total = (await dbs.execute(total_exec)).scalar() or 0
    # 分页数据
    slice_data_exec = (
        select(Demo)
        .where(Demo.is_active == 1)
        .order_by(Demo.id)
        .limit(limit)
        .offset(offset)
    )
    slice_result = (await dbs.execute(slice_data_exec)).scalars().all()
    slice_data: Annotated = list(map(dict, slice_result))
    return schemas.demos_sliced(total=total, slice_data=slice_data)
