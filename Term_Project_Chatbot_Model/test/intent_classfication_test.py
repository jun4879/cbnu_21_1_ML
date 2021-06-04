import sys
sys.path.append('..')
from utils.preprocess import Preprocess
from models.intent_classification import IntentModule

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

intent = IntentModule.IntentModel(model_name='../models/intent_classification/textbook_intent_model.h5', pre_process=p)

query = "5시반에 퇴근입니다"
# query = "안녕" # 욕설
# query = "선선한 봄 날씨가 계속 됐으면 좋겠네요" # 인사
# query = "짜장면 5개요" # 주문
# query = "짜장면 저녁 6시 반에 가능해요?" # 예약
# query = "5시반에 퇴근입니다" # 기타

predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print("의도 예측 클래스 :", predict)
print("의도 예측 label :", predict_label)

'''
<결과 및 고찰>
- 정확도 문제 해결 필요
    - 원인 후보 : 데이터 셋 or 전처리 or 모델 구조
'''