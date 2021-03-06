#import pymssql
import pymysql
import logging

class ChatbotDB:
    def __init__(self, host, user, password, db_name, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if self.conn != None:
            return

        self.conn = pymysql.connect( #pymssql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.db_name,
            charset = self.charset
        )

    def close(self):
        if self.conn is None:
            return

        if not self.conn:
        #if not self.conn.open:
            self.conn = None
            return
        self.conn.close()
        self.conn = None

    def execute(self, sql):
        last_row_id = -1
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
            last_row_id = cursor.lastrowid
        except Exception as ex:
            logging.error(ex)
        finally:
            return last_row_id

    def select_one(self, sql):
        result = None
        try:
            #with self.conn.cursor(as_dict=True) as cursor:  # pymssql 코드
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor: # pymysql 코드
                cursor.execute(sql)
                result = cursor.fetchone()
                print("db_module result: ", result)
        except Exception as ex:
            logging.error(ex)
            print("db_module exception: ", ex)
        finally:
            return result

    '''
    def select_all(self, sql):
        result = None
        try:
            with self.conn.cursor(as_dict=True) as cursor:
            #with self.conn.cursor(pymssql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception as ex:
            logging.error(ex)
        finally:
            return result
    '''

