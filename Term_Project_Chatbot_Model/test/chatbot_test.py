import sys
sys.path.append('..')
from config.DBConfig import *
from utils.db_module import ChatbotDB
from utils.preprocess import Preprocess
from models.intent_classification import IntentModule
from models.ner import NERModule
from utils.FindAnswer import FindAnswer

# 전처리 객체 생성
p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

# DB 연결 객체 생성
db = ChatbotDB(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME, charset='UTF8')
db.connect()

# 발화문
# query = "오전에 자장면 10개 주문합니다"

'''
의도 파악:  기타
개체명 인식:  [('오전', 'B_DT'), ('자장면', 'B_FOOD'), ('10', 'O'), ('개', 'O'), ('주문', 'O')]
답변 검색에 필요한 NER tag:  ['B_DT']
----------------------------------------
'NoneType' object is not subscriptable # 예외 처리 : 기타 클래스에 대한 답변 없음
답변:  무슨 말인지 몰라요
# 보완점 : 주문 의도 파악 못 함
'''

# query = "짜장면 탕수육 1개요"
'''
의도 파악:  주문
개체명 인식:  [('짜장면', 'B_OG'), ('탕수육', 'O'), ('1', 'O'), ('개요', 'O')]
답변 검색에 필요한 NER tag:  ['B_OG']
----------------------------------------
답변:  B_FOOD 주문 처리 감사!! / 답변:  B_FOOD 주문 처리 완료되었습니다. 주문해주셔서 감사합니다.
# 보완점 : 짜장면, 탕수육 개체명 인식 안 됐음
'''

# query = "안녕"
'''
----------------------------------------
의도 파악:  욕설
개체명 인식:  [('안녕', 'O')]
답변 검색에 필요한 NER tag:  None
----------------------------------------
답변:  욕하면 나빠요 ㅠ
# 보완점 : 인사 의도 파악 못 함
'''

# query = "내일 오후 17시 50분에 자장면을 주문하고 싶어요"
'''
----------------------------------------
의도 파악:  예약
개체명 인식:  [('내일', 'B_DT'), ('오후', 'B_DT'), ('17시', 'B_DT'), ('50분', 'B_DT'), ('자장면', 'B_FOOD'), ('주문', 'O'), ('싶', 'O')]
답변 검색에 필요한 NER tag:  ['B_DT']  
----------------------------------------
답변:  B_DT에 예약 접수 되었습니다.
'''

query = input("질문 내용 : ")

# 의도 파악
intent = IntentModule.IntentModel(model_name='../models/intent_classification/textbook_intent_model.h5', pre_process=p)
intent_predict = intent.predict_class(query)
intent_name = intent.labels[intent_predict]

# 개체명 인식
ner = NERModule.NerModel(model_name='../models/ner/ner_best_model.h5', pre_process=p)
ner_predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 :", query)
print("-"*40)
print("의도 파악: ", intent_name)
print("개체명 인식: ", ner_predicts)
print("답변 검색에 필요한 NER tag: ", ner_tags)
print("-"*40)

try:
    f = FindAnswer(db)
    answer_text = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(ner_predicts, answer_text)
except Exception as e:
    print(e)
    answer = "무슨 말인지 몰라요"

print("답변: ", answer)

db.close()