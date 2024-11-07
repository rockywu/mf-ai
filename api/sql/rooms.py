from mysql_helper import query_mysql
from sql.utils import buildSearchSql

def to_int(value):
    return int(value) if isinstance(value, str) and value.isdigit() else -1

def getMinMax(min, max, radius = 5):
    if min == max and min >= 0:
        min = min - min/radius
        max = max - max/radius
    return min, max
        

def findRooms(params, offset = None, limit = None):
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
    storesMap = {}
    if origin is not None:
        storeSql = buildSearchSql(where='region_name like %s', table_name="stores")
        stores = query_mysql(storeSql, [origin])
    if len(stores) > 0:
        storeCodes = [record.get('store_code', '') for record in stores]
        print('store_codes',storeCodes)
        filters.append('store_code in %s')
        args.append(storeCodes)
    roomtypeSql = buildSearchSql(table_name='rooms', where=" and ".join(filters), columns="MIN(room_unique_code) as room_unique_code",  expansion="group by room_type_code", limit=limit)
    tmpRooms = query_mysql(roomtypeSql, args)
    resultSql = f"""SELECT
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
            r.room_type_code,
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
        where room_unique_code in %s 
    """
    rows = query_mysql(resultSql, [[record.get('room_unique_code', '') for record in tmpRooms]])
    print('room-rows', rows)
    return rows