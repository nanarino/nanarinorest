# nanarinorest

自用 restful api demo



## 环境

- python 3.9

  ```python
  # pip install
  
  # ASGI服务
  uvicorn
  fastapi
  # 异步ORM操作mysql
  sqlalchemy
  aiomysql
  # Oauth2授权
  python-jose[cryptography]
  python-multipart
  passlib
  bcrypt
  # 异步Redis存取
  aioredis
  hiredis
  # 接口频率限制 从pip下载的库有bug，用git拉取的正常
  # 见 https://github.com/long2ice/fastapi-limiter/issues/18#issuecomment-955888999
  fastapi-limiter
  ```

- mysql 5.7

- redis 5+

## 目录

```python
/nanarino/nanarinorest # cwd
│
├── app.py             # 程序入口
├── config.ini         # 配置文件
├── api
│   ├── __init__.py
│   ├── auth.py        # Oauth2授权认证 登录以及注册api
│   ├── schemas.py     # 类型检查以及生成文档所需类型声明
│   └── ...            # 其他api 子路由等文件
├── db
│   ├── __init__.py
│   ├── base.py        # ORM mapper基类以及收集的数据元
│   └── models.py      # 数据库模型
├── util               # 封装的工具包
├── ...                # 测试脚本，静态资源等
└── requirements.txt   # pip安装的模块
```

