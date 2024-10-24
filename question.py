from pymilvus import MilvusClient,CollectionSchema,DataType,FieldSchema, model
import torch
import logging
import sys





#加载向量模型
# 初始化模型并将其加载到 CPU 或 GPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='./models/mf-all-MiniLM-L6-v2',
    device=device
)

query_embeddings = sentence_transformer_ef.encode_queries(['魔方金豫路668号7', '外高桥'])
print(len(query_embeddings))

# 初始化 MilvusClient
client = MilvusClient(
    uri='http://home.wujialei.com:19530',
    user="root",
    password="Rockywu0427",
    db_name="mf_db"
)
# 定义集合名称和 Schema
collection_name = "room_embeddings"

client.load_collection(
    collection_name=collection_name,
    replica_number=1 # Number of replicas to create on query nodes. Max value is 1 for Milvus Standalone, and no greater than `queryNode.replicas` for Milvus Cluster.
)

res = client.get_load_state(
    collection_name=collection_name
)
print('load_state', res)

search_params = {
    "metric_type": "L2", # 相似度度量方式，例如 L2、IP 或者 Cosine
    "params": {
        "nprobe": 64
    }
}

res = client.search(
    collection_name=collection_name,
    data=query_embeddings,
    anns_field="embedding",
    # filter="store_address in ['上海市闵行区合川路3098号']",
    output_fields=['room_unique_code', 'store_address', 'store_address', 'store_name'],
    limit=10,  # 返回前10条数据
)
for row in res:
    print(row)
    # print(row['room_unique_code'], row['store_address'], row['store_address'], row['store_name'])
    
# combined_text = f"{record['city_name']} {record['region_name']} {record['store_address']} {record['store_name']} "
# embedding = sentence_transformer_ef.encode_documents([combined_text])[0]
# print('关闭连接')
client.close()
sys.exit('exit')