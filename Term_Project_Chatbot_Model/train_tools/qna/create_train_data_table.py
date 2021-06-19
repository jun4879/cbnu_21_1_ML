#import pymssql
import pymysql
import sys
sys.path.append('../..')
from config.DBConfig import *

db = None
try :
    db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
        #pymssql.connect(server=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
    sql = '''
        CREATE TABLE IF NOT EXISTS 'chatbot_train_data' (
        'id' INT NULL,
        'intent' VARCHAR(45) NULL,
        'ner' VARCHAR(1024) NULL,
        'query' TEXT NULL,
        'answer' TEXT NOT NULL,
        'answer_image' VARCHAR(2048) NULL,
        PRIMARY KEY ('id')
        )
        '''
    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()