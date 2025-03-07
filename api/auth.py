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

oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/signin')


async def current(token: str = Depends(oauth2)):
    """依赖项 获取当前用户id和用户名 失败401"""
    try:
        decode_user = schemas.auth_token_data(**jwt.decode(token))
    except ValidationError:
        raise HTTPException(
            status_code=401,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return decode_user


@auth.post(
    '/auth/signin',
    summary='授权登录',
    dependencies=[Depends(RateLimiter(times=1, seconds=5))],
    description='频率限制5秒1次',
)
async def sign_in(
    form: OAuth2PasswordRequestForm = Depends(), dbs: AsyncSession = Depends(db_session)
) -> schemas.auth_res:
    select_exec = select(User).where(User.username == form.username)
    _user = (await dbs.execute(select_exec)).scalars().first()
    if (_user is None) or not pwd.eq(form.password, _user.password):
        raise HTTPException(status_code=403, detail='Incorrect username or password')
    access_token = jwt.encode(
        schemas.auth_token_data(uid=_user.id, uname=_user.username).model_dump()
    )
    return schemas.auth_res(access_token=access_token)


@auth.post(
    '/auth/signup',
    summary='注册用户',
    dependencies=[Depends(RateLimiter(times=1, seconds=5))],
    description='频率限制5秒1次',
)
async def sign_up(
    form: OAuth2PasswordRequestForm = Depends(), dbs: AsyncSession = Depends(db_session)
) -> schemas.auth_res:
    select_exec = select(User).where(User.username == form.username)
    async with dbs.begin():
        if (await dbs.execute(select_exec)).scalars().first() is not None:
            raise HTTPException(status_code=403, detail='The username already exists')
        hashed_pwd = pwd.hash(form.password)
        new_user = User(username=form.username, password=hashed_pwd)
        dbs.add(new_user)
        await dbs.flush()
        access_token = jwt.encode(
            schemas.auth_token_data(uid=new_user.id, uname=form.username).model_dump()
        )
        await dbs.commit()
    return schemas.auth_res(access_token=access_token)


@auth.get(
    '/auth/current',
    summary='获取当前用户',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
    description='频率限制1秒1次',
)
async def get_current_user(
    cu: schemas.auth_token_data = Depends(current),
) -> schemas.auth_token_data:
    return cu
