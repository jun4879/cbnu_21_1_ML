# 주피터 코드 참조

import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from seqeval.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import sys
sys.path.append('..')
from utils.preprocess import Preprocess

def read_file(file_name):
    sents = []
    # 학습 데이터 형태 참고
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx+1][0] == '$':
                this_sent = []
            elif l[0] == '$' and lines[idx-1][0] == ';':
                continue
            elif l[0] == '\n':
                sents.append(this_sent)
            else :
                this_sent.append(tuple(l.split()))
    return sents


# 전처리 객체
p = Preprocess(word2index_dic='../../train_tools/dict/chatbot_dict.bin',
               userdic='../../utils/user_dic.tsv')

# 학습용 말뭉치 데이터
corpus = read_file('ner_train.txt')

# 말뭉치 데이터에서 단어와 BIO 태그만 불러와 학습용 데이터셋 생성
sentences, tags = [], []
for t in corpus :
    tagged_sentence = []
    sentence, bio_tag = [], []
    for w in t:
        tagged_sentence.append((w[1],w[3]))
        sentence.append(w[1])
        bio_tag.append(w[3])
    sentences.append(sentence)
    tags.append(bio_tag)

print("sample size : ", len(sentences))
print("0번째 샘플 단어 시퀀스 : ", sentences[0])
print("0번째 샘플 bio tag : ", tags[0])
print("sample sequence maxlen : ", max(len(l) for l in sentences))
print("sample sequence average len : ", (sum(map(len, sentences))/len(sentences)))

# 토크나이저 정의
tag_tokenizer = preprocessing.text.Tokenizer(lower=False)
tag_tokenizer.fit_on_texts(tags)

# 단어 사전 및 태그 사전 크기
vocab_size = len(p.word_index) + 1
tag_size = len(tag_tokenizer.word_index) + 1
print("BIO 태그 사전 크기 : ", tag_size)
print("단어 사전 크기 : ", vocab_size)

# 학습용 단어 시퀀스 생성
x_train = [p.get_wordidx_sequence(sent) for sent in sentences]
y_train = tag_tokenizer.texts_to_sequences(tags)

index_to_ner = tag_tokenizer.index_word
index_to_ner[0] = 'PAD'

# 시퀀스 패딩 처리
max_len = 40
x_train = preprocessing.sequence.pad_sequences(x_train, padding='post', maxlen=max_len)
y_train = preprocessing.sequence.pad_sequences(y_train, padding='post', maxlen=max_len)

x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=.2, random_state=2021)

# 출력 데이터 One-Hot Encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=tag_size)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=tag_size)

print("학습 샘플 시퀀스 shape", x_train.shape)
print("학습 샘플 label shape", y_train.shape)
print("test 샘플 시퀀스 shape", x_test.shape)
print("test 샘플 label shape", y_test.shape)

# Bi-LSTM
model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=30, input_length=max_len, mask_zero=True))
model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.5, recurrent_dropout=0.25)))
model.add(TimeDistributed(Dense(tag_size, activation='softmax')))
checkpoint = ModelCheckpoint('./ner_best_model.h5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
model.compile(loss='categorical_crossentropy', optimizer=Adam(0.01), metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=128, epochs=10, callbacks= checkpoint, verbose=1)

print("평가 결과 : ", model.evaluate(x_test, y_test)[1])

# 시퀀스 NER 태그로 변환
def sequences_to_tag(sequences):
    result = []
    for sequence in sequences:
        temp = []
        for pred in sequence:
            pred_index = np.argmax(pred)
            temp.append(index_to_ner[pred_index].replace("PAD", "0"))
            result.append(temp)
    return result

y_predicted = model.predict(x_test)
pred_tags = sequences_to_tag(y_predicted)
test_tags = sequences_to_tag(y_test)

print(classification_report(test_tags, pred_tags))
print("F1-score : {:.2%}".format(f1_score(test_tags, pred_tags)))