"""card系列api"""
from fastapi import APIRouter, HTTPException, Depends
from db import db_session, AsyncSession
from db.models import Card, Card_bindinfo
from sqlalchemy import select
from . import schemas
from fastapi_limiter.depends import RateLimiter
from .auth import current


claim = APIRouter()

@claim.get('/claims',
          summary="获取本卡的理赔列表",
          dependencies=[Depends(RateLimiter(times=1, seconds=1))],
          description="需要验证登录，频率限制1秒1次"
          )
async def get_card_claimslist(
    cu: schemas.auth_token_data = Depends(current),
    dbs: AsyncSession = Depends(db_session)
):
    # 未实现
    return []