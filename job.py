from pymilvus import MilvusClient,CollectionSchema,DataType
from sentence_transformers import SentenceTransformer
from mysql_helper import query_mysql

# 初始化 MilvusClient
client = MilvusClient(
    uri='http://home.wujialei.com:19530',
    token="root:Rockywu0427",
    db_name="my_db"
)

# 定义文本向量化模型
model = SentenceTransformer("all-MiniLM-L6-v2")

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
    for record in results:
        combined_text = f"{record['region_name']} {record['store_address']} {record['store_name']} {record['city_name']}"
        embedding = model.encode(combined_text).tolist()

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

    # 递增偏移量，以便下次检索下一页
    offset += page_size

# 在最后刷新集合以确保数据持久化
client.flush([collection_name])