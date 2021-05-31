import pymssql
import pandas as pd


conn  = pymssql.connect(host='(local)', database='chatbot_train_data', as_dict=True, charset='UTF8')
cursor = conn.cursor()

cursor.execute('SELECT * from chatbot_train_data')

row = cursor.fetchall()

data = pd.DataFrame(row)

print(data)