
from pymilvus import MilvusClient

# 获取一个链接
client = MilvusClient(
    uri='http://home.wujialei.com:19530', # replace with your own Milvus server address
    token="root:Rockywu0427",
    db_name="my_db"
) 

opt = client.list_collections() 
print(opt)



#client.create_database("my_db")
