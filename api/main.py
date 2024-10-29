from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from ai_utils import getConfig
from ai_ollama import ask_question_with_ollama

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

ollamaModel = getConfig('ollama.model')
ollamaUrl = getConfig('ollama.url')

print(ollamaUrl, 'ollamaModel', ollamaModel)

# 定义模板
template = """
    Question: {question}
    已检索到的相关信息: 
    {context}
    Answer: Let's think step by step.
    请用简体中文回复。
    """

## 健康检查
@app.get("/")
def healthz():
    return {"status": "ok", "code": 200}

## 健康检查
@app.get("/healthz")
def healthz():
    return Response(content="OK", media_type="text/plain")

@app.get("/api")
def api():
    answer = ask_question_with_ollama(template=template, params={"question": '我叫什么名字', 'context': '我叫吴佳雷'}, model=ollamaModel)
    return {"answer": answer}

