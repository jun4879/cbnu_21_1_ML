import sys
sys.path.append('..')

import pickle
from utils.preprocess import Preprocess

f = open('../train_tools/dict/chatbot_dict.bin', 'rb')
word_index = pickle.load(f)
f.close()

sentence = "오늘 오후 5시 30분에 닭고기를 먹고 싶어 ㅎㅎㅎ"

# 전처리 객체 생성
p = Preprocess(userdic='../utils/user_dic.tsv')

# 형태소 분석기 실행
pos = p.pos(sentence)

# 품사 태그와 같이 키워드 출력
keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
    try:
        print(word, word_index[word])
    except KeyError:
        # 해당 단어가 사전에 없는 경우 OOV 처리
        print(word, word_index['OOV'])