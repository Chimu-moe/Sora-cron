import pymysql.cursors
import configparser
import os.path
import redis

CONFIG = ""

if not os.path.isfile("database.ini"):
    CONFIG = configparser.ConfigParser()
    CONFIG['MySQL'] = {
        'Host': 'localhost',
        'Port': '3306',
        'Username': 'root',
        'Password': '',
        'Database': 'database'
    }
    CONFIG['Redis'] = {
        'Host': 'localhost',
        'Port': '6379',
        'Password': '',
        'DB': '0'
    }
    with open('database.ini', 'w') as configfile:
        CONFIG.write(configfile)
    print("a config file got created")
    exit(0)
else:
    with open('database.ini', 'r') as configfile:
        CONFIG = configparser.ConfigParser()
        CONFIG.read("database.ini")

class SqlServer:
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user=CONFIG['MySQL']['Username'],
                             password=CONFIG['MySQL']['Password'],
                             db=CONFIG['MySQL']['Database'],
                             port=int(CONFIG['MySQL']['Port']),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def query(self, q, p=None):
        with self.connection.cursor() as cursor:
            cursor.execute(q, p)
            return cursor.fetchall()

SQL = SqlServer()
REDIS = redis.Redis(host=CONFIG['Redis']['Host'], port=int(CONFIG['Redis']['Port']), db=CONFIG['Redis']['DB'], password=CONFIG['Redis']['Password'])
