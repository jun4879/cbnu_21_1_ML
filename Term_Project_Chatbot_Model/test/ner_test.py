import sys
sys.path.append('..')
from utils.preprocess import Preprocess
from models.ner import NERModule

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

ner = NERModule.NerModel(model_name='../models/ner/ner_best_model.h5', pre_process=p)

# query = "내일 오후 17시 50분에 자장면을 주문하고 싶어요"
# [('내일', 'B_DT'), ('오후', 'B_DT'), ('17시', 'B_DT'), ('50분', 'B_DT'), ('자장면', 'B_FOOD'), ('주문', 'O'), ('싶', 'O')]

query = "첼시는 30일(한국시각) 포르투갈 포르투 이스타디우 두 드라강에서 열린 2020∼2021 유럽축구연맹(UEFA) 챔피언스리그 결승전에서 카이 하베르츠(22)의 결승골에 힘입어 맨체스터 시티를 1-0으로 꺾고 우승을 차지했다"

predicts = ner.predict(query)
print(predicts)