def buildSearchSql(table_name, columns="*", where = None, expansion = None, limit = None, offset=None):
    # 创建一个列表用于存储SQL的各部分
    sql_parts = []
    # 选择的列
    sql_parts.append(f"SELECT {columns} FROM {table_name}")
    if where is not None:
        sql_parts.append(f"where {where}")
    if expansion is not None:
        sql_parts.append(expansion)
    # 添加 LIMIT 和 OFFSET
    if limit is not None:
        sql_parts.append(f"LIMIT {limit}")
    if offset is not None:
        sql_parts.append(f"OFFSET {offset}")
    # 将所有部分组合成一个完整的 SQL 查询
    sql_query = " ".join(sql_parts)
    print('sql_query', sql_query)
    return sql_query