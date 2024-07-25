import os
import re
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
# import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook
from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt

import pandas as pd
#
# chatbot_data = pd.read_csv('last_data.csv')
# # print(chatbot_data)
# # f = chatbot_data['comments'].map(lambda x: x[0:-2])
#
#
# # df = chatbot_data['comments'].map(lambda x: x[0:]) # 문장 끝까지? 문장부호 제거하는게 맞음?
# # print(df)
#
# # chatbot_data['comments'] = df
#
# # chatbot_data = chatbot_data.rename(columns={'coments':"comments"})
# # ladataset = chatbot_data
#
# # print(ladataset)
# # print(chatbot_data.sample(n=10))
#
# # ladataset['comments'].nunique(), ladataset['nonehate'].nunique()
# # print('결측값 여부 :',df.isnull().values.any()) # 결측값 없음
# # df.info()
#
# X_data = chatbot_data['comments']  #
# y_data = chatbot_data['nonehate']
# print('코멘트: {}'.format(len(X_data)))
# print('레이블의 개수: {}'.format(len(y_data)))
# # 훈련 테스트  데이터로 쪼개기
# X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.5, random_state=0, stratify=y_data)
# # 검증
# X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=.2, random_state=0, stratify=y_train)
#
# # 소수점 3번째에서 반올림
# print('--------훈련 데이터의 비율-----------')
# print(f'욕설  = {round(y_train.value_counts()[0] / len(y_train) * 100, 3)}%')
# print(f'정상  = {round(y_train.value_counts()[1] / len(y_train) * 100, 3)}%')
# print('--------검증 데이터의 비율-----------')
# print(f'욕설  = {round(y_valid.value_counts()[0] / len(y_valid) * 100, 3)}%')
# print(f'정상  = {round(y_valid.value_counts()[1] / len(y_valid) * 100, 3)}%')
# print('--------테스트 데이터의 비율-----------')
# print(f'욕설  = {round(y_test.value_counts()[0] / len(y_test) * 100, 3)}%')
# print(f'정상  = {round(y_test.value_counts()[1] / len(y_test) * 100, 3)}%')
#
# # 한글과 공백 빼고 전부 제거 사실 이미 제거 되어있어서 ㄱㅊ
# chatbot_data['comments'] = chatbot_data['comments'].str.replace(pat="[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", repl="", regex=True)
# # chatbot_data['comments'] = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","",chatbot_data['comments'])
#
# # print(chatbot_data[:5])
# print(chatbot_data['comments'][:5])
#
# # chatbot_data['comments'].str.replace()
# # print(chatbot_data.isnull().sum())
# chatbot_data['comments'] = chatbot_data['comments'].str.replace('^ +', "") # white space 데이터를 empty value로 변경
# chatbot_data['comments'].replace('', np.nan, inplace=True)
# # chatbot_data['comments'].replace('', np.nan, inplace=True)
#
# # null 값 숫자
# print(chatbot_data.isnull().sum())
#
# # nan값 제거
# chatbot_data = chatbot_data.dropna(how = 'any')
# print(len(chatbot_data))
#
# #train & test 데이터로 나누기
# from sklearn.model_selection import train_test_split
# train_data, test_data = train_test_split(chatbot_data, test_size=0.1, random_state=2023)
# print('훈련용 데이터 개수 :',len(train_data))
# print('테스트용 데이터 개수 :',len(test_data))
#
# stop = pd.read_csv('stopword.txt')
# #print(stop['stopword'])
# stopwords = list(stop['stopword'])
# #print(stopwords)
#
# import platform
# #print(platform.architecture())
#
# os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-22\bin\server"
# print('java_home' in os.environ)
# from konlpy.tag import Okt
# okt = Okt()
#
# X_train = []
# for sentence in tqdm(train_data['comments']): # 진행률 프로그래스바
#     tokenized_sentence = okt.morphs(sentence) # 토큰화 형태소로 자르기 stem = true 각 단어에서 어간을 추출한다.
#
#     # tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화 형태소로 자르기 stem = true 각 단어에서 어간을 추출한다.
#     stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
#     X_train.append(stopwords_removed_sentence)
#
# print(X_train[:5])
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(X_train) # 빈도수 기준으로 단어 집합 생성  tokenizer여기에 담아 버림
# print(tokenizer.word_index)

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from tensorflow.keras.preprocessing.text import Tokenizer
import re
def sentiment_predict(new_sentence):
  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
  new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
  new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
  encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
  pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
  score = float(loaded_model.predict(pad_new)) # 예측
  if(score > 0.5):
    print("{:.2f}% 확률로 정상댓글입니다.\n".format(score * 100))
  else:
    print("{:.2f}% 확률로 이상댓글입니다.\n".format((1 - score) * 100))