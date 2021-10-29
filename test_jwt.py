"""jwt测试"""
import time
from util import jwt

# 生成token
token = jwt.ecd({"sub": '超级管理员', "uid": "ECAB"}, timeout=.1)
print(token)
print(jwt.dcd(token))
time.sleep(7)
print(jwt.dcd(token))
