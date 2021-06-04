import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import preprocessing
import sys
sys.path.append('../../utils')
sys.path.append('../..')
from config.GlobalParams import MAX_SEQ_LEN

class IntentModel:
    def __init__(self, model_name, pre_process):
        # 의도별 클래스 labels
        self.labels = {0:'인사', 1:'욕설', 2:'주문', 3:'예약', 4:'기타'}
        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)
        # 챗봇 preprocess 객체
        self.p = pre_process

    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 불용어 제거 및 키워드 추출
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩 처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)

        return predict_class.numpy()[0]