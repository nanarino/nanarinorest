# nanarinorest

自用 restful api demo 模板。

接口频率限制使用的是redis，自用不需要时可以砍掉这个功能， 需要删除入口文件app.py中挂载的startup和shutdown事件函数

---



## API demo

增删改查完备，生成的接口文档 http://127.0.0.1:8080/docs

- GET    /demo/{id}    指定获取单条
- PUT    /demo/{id}    修改指定单条
- POST    /demo    新增单条
- GET    /demos    分页获取多条
- DELETE    /demos    删除指定多条



## 环境

- python 3.9+
- mysql 5.7 （charset==utf8mb4）
- redis 5+

```bash

# 安装依赖
pip install -r requirements.txt

  #其中：
  fastapi-limiter
  # 从pip下载的库不是最新版本
  # 见 https://github.com/long2ice/fastapi-limiter/issues/18#issuecomment-955888999
  # 国内windows安装需要设置代理 命令：pip install git+https://github.com/long2ice/fastapi-limiter.git --proxy="https://127.0.0.1:7890" --user


# 配置好./config.ini后创建空的数据表
py db_create.py

# 运行项目
py app.py

```


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
│   └── demo.py        # 一组增删改查的 Demo api
├── db
│   ├── __init__.py
│   ├── base.py        # ORM mapper基类以及收集的数据元
│   └── models.py      # 数据库模型
├── util               # 封装的工具包
└── requirements.txt   # 依赖列表

│
demo_frontend          # 为 Demo api 编写的 Demo Frontend

```


---


## 运行前端

将app.py运行到127.0.0.1:8080后，运行与其对应的 demo前端

```bash

cd demo_frontend

py -m http.server 8081

```