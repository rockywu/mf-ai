from pymilvus import MilvusClient,CollectionSchema,DataType,FieldSchema, model
from sentence_transformers import SentenceTransformer
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
        FieldSchema(name="room_unique_code", dtype=DataType.VARCHAR, max_length=50, is_primary=True),  # 作为主键
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
   client.create_collection(collection_name, schema=collection_schema, shards_num=2)

#加载向量模型
# 初始化模型并将其加载到 CPU 或 GPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='./models/mf-all-MiniLM-L6-v2',
    device=device
)


# 分页查询和处理
page_size = 100
offset = 0
while True:
    # SQL 查询语句
    sql_query = f"""
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
        LIMIT {page_size} OFFSET {offset}
    """

    # 查询数据
    results = query_mysql(sql_query)
    if not results:
        break  # 如果没有更多结果，则退出循环

    # 插入每页数据
    for index, record in enumerate(results):
        combined_text = f"{record['city_name']} {record['region_name']} {record['store_address']} {record['store_name']} "
        embedding = sentence_transformer_ef.encode_documents(combined_text)

        # 例如，截断或补齐向量
        if len(embedding) > 384:
            embedding = embedding[:384]
        elif len(embedding) < 384:
            embedding = np.pad(embedding, (0, 384 - len(embedding)), 'constant')
        print('embedding-finish', combined_text)

        insert_data = [
            record['room_unique_code'],
            record['store_code'],
            record['region_name'],
            record['store_address'],
            record['store_name'],
            record['city_name'],
            embedding
        ]

        client.insert(collection_name, [insert_data])
    print('完成序号', offset)

    # 递增偏移量，以便下次检索下一页
    offset += page_size


print('关闭连接')
client.close()
sys.exit('x')



# 定义文本向量化模型 # 定义模型并载入到指定设备
#model = SentenceTransformer("./models/mf-all-MiniLM-L6-v2").to('cuda:0')
#embedding = model.encode(f"你好么？").tolist()
embedding = sentence_transformer_ef.encode_documents('你好么？')
print('embedding', embedding)






# 在最后刷新集合以确保数据持久化

client.close();



