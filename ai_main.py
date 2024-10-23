from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_ollama import AiOllamaClassifier
from ai_analyze_prompt import get_analyze_context_by_type_prompt, get_context_prompt
from typing import Optional
from ai_utils import xml_to_json

app = FastAPI()


#获取推荐
@app.get("/api/recommended")
async def recommended(question: Optional[str] = None):

    # 调用外部 Ollama API
    handle = AiOllamaClassifier()
    typeRes = handle.classify_question_type(
        get_context_prompt(question)
    )
    typeJson = xml_to_json(typeRes)
    type = int(typeJson['type'])
    extRes = handle.classify_question_type(
        get_analyze_context_by_type_prompt(type = type, question=question)
    )
    extJson = xml_to_json(extRes)
    if type == 5:
        return {'question': question, "response": (f"""
            {extJson.get('content_title', '')}
            {extJson.get('content_desc', '')}
            {extJson.get('content_note', '')}
            """)}
    else:
        #尝试从向量数据库中排查数据
        return {'question': question, 'typeJson': typeJson, 'type': type, 'extJson': extJson}

# 启动应用
# uvicorn main:app --reload

