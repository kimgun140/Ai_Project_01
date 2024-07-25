import os
import re
import torch
# from keras.src.saving import load_model
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
# import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook
# from keras.preprocessing.text import Tokenizer

# from keras.src.preprocessing.text.Tokenizer import Tokenizer

# from keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.text import Tokenizer

from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
import pandas as pd
# from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.sequence import pad_sequences
import keras.models
import pickle


stop = pd.read_csv('stopword.txt',sep = '\t' )
stop['stopword'] = stop['stopword'].str.replace("'", "")
stop['stopword'] = stop['stopword'].str.replace(",", "") # 불용어 제거 중
stop['stopword'].to_list()
list(stop['stopword'])
stopwords = list(stop['stopword']) #불용어
print(stopwords)
max_len = 50
# loaded_model = keras.models.load_model('LSTM_model (2).h5')
loaded_model = keras.models.load_model('LSTM_model.h5')

with open('tokenizer (1).pickle', 'rb') as handle:
  tokenizer = pickle.load(handle)
def sentiment_predict(new_sentence):
  okt = Okt()
  # tokenizer = Tokenizer()

  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
  new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
  print(new_sentence[0])
  new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
  print(new_sentence[0])
  encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩 여기서 0으로 바꿔버리네
  print(encoded)
  pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
  print(pad_new)
  score = float(loaded_model.predict(pad_new)) # 예측
  print(score)
  if(score > 0.5):
    print("{:.2f}% 확률로 정상댓글입니다.\n".format(score * 100))
  else:
    print("{:.2f}% 확률로 이상댓글입니다.\n".format((1 - score) * 100))

import re
# def sentiment_predict(new_sentence):
#   new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
#   new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
#   new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
#   encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
#   pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
#   score = float(loaded_model.predict(pad_new)) # 예측
#   if(score > 0.5):
#     print("{:.2f}% 확률로 정상댓글입니다.\n".format(score * 100))
#   else:
#     print("{:.2f}% 확률로 이상댓글입니다.\n".format((1 - score) * 100))
sentence = "씨발"
sentiment_predict(sentence)
# import tensorflow as tf
# print(tf.__version__)  # TensorFlow 버전 확인