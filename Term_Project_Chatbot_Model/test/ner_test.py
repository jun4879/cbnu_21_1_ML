import sys
sys.path.append('../utils')
sys.path.append('../models')
sys.path.append('../config')
from preprocess import Preprocess
from ner import NERModule

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

ner = NERModule.NerModel(model_name='../models/ner/ner_best_model.h5', pre_process=p)

# query = "내일 오후 17시 50분에 자장면을 주문하고 싶어요"
# [('내일', 'B_DT'), ('오후', 'B_DT'), ('17시', 'B_DT'), ('50분', 'B_DT'), ('자장면', 'B_FOOD'), ('주문', 'O'), ('싶', 'O')]

query = "오늘 오전 3시 삼성에 이재용이 출근했다"

predicts = ner.predict(query)
print(predicts)