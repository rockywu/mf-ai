# main.py
from mysql_helper import query_mysql
from vdb_connect import connect_to_weaviate 
client = connect_to_weaviate(
    http_host='127.0.0.1',
    http_port=18080,
    http_secure=False,
    grpc_host='127.0.0.1',
    grpc_port=50051,
    grpc_secure=False
)
client.close()
# SQL 查询语句
sql_query = """
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
        stores s ON r.store_code = s.store_code;
"""
# 调用 query_mysql 函数执行查询
results = query_mysql(sql_query)

# # 输出查询结果
# if results:
#     for row in results:
#         print(row['city_code'])
#         print(row)
# else:
#     print("查询失败或无结果")
