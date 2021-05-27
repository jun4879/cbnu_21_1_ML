import pandas as pd
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate
import sys
sys.path.append('../../utils')
from preprocess import Preprocess
sys.path.append('../../config')
from GlobalParams import MAX_SEQ_LEN

train_file = "total_train_data.csv"
data = pd.read_csv(train_file, delimiter=',')
# 데이터 구조 : 컬럼 2개(query, intent)
# query : 발화 내용
# intent : 발화 내용에 대한 label, 0~인사, 1~욕설, 2~주문, 3~예약, 4~기타
queries = data['query'].tolist()
intents = data['intent'].tolist()

# 전처리 객체
p = Preprocess(word2index_dic='../../train_tools/dict/chatbot_dict.bin',
               userdic='../../utils/user_dic.tsv')

# 단어 시퀀스 생성
sequences = []
for sentence in queries:
    pos = p.pos(sentence)
    keywords = p.pos(sentence)
    seq = p.get_wordidx_sequence(keywords)
    sequences.append(seq)

# 단어 시퀀스 벡터 생성
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

# train, validation, test set 생성