import sys
sys.path.append('../utils')
from preprocess import Preprocess

sentense = "내일 저녁 8시에 닭튀김을 주문하고 싶어"

# 전처리 객체 생성
p = Preprocess(userdic='../utils/user_dic.tsv')  # tsv : tab seperated values, 음식 이름, 시간 정보에 대한 사전

# 형태소 분석기 실행
pos = p.pos(sentense)

# 품사 태그와 같이 키워드 출력
ret = p.get_keywords(pos, without_tag=False)
print(ret)
