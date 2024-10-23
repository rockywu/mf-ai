import pymysql

db_host='home.wujialei.com'
db_port=11406
db_user='root'
db_password='RwHome!0427'
db_database='mf-ai'

class MySQLConnectionSingleton:
    _instance = None  # 类的唯一实例
    _connection = None  # 数据库连接

    def __new__(cls):
        # 如果实例不存在，就创建一个新的实例
        if cls._instance is None:
            cls._instance = super(MySQLConnectionSingleton, cls).__new__(cls)
            # 初始化数据库连接
            try:
                cls._connection = pymysql.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_database,
                    port=db_port,
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("数据库连接已建立")
            except pymysql.MySQLError as err:
                print(f"Error connecting to the database: {err}")
                cls._instance = None  # 如果连接失败，释放实例
        return cls._instance

    def get_connection(self):
        """返回数据库连接"""
        return self._connection
