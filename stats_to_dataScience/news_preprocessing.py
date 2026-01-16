import pandas as pd
from ast import literal_eval
from collections import Counter
import re

'''
2. 데이터 전처리 : 키워드 태깅 및 불용어 처리
- 명사로 분리
- 불용어 처리
- 특수문자제거
- 최빈어를 조회 => 제거 대상 선정
'''   

def load_stop_words(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
         stop_words = [line.strip() for line in file.readlines()]
    return stop_words

keywords = ['데이터', '통계']
text_df = pd.read_csv(f"./stats_to_dataScience/data/news_cleaning_{keywords}.csv")
print(text_df.head())
print(text_df.shape) 
print("---------------------품사부착 및 파일 저장 (PoS Tagging)------------------------")

# #명사 추출 (단, 1글자는 제외)
# text_df["noun_token"] = text_df["content"].apply(WordTagging.okt_noun_tagging_remove_one_char)
# print(text_df.head())

# text_df[['date', 'title', 'content','noun_token']].to_csv(f"./stats_to_dataScience/data/news_noun_tagging_{keywords}.csv", index=False, encoding='utf-8-sig')


print("---------------------불용어 처리 시작------------------------")
# 1. 파일 읽기
news_text_nouns = pd.read_csv(f"./stats_to_dataScience/data/news_noun_tagging_{keywords}.csv")

# 2. 먼저 리스트 객체로 변환 
# NaN 값이 있을 수 있으므로 fillna 후 변환
news_text_nouns['noun_token'] = news_text_nouns['noun_token'].fillna('[]').apply(literal_eval)

# 3. 불용어 사전 미리 로드 (딱 한 번만 실행)
stopwords_file = "./stats_to_dataScience/data/stopwords.txt"
stop_words = load_stop_words(stopwords_file)

# 4. 통합 전처리 함수 (특수문자 제거 + 불용어 처리)
def final_cleaning(tokens):
    cleaned = []
    for token in tokens:
        word = re.sub(r"[^가-힣]", "", token)
        # 리스트보다 Set에서 찾는 것이 훨씬 빠름
        if (word not in stop_words) and (len(word) >= 2):
            cleaned.append(word)
    return cleaned

# 5. 전처리 적용
news_text_nouns["noun_contents"] = news_text_nouns['noun_token'].apply(final_cleaning)

# 6. 최빈어 조회 (메모리 아끼는 Counter 사용)
word_counts = Counter()
for tokens in news_text_nouns['noun_contents']:
    word_counts.update(tokens)

most_common_words = word_counts.most_common(40)
print("최종 최빈어 조회 : ", most_common_words)

# 7. 저장
print(news_text_nouns.info())
news_text_nouns[['date', 'title', 'noun_contents']].to_pickle(f"./stats_to_dataScience/data/news_tokenized_{keywords}.pkl")
#news_text_nouns[['date', 'title', 'noun_contents']].to_csv(f"./stats_to_dataScience/data/news_tokenized_{keywords}.csv",index=False, encoding='utf-8-sig')