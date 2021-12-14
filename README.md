# nanarinorest

自用 restful api demo 模板。

接口频率限制使用的是redis，自用不需要时可以砍掉这个功能，

需要删除入口文件app.py中挂载的startup和shutdown事件函数

---



## API demo

增删改查完备，生成的接口文档 http://127.0.0.1:8080/docs

- GET    /demo/{id}    指定获取单条
- PUT    /demo/{id}    修改指定单条
- POST    /demo    新增单条
- GET    /demos    分页获取多条
- DELETE    /demos    删除指定多条



## 环境

- python 3.9

  ```python
  # pip install
  
  # 数据接口类型
  pydantic
  
  # ASGI服务
  uvicorn
  fastapi
  
  # 异步ORM操作mysql
  sqlalchemy
  aiomysql
  
  # Oauth2授权以及散列
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


.demo_client           # web客户端demo
```

