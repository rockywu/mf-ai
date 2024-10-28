from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_ollama import AiOllamaClassifier
from ai_analyze_prompt import get_analyze_context_by_type_prompt, get_context_prompt
from typing import Optional
from ai_utils import xml_to_json
from ai_milvus import MilvusDatabase
from ai_encode import encode_queries
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal

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
    return {"message": "欢迎来到魔方AI推荐"}

def to_int(value):
    return int(value) if isinstance(value, str) and value.isdigit() else -1


def buildStoreFilter(params):
    print(params)
    filters = None
    return filters

def buildRoomFilter(params):
    minPrice = to_int(params['price_min'])
    maxPirce = to_int(params['price_max'])
    minArea = to_int(params['area_min'])
    maxArea = to_int(params['area_max'])
    filters = []
    if minPrice >= 0 and maxPirce >= 0:
        if minPrice == maxPirce:
            #附近附近查询
            minPrice = minPrice - minPrice/4
            maxPirce = maxPirce + maxPirce/4
        filters.append(f" price >= {minPrice} && price <= {maxPirce} ")
    if minArea >= 0 and maxArea >= 0:
        if minArea == maxArea:
            #附近附近查询
            minArea = minArea - minArea/4
            maxArea = maxArea + maxArea/4
        filters.append(f" area >= {int(minArea)} && area <= {int(maxArea)} ")
    return  " && ".join(filters) if len(filters) else None
    
    

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
        return {
            'code': 200,
            'type': type,
            'desc': typeJson['desc'],
            'question': question,
            "response": (f"""
                {extJson.get('content_title', '')}
                {extJson.get('content_desc', '')}
                {extJson.get('content_note', '')}
            """)
        }
    vQuestions =encode_queries(questions=[
        f"{extJson.get('origin')}",
    ])
    print(len(vQuestions), extJson)
    #type:1 查区域房源, type:2 查区域门店, type:3 查就近门店, type:4 查就近房源, type:5 未知类型
    search_params = {
        "metric_type": "L2", # 相似度度量方式，例如 L2、IP 或者 Cosine
        "params": {
            "nprobe":  200
        }
    }

    vdb = MilvusDatabase()
    if type == 2 or type == 3:
        #搜索门店
        print('查门店')
        collection_name='stores_embeddings'
        vdb.load_collection(collection_name)
        resp = vdb.search(
            collection_name=collection_name,
            data=vQuestions,
            anns_field="embedding",
            filter=buildStoreFilter(extJson),
            output_fields=['store_address', 'store_address', 'store_name', 'store_code', 'region_name'],
            limit=10,  # 返回前10条数据
            search_params=search_params
        )
        vdb.close()
    else:
        collection_name='room_embeddings'
        vdb.load_collection(collection_name)
        print(12312, buildRoomFilter(extJson))
        resp = vdb.search(
            collection_name=collection_name,
            data=vQuestions,
            anns_field="embedding",
            filter=buildRoomFilter(extJson),
            output_fields=[
                'room_unique_code',
                'room_type_code', 
                'store_address', 
                'store_address', 
                'store_name', 
                'store_code', 
                'region_name', 
                'long_term_type_name',
                'area',
                'price'
            ],
            limit=10,  # 返回前10条数据
            search_params=search_params
        )
        vdb.close()
    #尝试从向量数据库中排查数据
    return {
        'code': 200,
        'type': type,
        'desc': typeJson['desc'],
        'question': question, 
        'typeJson': typeJson, 
        'extJson': extJson, 
        'response': resp[0] if resp[0] else []
    }

# 启动应用
# uvicorn main:app --reload

