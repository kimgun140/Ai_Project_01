import numpy as np
from tqdm.notebook import tqdm

from mxnet.gluon import nn
from mxnet import gluon
import mxnet as mx
import gluonnlp as nlp

from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from kobert import get_mxnet_kobert_model
from kobert import get_tokenizer


# CPU
ctx = mx.cpu()

# GPU
# ctx = mx.gpu()


bert_base, vocab = get_mxnet_kobert_model(use_decoder=False, use_classifier=False, ctx=ctx, cachedir=".cache")
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
#
ds = gluon.data.SimpleDataset([['나 보기가 역겨워', '김소월']])
trans = nlp.data.BERTSentenceTransform(tok, max_seq_length=10)
#
# list(ds.transform(trans))

dataset_train = nlp.data.TSVDataset(r"C:\Users\LMS\PycharmProjects\Ai_Project_01\.cache\ratings_train.txt",
                                    field_indices=[1, 2], field_separator=lambda x: x.split(), num_discard_samples=1)
dataset_test = nlp.data.TSVDataset(r"C:\Users\LMS\PycharmProjects\Ai_Project_01\.cache\ratings_test.txt",
                                   field_indices=[1, 2], field_separator=lambda x: x.split(), num_discard_samples=1)
print(dataset_train[0])
class BERTDataset(mx.gluon.data.Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)
        sent_dataset = gluon.data.SimpleDataset([[
            i[sent_idx],
        ] for i in dataset])
        self.sentences = sent_dataset.transform(transform)
        self.labels = gluon.data.SimpleDataset(
            [np.array(np.int32(i[label_idx])) for i in dataset])

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))

max_len = 128
data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)
print(data_test[0])
