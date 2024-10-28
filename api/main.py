from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# 配置允许的来源
origins = [
    "*",  # 本地主机开发
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,  # 允许凭证
    allow_methods=["*"],  # 允许方法
    allow_headers=["*"],  # 允许头
)


@app.get("/")
def hello():
    return {"message": "欢迎来到魔方AI推荐1"}
@app.get("/api/recommended")
async def recommended():
    return {"message": "欢迎来到魔方AI推荐2"}
