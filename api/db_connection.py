import pymysql

from ai_utils import getConfig

db_host=getConfig('mysql.host')
db_port=getConfig('mysql.port')
db_user=getConfig('mysql.user')
db_password=getConfig('mysql.password')
db_database=getConfig('mysql.database')

print (db_host, db_port, db_user, db_password, db_database)

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
                    port=int(db_port),
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
