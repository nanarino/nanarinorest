"""card系列api"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from db import db_session, AsyncSession
from db.models import Card, Card_bindinfo
from sqlalchemy import select
from . import schemas
from fastapi_limiter.depends import RateLimiter
from .auth import current


card = APIRouter()


@card.get('/card/{username}',
          response_model=Optional[schemas.card],
          summary="指定卡号获取卡是否被激活",
          dependencies=[Depends(RateLimiter(times=5, seconds=1))],
          description="频率限制1秒5次"
          )
async def get_card(username: str, dbs: AsyncSession = Depends(db_session)):
    _orm = select(Card).where(Card.username == username)
    result: Card = (await dbs.execute(_orm)).scalars().first()
    if result is not None:
        result.password = '******'
    return result


@card.put('/card/bindinfo',
          summary="覆盖更新本卡号的绑定信息",
          dependencies=[Depends(RateLimiter(times=1, seconds=1))],
          description="需要验证登录，频率限制1秒1次"
          )
async def create_card_bindinfo(
    bindinfo: schemas.card_bindinfo,
    cu: schemas.auth_token_data = Depends(current),
    dbs: AsyncSession = Depends(db_session)
):
    card: Card = await dbs.get(Card, cu.cid)
    if card is None:
        raise HTTPException(
            status_code=412, detail="此卡号不存在或已被注销")
    if card.is_active:
        raise HTTPException(
            status_code=412, detail="无法给已激活的卡号新增绑定")
    card_bindinfo = Card_bindinfo(cid=card.id, **bindinfo.dict())
    dbs.add(card_bindinfo)
    await dbs.flush()
    await dbs.commit()
    return {"msg": "覆盖绑定信息成功"}


@card.post('/card/active',
           summary="手动激活本卡",
           dependencies=[Depends(RateLimiter(times=1, seconds=1))],
           description="需要验证登录，频率限制1秒5次"
           )
async def card_active(
    cu: schemas.auth_token_data = Depends(current),
    dbs: AsyncSession = Depends(db_session)
):
    card: Card = await dbs.get(Card, cu.cid)
    if card is None:
        raise HTTPException(
            status_code=412, detail="此卡号不存在或已被注销")
    if card.is_active:
        raise HTTPException(
            status_code=412, detail="已激活的卡号")
    select_orm = select(Card_bindinfo).where(
        Card_bindinfo.cid == card.id).order_by(Card_bindinfo.id.desc())
    _user_bindinfo: Card_bindinfo = (await dbs.execute(select_orm)).scalars().first()
    if _user_bindinfo is None:
        raise HTTPException(
            status_code=412, detail="无法给还未绑定信息的卡激活")
    card.is_active = 1
    await dbs.flush()
    await dbs.commit()
    return {"msg": "手动激活本卡成功"}


@card.get('/card/bindinfo/',
          summary="获取本卡的绑定信息",
          response_model=schemas.card_bindinfo,
          dependencies=[Depends(RateLimiter(times=1, seconds=1))],
          description="需要验证登录，频率限制1秒1次，注意url末尾的`/`"
          )
async def get_card_bindinfo(
    cu: schemas.auth_token_data = Depends(current),
    dbs: AsyncSession = Depends(db_session)
):
    card: Card = await dbs.get(Card, cu.cid)
    if card is None:
        raise HTTPException(
            status_code=412, detail="此卡号不存在或已被注销")
    select_orm = select(Card_bindinfo).where(
        Card_bindinfo.cid == card.id).order_by(Card_bindinfo.id.desc())
    _user_bindinfo: Card_bindinfo = (await dbs.execute(select_orm)).scalars().first()
    if _user_bindinfo is None:
        raise HTTPException(
            status_code=412, detail="此卡未绑定信息")
    return _user_bindinfo


