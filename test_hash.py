"""hash测试"""
from util import pwd

pwd_hashed = pwd.hash('123456')

print(pwd_hashed)

print(pwd.eq('123456',pwd_hashed))