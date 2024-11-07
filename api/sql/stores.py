from mysql_helper import query_mysql
from sql.utils import buildSearchSql

def to_int(value):
    return int(value) if isinstance(value, str) and value.isdigit() else -1

def getMinMax(min, max, radius = 5):
    if min == max and min >= 0:
        min = min - min/radius
        max = max - max/radius
    return min, max
        

def findStores(params, offset = None, limit = None):
    origin = params.get('origin')
    filters = []
    minPrice = to_int(params['price_min'])
    maxPirce = to_int(params['price_max'])
    minArea = to_int(params['area_min'])
    maxArea = to_int(params['area_max'])
    minPrice, maxPirce = getMinMax(minPrice, maxPirce)
    minArea, maxArea = getMinMax(minArea, maxArea)
    args = []
    if minPrice >= 0:
        filters.append('price >= %s')
        args.append(minPrice)
    if maxPirce >= 0:
        filters.append('price <= %s')
        args.append(maxPirce)
    if minArea >= 0:
        filters.append('area >= %s')
        args.append(minArea)
    if maxPirce >= 0:
        filters.append('area <= %s')
        args.append(maxPirce)
    stores = []
    if origin is not None:
        storeSql = buildSearchSql(where='region_name like %s', table_name="stores")
        stores = query_mysql(storeSql, [origin])
    if len(stores) > 0:
        storeCodes = [record.get('store_code', '') for record in stores]
        print('store_codes',storeCodes)
        filters.append('store_code in %s')
        args.append(storeCodes)
    roomtypeSql = buildSearchSql(table_name='rooms', where=" and ".join(filters), columns="store_code",  expansion="group by store_code")
    tmpRooms = query_mysql(roomtypeSql, args)
    rows = query_mysql(buildSearchSql(table_name="stores", where="store_code in %s ", limit=limit), [[record.get('store_code', '') for record in tmpRooms]])
    print('room-stores', rows)
    return rows