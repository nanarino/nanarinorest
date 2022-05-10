from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api
import aioredis
from fastapi_limiter import FastAPILimiter
import db


app = FastAPI(title='nanarinorest', description="""
    * Oauth2授权强制字段名使用username和password，且规定请求使用application/x-www-form-urlencoded
""")


@app.on_event("startup")
async def startup():
    # 初始化FastAPILimiter 用来限制api请求频率 默认返回429错误
    redis = await aioredis.from_url(db.cfg.get('redis'), encoding="utf8")
    await FastAPILimiter.init(redis)


@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()


# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册路由
app.include_router(api.demo)
app.include_router(api.auth, tags=["auth"])


if __name__ == '__main__':
    import os
    os.system('')
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8080) 
    # WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
    uvicorn.run(app="app:app", host="0.0.0.0",port=8080, reload=True, debug=True)

    # ERROR:    [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。
    # 意味着端口号可能被占用
