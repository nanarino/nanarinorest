from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from . import schemas
from db import db_session, AsyncSession
from db.models import User
from util import jwt, pwd
from sqlalchemy import select
from pydantic import ValidationError
from fastapi_limiter.depends import RateLimiter

auth = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/signin")


async def current(token: str = Depends(oauth2)):
    """依赖项 获取当前用户id和用户名 失败401"""
    try:
        dcd_user = schemas.auth_token_data(**jwt.dcd(token))
    except ValidationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return dcd_user


@auth.post("/auth/signin",
           response_model=schemas.auth_res,
           summary='授权登录',
           dependencies=[Depends(RateLimiter(times=1, seconds=5))],
           description="频率限制5秒1次"
           )
async def sign_in(
    form: OAuth2PasswordRequestForm = Depends(),
    dbs: AsyncSession = Depends(db_session)
):
    select_orm = select(User).where(User.username == form.username)
    _user = (await dbs.execute(select_orm)).scalars().first()
    if (_user is None) or not pwd.eq(form.password, _user.password):
        raise HTTPException(
            status_code=403, detail="Incorrect username or password")
    access_token = jwt.ecd(schemas.auth_token_data(
        uid=_user.id,
        uname=_user.username
    ).dict())
    return {"access_token": access_token}


@auth.post("/auth/signup",
           response_model=schemas.auth_res,
           summary='注册用户',
           dependencies=[Depends(RateLimiter(times=1, seconds=5))],
           description="频率限制5秒1次"
           )
async def sign_up(
    form: OAuth2PasswordRequestForm = Depends(),
    dbs: AsyncSession = Depends(db_session)
):
    select_orm = select(User).where(User.username == form.username)
    if (await dbs.execute(select_orm)).scalars().first() is not None:
        raise HTTPException(
            status_code=403, detail="The username already exists")
    hashed_pwd = pwd.hash(form.password)
    new_user = User(username=form.username, password=hashed_pwd)
    dbs.add(new_user)
    await dbs.flush()
    access_token = jwt.ecd(schemas.auth_token_data(
        uid=new_user.id,
        uname=form.username
    ).dict())
    await dbs.commit()
    return {"access_token": access_token}


@auth.get("/auth/current",
          response_model=schemas.auth_token_data,
          summary='获取当前用户',
          dependencies=[Depends(RateLimiter(times=1, seconds=1))],
          description="频率限制1秒1次"
          )
async def get_current_user(cu: schemas.auth_token_data = Depends(current)): return cu
