from db_connection import MySQLConnectionSingleton

def query_mysql(query):
    """
    使用单例数据库连接执行给定的 SQL 查询并返回结果。

    参数:
    - query: SQL 查询字符串

    返回:
    - 查询结果（list），每一行是一个 tuple。
    """
    try:
        # 获取数据库连接单例实例
        db_connection_singleton = MySQLConnectionSingleton()
        db_connection = db_connection_singleton.get_connection()

        if db_connection is None:
            print("数据库连接不可用")
            return None

        # 创建游标对象
        cursor = db_connection.cursor()

        # 执行查询
        cursor.execute(query)

        # 获取所有查询结果
        results = cursor.fetchall()

        # 关闭游标（不关闭连接）
        cursor.close()

        return results

    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None
