# nanarinorest

自用 restful api demo



## 环境

- python3.9
- mysql5.7

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

