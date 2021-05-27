from konlpy.tag import Komoran

class Preprocess:
    def __init__(self, userdic=None):
        # 형태소 분석기 komoran 초기화
        self.komoran = Komoran(userdic=userdic) # userdic 인자에 사용자 정의 사전 파일 경로 입력하여 추가 가능
        # 제외할 품사 (참조 : https://komorandocs.readthedocs.io/ko/latest/firststep/postypes.html)
        self.exclusion_tags = [
            # 관계언 - 주격조사, 보격조사, 관형격조사, 목적격조사, 부사격조사, 호격조사, 인용격조사, 보조사, 접속조사
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC',
            # 기호 : 마침표,물음표,느낌표, 쉼표,가운뎃점,콜론,빗금, 따옴표,괄호표,줄표, 붙임표
            'SF', 'SP', 'SS', 'SE', 'SO',
            # 어미 : 선어말어미, 종결어미, 연결어미, 명사형전성어미, 관형형전성어미
            'EP', 'EF', 'EC', 'ETN', 'ETM'
            # 접미사 : 명사파생접미사, 동사파생접미사, 형용사파생접미사
            'XSN', 'XSV', 'XSA'
        ]

    # 형태소 분석기 POS Tagger
    def pos(self, sentence):
        return self.komoran.pos(sentence)

    # 불용어 제거 후 필요한 품사 정보 가져오기
    def get_keywords(self, pos, without_tag=False):
        f = lambda x : x in self.exclusion_tags
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list