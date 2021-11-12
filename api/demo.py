"""demo系列api"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from db import db_session, AsyncSession
from db.models import Demo
from sqlalchemy import func, select
from . import schemas
#from fastapi_limiter.depends import RateLimiter # demo接口不限制频率

demo = APIRouter(tags=["demo"])  # 和文件名一样方便导出


@demo.get('/demo/{id}', response_model=Optional[schemas.demo], summary="指定获取单条")
async def get_demo(id: int, dbs: AsyncSession = Depends(db_session)):
    return await dbs.get(Demo, id)


@demo.post('/demo', summary="新增单条")
async def create_demo(data: schemas.demo_create, dbs: AsyncSession = Depends(db_session)):
    new_demo = Demo(create_at=datetime.now(), is_active=1, **data.dict())
    dbs.add(new_demo)
    await dbs.flush()
    await dbs.commit()
    return {"msg": "新增成功"}


@demo.delete('/demos', summary="删除指定多条")
async def del_demos(data: schemas.del_data, dbs: AsyncSession = Depends(db_session)):
    _orm = select(Demo).where(Demo.id.in_(data.id_set))
    demos_qs: list[Demo] = (await dbs.execute(_orm)).scalars().all()
    for d in demos_qs:
        d.is_active = 0
    await dbs.flush()
    await dbs.commit()
    return {"msg": "删除成功"}


@demo.put('/demo', summary="修改单条")
async def update_demo(data: schemas.demo_update, dbs: AsyncSession = Depends(db_session)):
    _orm = select(Demo).where(Demo.id == data.id)
    this_demo: Demo = (await dbs.execute(_orm)).scalars().first()
    for k, v in data.dict().items():
        if k == "id":
            pass
        setattr(this_demo, k, v)
    await dbs.flush()
    await dbs.commit()
    return {"msg": "更新成功"}


@demo.get('/demos', response_model=schemas.demos_sliced, summary="分页获取多条")
async def get_demos(
    limit: int = Query(5, ge=5, le=100),  # limit 5~100
    offset: int = Query(0, ge=0),         # offset >= 0
    dbs: AsyncSession = Depends(db_session)
):
    # 总数据条数
    total_orm = select(func.count(Demo.id))
    total: int = (await dbs.execute(total_orm)).scalar()
    # 分页数据
    slice_data_orm = select(Demo).where(Demo.is_active == 1).order_by(
        Demo.id).limit(limit).offset(offset)
    slice_data: list[Demo] = (await dbs.execute(slice_data_orm)).scalars().all()
    return {"total": total, "slice_data": slice_data}
