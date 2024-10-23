"""令牌设置和读取模块"""

from jose import jwt as _jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, timezone
from pathlib import Path
from configparser import ConfigParser


# 读取配置文件
ini = ConfigParser()
ini.read(Path.cwd() / Path('config.ini'), encoding='utf8')
cfg = ini['auth']
TIMEOUT = cfg.getfloat('TIMEOUT', 1800.0)
KEY = cfg.get('KEY', '******')
ALGORITHM = cfg.get('ALGORITHM')
ISS = cfg.get('ISS', 'nanari')


def encode(data: dict, key: str = KEY, timeout: float = TIMEOUT) -> str:
    '''设置令牌  key参数默认读取配置文件

    data['exp'] 应由 timeout参数设置 | 配置文件设置 | 1800  （分钟） 

    '''
    return _jwt.encode(
        data | {"exp": datetime.now(timezone.utc) + timedelta(minutes=timeout),
                "iss": ISS},
        key,
        algorithm=ALGORITHM
    )


def decode(token: str, key: str = KEY) -> dict:
    '''读取令牌  key参数默认读取配置文件'''
    try:
        return _jwt.decode(token, key, algorithms=[ALGORITHM])
    except (ExpiredSignatureError, JWTError):
        # 过期或不可读取 返回空
        return dict()
