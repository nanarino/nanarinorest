from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api
import redis.asyncio as aioredis
from fastapi_limiter import FastAPILimiter
import db


app = FastAPI(title='LLTS',description='由于OAuth2规范，授权表单字段强制使用username和password,所以用username表示卡号')


@app.on_event("startup")
async def startup():
    # 初始化FastAPILimiter 用来限制api请求频率 默认返回429错误
    redis = aioredis.from_url(db.cfg.get('redis'), encoding="utf8")
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
app.include_router(api.auth, tags=["auth"])
app.include_router(api.card, tags=["card"])
app.include_router(api.claim, tags=["claim"])


if __name__ == '__main__':
    import os
    os.system('')
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
