class FindAnswer:
    def __init__(self, db):
        self.db = db

    def _make_query(self, intent_name, ner_tags):
        sql = "select TOP 1 * from chatbot_train_data"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}'".format(intent_name)

        elif intent_name != None and ner_tags != None:
            where = " where intent='%s' "%intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where

        # 동일 답변이 2개 이상인 경우 랜덤으로 선택
        # mssql의 경우 limit 1 없어서 고쳐야 함
        sql = sql + " order by newid()"
        return sql

    def search(self, intent_name, ner_tags):
        # 의도명과 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)
        #print("의도명 및 개체명 답변 검색 :", sql)
        #print("의도명 및 개체명으로 검색한 답변 :", answer)

        # 검색 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)
            #print("의도명 답변 검색 :", sql)
            #print("의도명으로 검색한 답변 :", answer)
        return answer['answer']  # answer['answer_image']

    def tag_to_word(self, ner_predicts, answer):
        food_word = ''
        dt_word = ''
        for word, tag in ner_predicts:
            if tag == 'B_FOOD':
                food_word += word + ' '
            if tag == 'B_DT':
                dt_word += word + ' '
        answer = answer.replace('B_FOOD', food_word)
        answer = answer.replace('B_DT', dt_word)
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
