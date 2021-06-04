# 주피터 수정 코드 참조

import pandas as pd
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate
import sys
sys.path.append('../..')
from utils.preprocess import Preprocess
from config.GlobalParams import MAX_SEQ_LEN

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
dataset = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
dataset = dataset.shuffle(len(queries))

train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_dataset = dataset.take(train_size).batch(20)
val_dataset = dataset.skip(train_size).take(val_size).batch(20)
test_dataset = dataset.skip(train_size + val_size).take(test_size).batch(20)

# 하이퍼 파라미터 설정
dropout_prob = 0.5
EMB_SIZE = 128
EPOCH = 5
VOCAB_SIZE = len(p.word_index) + 1

# CNN 모델 정의
input_layer = Input(shape=(MAX_SEQ_LEN,))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)
# 3-gram
conv1 = Conv1D(filters=128, kernel_size=3, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool1 = GlobalMaxPool1D()(conv1)
# 4-gram
conv2 = Conv1D(filters=128, kernel_size=4, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool2 = GlobalMaxPool1D()(conv2)
# 5-gram
conv3 = Conv1D(filters=128, kernel_size=5, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool3= GlobalMaxPool1D()(conv3)

concat = concatenate([pool1, pool2, pool3])

hidden = Dense(128, activation=tf.nn.relu)(concat)
dropout_hidden = Dropout(rate=dropout_prob)(hidden)
logits = Dense(5, name='logits')(dropout_hidden)
predictions = Dense(5, activation=tf.nn.softmax)(logits)

# 모델 생성
model = Model(inputs=input_layer, outputs=predictions)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_dataset, validation_data=val_dataset, epochs=EPOCH, verbose=1)

loss, acc = model.evaluate(test_dataset, verbose=1)
print("ACC : %f"%(acc*100))
print("LOSS : %f"%loss)

model.save('intent_classification_model.h5')
