'''使用sqlalchemy连接关系型数据库

包括：
- 已配置的异步引擎 `async_egn` 
- 已配置的会话元类 `async_session_local` 和生成器 `db_session` 
- 数据库模型 `models` 

额外:
- 异步Redis实例 `redis` 

'''
from .base import metadata
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from . import models
from typing import Callable, AsyncGenerator
import redis.asyncio as aioredis

__all__ = ['async_egn', 'async_session_local',
           'db_session', 'metadata', 'models', "AsyncSession", "redis"]

# 读取配置文件
from pathlib import Path
from configparser import ConfigParser
ini = ConfigParser()
ini.read(Path.cwd() / Path('config.ini'), encoding='utf8')
cfg = ini['db']

# 数据库引擎，默认的连接池
async_egn = create_async_engine(
    cfg.get('mysql'),
    pool_recycle=cfg.getint('recycle', 7200)
)

# 创建session元类
async_session_local: Callable[..., AsyncSession] = sessionmaker(
    class_=AsyncSession,
    autocommit=cfg.getboolean('autocommit', False),
    autoflush=cfg.getboolean('autoflush', False),
    bind=async_egn
)  # type: ignore


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    '''session生成器 作为fastapi的Depends选项'''
    async with async_session_local() as session:
        yield session

# 创建异步redis实例，默认的连接池
redis = aioredis.from_url(cfg.get('redis'), encoding="utf8")
