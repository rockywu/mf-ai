import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from ai_utils import getConfig, filter_none_recursive
from ai_ollama import ask_question_with_ollama_toJson, ask_question_with_ollama
from typing import Optional, List
from sql.stores import findStores
from sql.rooms import findRooms
from prompt_template import get_search_params_tpl, get_unknow_tpl, get_filter_list
from ai_milvus import MilvusDatabase
from ai_encode import encode_queries

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

def to_int(value):
    return int(value) if isinstance(value, str) and value.isdigit() else -1
def buildRoomFilter(params):
    minPrice = to_int(params['price_min'])
    maxPirce = to_int(params['price_max'])
    minArea = to_int(params['area_min'])
    maxArea = to_int(params['area_max'])
    origin = params.get('origin')
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
    if origin is not None:
        filters.append(f' region_name like "{origin}" ')
    return  " && ".join(filters) if len(filters) else None


def buildStoreFilter(params):
    print(params)
    filters = None
    return filters

    

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
def hello():
    return {"status": "ok", "code": 200,  "ollama": {
        "ollamaUrl": ollamaUrl,
        "ollamaModel": ollamaModel
    }}

## 健康检查
@app.get("/healthz")
def healthz():
    return Response(content="OK", media_type="text/plain")
    
class QList(BaseModel):
    question: List[str]  # 字符串数组
    size: int = 5

def searchRooms(params):
    print(params)

    

@app.post("/api/customer")
async def apiCustomer(body: QList):
    q = body.question
    limit = body.size if body.size > 0 else 5
    params = ask_question_with_ollama_toJson(template=get_search_params_tpl, params={"question": q}, model=ollamaModel)
    # 将无法解析的数据丢弃掉
    analyzes = filter_none_recursive(params)
    print('params', analyzes)
    #0-未知类型、1-查房源、2-查门店、3-人工
    vdb = MilvusDatabase()
    vQuestionsArr = []
    for item in ['stroe_name', 'city', 'address', 'origin', 'location', 'decoration']:
        if analyzes.get(item) is not None:
            vQuestionsArr.append(analyzes.get(item))
    print('vQuestionsArr', vQuestionsArr)
    type = int(analyzes.get('type'))
    search_params = {
        "metric_type": "L2", # 相似度度量方式，例如 L2、IP 或者 Cosine
        "params": {
            "nprobe":  200
        }
    }
    if type == 1:  #查房源
        if len(vQuestionsArr) < 1:
            return searchRoomPromptDetails()
        rows = findRooms(params=params, limit=limit)
        return {
            'code': 200,
            'type': type,
            'question': q, 
            'extJson': params, 
            'size': limit,
            'response': rows
        }
        # print(rows)
        # collection_name='room_embeddings'
        # vdb.load_collection(collection_name)
        # vQuestions =encode_queries(questions=vQuestionsArr)
        # resp = vdb.search(
        #     collection_name=collection_name,
        #     data=vQuestions,
        #     anns_field="embedding",
        #     filter=buildRoomFilter(params),
        #     output_fields=[
        #         'room_unique_code',
        #         'room_type_code', 
        #         'store_address', 
        #         'store_address', 
        #         'store_name', 
        #         'store_code', 
        #         'region_name', 
        #         'long_term_type_name',
        #         'area',
        #         'price'
        #     ],
        #     limit=10,  # 返回前10条数据
        #     search_params=search_params
        # )
        # vdb.close()
    elif type == 2:
        if len(vQuestionsArr) < 1:
            return searchStorePromptDetails()
        rows = findStores(params=params, limit=limit)
        return {
            'code': 200,
            'type': type,
            'question': q, 
            'extJson': params, 
            'size': limit,
            'response': rows
        }
        vQuestions =encode_queries(questions=vQuestionsArr)
        collection_name='stores_embeddings'
        vdb.load_collection(collection_name)
        resp = vdb.search(
            collection_name=collection_name,
            data=vQuestions,
            anns_field="embedding",
            filter=buildStoreFilter(params),
            output_fields=['store_address', 'store_address', 'store_name', 'store_code', 'region_name'],
            limit=50,  # 返回前10条数据
            search_params=search_params
        )
        vdb.close()

    elif type == 3:
        No = random.randrange(1000, 10000)
        return {
        'code': 200,
        'type': 3,
        'response': f"人工客服：{No} \n 很高兴为您服务"
    }

    else:
        # unknowParams = ask_question_with_ollama_toJson(template=get_unknow_tpl, params={'question': q}, model=ollamaModel)
        return searchRoomPromptDetails()
        
       
    #尝试从向量数据库中排查数据
    return {
        'code': 200,
        'type': type,
        'question': q, 
        'extJson': params, 
        'response': resp[0] if resp[0] else []
    }

    
def searchRoomPromptDetails(): 
    return {
        'code': 200,
        'type': 0,
        'response': "请说出你详细的找房需求"
    }

def searchStorePromptDetails(): 
    return {
        'code': 200,
        'type': 0,
        'response': "请说出你想找哪里的门店"
    }