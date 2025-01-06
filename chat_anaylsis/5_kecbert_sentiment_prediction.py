import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset
from text_cleaning import TextCleaner

"""
2. KcBERT를 활용한 감성분석 : 학습된 모델을 사용하여 새로운 데이터의 감정을 예측 (감성분석)
- 학습된 모델과 토크나이저를 로드
- 새로운 댓글 데이터를 로드하고 전처리
- 새로운 댓글 데이터를 토크나이징
- 토크나이징된 데이터를 예측하기 위한 데이터셋으로 변환
- 모델을 사용하여 감정을 예측
- 예측된 감정을 레이블로 변환
- 예측 결과를 원본 데이터프레임에 추가하고 저장
"""

# 데이터 토크나이징
def preprocess_new_data(texts, tokenizer, max_length=128):
    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt"
    )
    return encodings

# 학습된 모델과 토크나이저 로드
model_path = './chat_anaylsis/data/comment/fine_tuned_kcbert'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path) 

# 모델 평가 모드로 전환
model.eval()

# 댓글 데이터 로드 및 전처리
new_data = pd.read_csv(f'./chat_anaylsis/data/kakaochat_cleaning.csv')

# 전처리 함수 재사용
new_data['content'] = new_data['content'].apply(TextCleaner.preprocess_text)
print(new_data.head())
new_comments = new_data['content'].tolist()

new_encodings = preprocess_new_data(new_comments, tokenizer)
 
# 데이터셋 클래스 정의 재사용
class CustomDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: tensor[idx] for key, tensor in self.encodings.items()}

    def __len__(self):
        return len(self.encodings['input_ids'])

new_dataset = CustomDataset(new_encodings)

# 감정 예측
def predict(dataset, model):
    predictions = []
    for item in dataset:
        with torch.no_grad():
            input_ids = item['input_ids'].unsqueeze(0)
            attention_mask = item['attention_mask'].unsqueeze(0)
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=1).item()
            predictions.append(predicted_class_id)
    return predictions

predictions = predict(new_dataset, model)

# 감정 레이블을 숫자로 변환
label_map = {'공포': 0, '분노': 1, '슬픔': 2, '중립': 3, '행복': 4, '혐오': 5}

# 예측된 감정을 레이블로 변환
label_map_reverse = {v: k for k, v in label_map.items()}
predicted_emotions = [label_map_reverse[prediction] for prediction in predictions]

# 예측 결과를 데이터프레임에 추가
new_data['predicted_emotion'] = predicted_emotions

# 결과 저장
new_data[["date","time","dayname","nickname","content","predicted_emotion"]].to_csv(f'./chat_anaylsis/data/predicted_sentiment_chat.csv', index=False)
print("댓글 데이터 Shape : ", new_data.shape)
