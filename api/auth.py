from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Form
from . import schemas
from db import db_session, AsyncSession
from db.models import Card
from util import jwt, pwd, captcha
from sqlalchemy import select
from pydantic import ValidationError
from fastapi_limiter.depends import RateLimiter

auth = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/_signin")


async def current(token: str = Depends(oauth2)):
    """依赖项 获取当前用户id和用户名 失败401"""
    try:
        dcd_user = schemas.auth_token_data(**jwt.dcd(token))
    except ValidationError:
        raise HTTPException(
            status_code=401,
            detail="未提供已授权登录的令牌",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return dcd_user


@auth.post("/auth/signin",
           response_model=schemas.auth_res,
           summary='授权登入卡号',
           dependencies=[Depends(RateLimiter(times=1, seconds=5))],
           description="频率限制5秒1次，需要先请求验证图片，接口文档受限无法请求"
           )
async def sign_in(
    form: OAuth2PasswordRequestForm = Depends(),
    dbs: AsyncSession = Depends(db_session),
    captcha_token: str = Form(...),
    captcha_key: str = Form(...)
):
    try:
        captcha_key_dcd: str = jwt.dcd(captcha_token)["captcha_key"]
    except KeyError:
        raise HTTPException(
            status_code=403, detail="验证码已过期")
    if not (captcha_key.lower() == captcha_key_dcd.lower()):
        raise HTTPException(
            status_code=403, detail="验证码错误")
    select_orm = select(Card).where(Card.username == form.username)
    _user = (await dbs.execute(select_orm)).scalars().first()
    if (_user is None) or not pwd.eq(form.password, _user.password):
        raise HTTPException(
            status_code=403, detail="卡号或者密码错误")
    access_token = jwt.ecd(schemas.auth_token_data(
        cid=_user.id,
        uname=_user.username
    ).dict())
    return {"access_token": access_token}


@auth.post("/auth/_signin",
           response_model=schemas.auth_res,
           summary='授权登入卡号（接口文档测试用）',
           dependencies=[Depends(RateLimiter(times=1, seconds=5))],
           description="频率限制5秒1次，无需验证图片，接口文档专用测试接口"
           )
async def sign_in(
    form: OAuth2PasswordRequestForm = Depends(),
    dbs: AsyncSession = Depends(db_session)
):
    select_orm = select(Card).where(Card.username == form.username)
    _user = (await dbs.execute(select_orm)).scalars().first()
    if (_user is None) or not pwd.eq(form.password, _user.password):
        raise HTTPException(
            status_code=403, detail="卡号或者密码错误")
    access_token = jwt.ecd(schemas.auth_token_data(
        cid=_user.id,
        uname=_user.username
    ).dict())
    return {"access_token": access_token}


@auth.post("/auth/signup",
           response_model=schemas.auth_res,
           summary='注册卡号',
           dependencies=[Depends(RateLimiter(times=1, seconds=5))],
           description="频率限制5秒1次"
           )
async def sign_up(
    form: OAuth2PasswordRequestForm = Depends(),
    dbs: AsyncSession = Depends(db_session)
):
    select_orm = select(Card).where(Card.username == form.username)
    if (await dbs.execute(select_orm)).scalars().first() is not None:
        raise HTTPException(
            status_code=412, detail="此卡号已被注册")
    hashed_pwd = pwd.hash(form.password)
    new_user = Card(username=form.username, password=hashed_pwd, is_active=0)
    dbs.add(new_user)
    await dbs.flush()
    access_token = jwt.ecd(schemas.auth_token_data(
        cid=new_user.id,
        uname=form.username
    ).dict())
    await dbs.commit()
    return {"access_token": access_token}


@auth.get("/auth/current",
          response_model=schemas.auth_token_data,
          summary='获取当前登入的卡号',
          dependencies=[Depends(RateLimiter(times=1, seconds=1))],
          description="频率限制1秒1次"
          )
async def get_current_user(cu: schemas.card = Depends(current)): return cu


@auth.get("/auth/captcha",
          response_model=schemas.auth_captcha,
          summary='请求获取人机图片验证',
          dependencies=[Depends(RateLimiter(times=1, seconds=3))],
          description="频率限制3秒1次"
          )  # 生成验证码内部不是异步IO 所以用同步函数防止出问题
def get_captcha():
    captcha_key, captcha_img = captcha.create_img()
    token = jwt.ecd({'captcha_key': captcha_key}, timeout=2)
    return {'captcha_token': token, 'captcha_img': captcha_img}
