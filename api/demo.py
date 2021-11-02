"""demo系列api"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from db import db_session, AsyncSession
from db.models import Demo
from sqlalchemy import func, select
from . import schemas
from fastapi_limiter.depends import RateLimiter

demo = APIRouter(tags=["demo"])  # 和文件名一样方便导出


@demo.get('/demo/{id}',
          response_model=Optional[schemas.demo],
          summary="指定获取"
          )
async def get_demo(id: int, dbs: AsyncSession = Depends(db_session)):
    return await dbs.get(Demo, id)


@demo.get('/demos',
          response_model=schemas.demos_sliced,
          summary="分页获取",
          dependencies=[Depends(RateLimiter(times=5, seconds=1))],
          description="limit限制5到20之间，offset限制不小于0，频率限制一秒5次"
          )
async def get_demo_list(
    limit: int = Query(5, ge=5, le=20),  # 5 <= limit <= 20
    offset: int = Query(0, ge=0),  # offset >= 0
    dbs: AsyncSession = Depends(db_session)
):
    # 总数据条数
    total_orm = select(func.count(Demo.id))
    total: int = (await dbs.execute(total_orm)).scalar()
    # 分页数据
    slice_data_orm = select(Demo).order_by(Demo.id).limit(limit).offset(offset)
    slice_data: list[schemas.demo] = (await dbs.execute(slice_data_orm)).scalars().all()
    return {"total": total, "slice_data": slice_data}
