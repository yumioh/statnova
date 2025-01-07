import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from text_cleaning import TextCleaner

"""
1. KcBERT를 활용한 감성분석 : 학습된 모델을 사용하여 새로운 데이터의 감정을 예측(감성분석)
"""

# 데이터 로드
data = pd.read_csv('./chat_anaylsis/data/comment/korean_coverstaion_datasets.csv')

# "놀람"을 제외한 데이터 필터링
# data = data[data['Emotion'] != '놀람']

data['Sentence'] = data['Sentence'].apply(TextCleaner.preprocess_text)
comments = data['Sentence'].tolist()
labels = data['Emotion'].tolist()

# 감정 레이블을 숫자로 
 
label_map = {'공포': 0, '분노': 1, '슬픔': 2, '중립': 3, '행복': 4, '혐오': 5, '놀람' : 6}
labels = [label_map[label] for label in labels]

# 데이터 분할
train_texts, val_texts, train_labels, val_labels = train_test_split(comments, labels, test_size=0.2)

# Tokenizer로 BertModel의 입력값을 만든 후, 넣어서 출력값 생성
tokenizer = BertTokenizer.from_pretrained("beomi/kcbert-base")

def preprocess_data_with_labels(texts, labels, tokenizer, max_length=128):
    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt"
    )
    encodings['labels'] = torch.tensor(labels)
    return encodings

train_encodings = preprocess_data_with_labels(train_texts, train_labels, tokenizer)
val_encodings = preprocess_data_with_labels(val_texts, val_labels, tokenizer)

# 데이터셋 클래스 정의
class CustomDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: tensor[idx] for key, tensor in self.encodings.items()}

    def __len__(self):
        return len(self.encodings['input_ids'])

train_dataset = CustomDataset(train_encodings)
val_dataset = CustomDataset(val_encodings)

# 모델 로드 및 학습 설정
model = BertForSequenceClassification.from_pretrained("beomi/kcbert-base", num_labels=len(label_map))

training_args = TrainingArguments(
    output_dir='./chat_anaylsis/data/comment/results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=300,
    weight_decay=0.01,
    logging_dir='./chat_anaylsis/data/comment/logs',
    logging_steps=50,
    eval_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# 모델 학습
trainer.train()

# 모델 평가
eval_result = trainer.evaluate()
print("Evaluation result:", eval_result)

# 학습된 모델 저장
model.save_pretrained('./chat_anaylsis/data/comment/fine_tuned_kcbert')
tokenizer.save_pretrained('./chat_anaylsis/data/comment/fine_tuned_kcbert')