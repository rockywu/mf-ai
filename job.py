from pymilvus import MilvusClient,CollectionSchema,DataType,FieldSchema, model
from mysql_helper import query_mysql
import numpy as np
import torch
import logging
import sys


# 初始化 MilvusClient
client = MilvusClient(
    uri='http://home.wujialei.com:19530',
    user="root",
    password="Rockywu0427",
    db_name="mf_db"
)


# 定义集合名称和 Schema
collection_name = "room_embeddings"

collection_schema = CollectionSchema(
    fields=[
        FieldSchema(name="room_unique_code", dtype=DataType.VARCHAR, max_length=50, is_primary=True, auto_id=False),  # 作为主键
        FieldSchema(name="store_code", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="region_name", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="store_address", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="store_name", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="city_name", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)  # 根据模型的维度
    ],
    auto_id=False,
    description="Embeddings with unique room codes as primary key"
)

# 创建集合如果还没有创建的话
if not client.has_collection(collection_name):
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="embedding", 
        index_type="IVF_FLAT",
        metric_type="L2",
        params={ "nlist": 128 }
    )
    client.create_collection(
        collection_name=collection_name, 
        schema=collection_schema, 
        shards_num=2,
        index_params=index_params
    )

#加载向量模型
# 初始化模型并将其加载到 CPU 或 GPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='./models/mf-all-MiniLM-L6-v2',
    device=device
)

def getQuery(offset, pageSize = 100):
    # SQL 查询语句
    return f"""
        SELECT
            r.store_code,
            r.store_name,
            r.room_unique_code,
            r.room_number,
            r.price,
            r.building_number,
            r.building_name,
            r.floor,
            r.long_term_type_code,
            r.long_term_type_name,
            r.area,
            r.orientation,
            r.light_status,
            r.decoration,
            s.city_code,
            s.city_name,
            s.region_code,
            s.region_name,
            s.store_address,
            s.latitude,
            s.longitude
        FROM
            rooms r
        JOIN
            stores s ON r.store_code = s.store_code
        LIMIT {pageSize} OFFSET {offset}
    """


# 分页查询和处理
pageSize = 200
offset = 0
while True:
    # 查询数据
    results = query_mysql(getQuery(offset=offset, pageSize=pageSize))
    if not results:
        break  # 如果没有更多结果，则退出循环
    # 构建插入数据
    insert_data_list = []

    # 插入每页数据
    for index, record in enumerate(results):
        combined_text = f"{record['city_name']} {record['region_name']} {record['store_address']} {record['store_name']} "
        embedding = sentence_transformer_ef.encode_documents([combined_text])[0]
        # print('embedding-len', len(embedding))
        # 确保嵌入的向量长度为 384
        if len(embedding) != 384:
            print(f"Warning: Embedding size is {len(embedding)}, but expected 384.")
            continue  # 跳过不符合维度的记录
        insert_data = {
            "room_unique_code": record['room_unique_code'],
            "store_code": record['store_code'],
            "region_name": record['region_name'],
            "store_address": record['store_address'],
            "store_name": record['store_name'],
            "city_name": record['city_name'],
            "embedding": embedding
        }
        insert_data_list.append(insert_data)
    # print('data-list-len', len(insert_data_list))
    # print('data-list[0]', insert_data_list[0])

    res = client.insert(
        collection_name=collection_name, 
        data=insert_data_list,
        sync=True
    )
    print('完成序号', offset, '~', offset + pageSize)

    # 递增偏移量，以便下次检索下一页
    offset += pageSize


print('关闭连接')
client.close()
sys.exit('exit')