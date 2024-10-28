from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from ai_config import Config

# 定义模板
template = """
    Question: {question}
    已检索到的相关信息: 
    {context}
    Answer: Let's think step by step.
    请用简体中文回复。
    """


def ask_question_with_llama(template:str, params, model="llama3.2:1b"):
     # 创建 ChatPromptTemplate 实例
    prompt = ChatPromptTemplate.from_template(template)
    # 使用本地部署的 llama3.1 模型
    model = OllamaLLM(model=model, base_url=Config.OLLAMA.get('url'))
    # 创建链，定义数据流
    chain = prompt | model
    # 执行链，传递实际提问
    result = chain.invoke(params)
    # 返回模型生成的回答
    return result

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
    answer = ask_question_with_llama(template=template, params={"question": '我叫什么名字', 'context': '我叫吴佳雷'})
    return {"answer": answer}
    return generate_response(answer = answer, question=question)
