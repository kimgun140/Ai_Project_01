import pandas as pd
import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import AdamW, BertModel, BertTokenizer
from transformers.optimization import get_cosine_schedule_with_warmup
from tqdm import tqdm
import gluonnlp as nlp

# KoBERT 모델과 토크나이저 로드
from kobert_transformers import get_kobert_model

# KoBERT 모델과 토크나이저 로드
kobert_model = get_kobert_model()
tokenizer = BertTokenizer.from_pretrained('monologg/kobert')


# KoBERT에 입력될 데이터셋 클래스
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return self.sentences[i] + (self.labels[i],)

    def __len__(self):
        return len(self.labels)


# 파라미터 설정
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 5
max_grad_norm = 1
log_interval = 200
learning_rate = 5e-5


# 모델 정의
class BERTClassifier(nn.Module):
    def __init__(self, bert, hidden_size=768, num_classes=2, dr_rate=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1

        _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                              attention_mask=attention_mask.float())
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


# 데이터 로드 및 전처리
dataset_train = nlp.data.TSVDataset(r"C:\Users\LMS\PycharmProjects\Ai_Project_01\.cache\ratings_train.txt",
                                    field_indices=[0, 1], num_discard_samples=1)
dataset_test = nlp.data.TSVDataset(r"C:\Users\LMS\PycharmProjects\Ai_Project_01\.cache\ratings_test.txt",
                                   field_indices=[0, 1], num_discard_samples=1)

# BERTSentenceTransform에 tokenizer를 직접 전달
data_train = BERTDataset(dataset_train, 0, 1, tokenizer, max_len, True, False)
data_test = BERTDataset(dataset_test, 0, 1, tokenizer, max_len, True, False)

train_dataloader = DataLoader(data_train, batch_size=batch_size, num_workers=5)
test_dataloader = DataLoader(data_test, batch_size=batch_size, num_workers=5)

# 모델 초기화
model = BERTClassifier(kobert_model, dr_rate=0.5)

# 최적화 설정
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
    {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]

optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
loss_fn = nn.CrossEntropyLoss()

t_total = len(train_dataloader) * num_epochs
warmup_step = int(t_total * warmup_ratio)

scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

# 모델 훈련
for epoch in range(num_epochs):
    model.train()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(train_dataloader)):
        optimizer.zero_grad()
        token_ids = token_ids.long()
        segment_ids = segment_ids.long()
        valid_length = valid_length
        label = label.long()
        out = model(token_ids, valid_length, segment_ids)
        loss = loss_fn(out, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        optimizer.step()
        scheduler.step()

    # 모델 평가
    model.eval()
    eval_accuracy = 0.0
    nb_eval_steps = 0
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(test_dataloader)):
        token_ids = token_ids.long()
        segment_ids = segment_ids.long()
        valid_length = valid_length
        label = label.long()
        with torch.no_grad():
            out = model(token_ids, valid_length, segment_ids)

        logits = out.detach().numpy()
        label_ids = label.numpy()

        tmp_eval_accuracy = np.sum(np.argmax(logits, axis=1) == label_ids)
        eval_accuracy += tmp_eval_accuracy
        nb_eval_steps += 1

    print("Epoch {}: Accuracy: {}".format(epoch, eval_accuracy / len(data_test)))
