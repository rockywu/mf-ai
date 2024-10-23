from pymilvus import MilvusClient,CollectionSchema,DataType,FieldSchema
from sentence_transformers import SentenceTransformer
from mysql_helper import query_mysql
import torch

# 初始化模型并将其加载到 CPU 或 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
# 定义文本向量化模型 # 定义模型并载入到指定设备
#model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
print('device', device)

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


client.close()



