'''数据库会话以及模型

包括 已配置的引擎 已配置的会话元类和生成器 数据库模型

'''
from .base import table, metadata
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from . import models
from typing import Callable, AsyncGenerator

__all__ = ['async_egn', 'async_session_local', 'db_session',
           'table', 'metadata', 'models', AsyncSession]

# 读取配置文件
from pathlib import Path
from configparser import ConfigParser
ini = ConfigParser()
ini.read(Path.cwd() / Path('config.ini'), encoding='utf8')
cfg = ini['db']

# 数据库引擎，也是连接池
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
)


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    '''session生成器 作为fastapi的Depends选项'''
    async with async_session_local() as session:
        yield session
