import pymssql
import openpyxl
#import pyodbc
import sys
sys.path.append('../../config')
from DBConfig import *

def all_clear_train_data(db):
    sql = '''
        delete from chatbot_train_data
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)
    # 교재 auto increment 초기화 ~ mysql 관련 구문인듯 하여 삭제

def insert_data(db, xls_row):
    row_id, intent, ner, query, answer, answer_img_url = xls_row
    # 쿼리문 들어갈 때 따옴표 넣어서 string 형태로 insert 되게 작성 주의 / 오류 날 경우 sql 문으로 디버그 테스트
    sql = "INSERT into chatbot_train_data(id, intent, ner, query, answer, answer_image) values({0}, '{1}', '{2}', '{3}', '{4}', '{5}')".format(
        row_id.value, intent.value, ner.value, query.value, answer.value, answer_img_url.value)
    sql = sql.replace("'None'", "null")

    with db.cursor() as cursor:
        cursor.execute(sql)
        print('{} 저장'.format(query.value))
        db.commit()

train_file = './train_data.xlsx'
db = None
try :
    #db = pyodbc.connect(server=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
    db = pymssql.connect(server=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
    all_clear_train_data(db)

    wb = openpyxl.load_workbook(train_file)
    sheet = wb['Sheet1']
    for row in sheet.iter_rows(min_row=2):
        print(row)
        insert_data(db, row)
    wb.close()
except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()