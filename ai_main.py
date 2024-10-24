from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_ollama import AiOllamaClassifier
from ai_analyze_prompt import get_analyze_context_by_type_prompt, get_context_prompt
from typing import Optional
from ai_utils import xml_to_json
from ai_milvus import MilvusDatabase
from ai_encode import encode_queries

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "欢迎来到魔方AI推荐"}


def buildFilter(params):
    filter=[]
    filters = None
    return filters
    

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
    vQuestions =encode_queries(questions=[question])
    print(len(vQuestions))
    collection_name='room_embeddings'
    vdb = MilvusDatabase()
    vdb.load_collection(collection_name)
    reps = vdb.search(
        collection_name=collection_name,
        data=vQuestions,
        anns_field="embedding",
        filter=buildFilter(extJson),
        output_fields=['room_unique_code', 'store_address', 'store_address', 'store_name'],
        limit=10,  # 返回前10条数据
    )
    vdb.close()
    #尝试从向量数据库中排查数据
    return {'question': question, 'typeJson': typeJson, 'type': type, 'extJson': extJson, 'resp': reps}

# 启动应用
# uvicorn main:app --reload

