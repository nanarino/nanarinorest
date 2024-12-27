"""
密码散列工具

https://github.com/pyca/bcrypt/issues/684#issuecomment-1902590553
"""

import bcrypt


def eq(plain_password: str, hashed_password: bytes) -> bool:
    """前者散列后是否等于后者"""
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password)


def hash(password: str) -> bytes:
    """散列"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)
