"""密码散列工具"""
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def eq(pwd: str, hashed_pwd: str) -> bool:
    """前者散列后是否等于后者"""
    return crypt_context.verify(pwd, hashed_pwd)


def hash(pwd: str) -> str:
    """散列"""
    return crypt_context.hash(pwd)
