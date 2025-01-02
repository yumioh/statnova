import pandas as pd
from word_tagging import WordTagging
from text_cleaning import TextCleaner
from ast import literal_eval
from collections import Counter

'''
2. 데이터 전처리 : 키워드 태깅 및 불용어 처리
- 명사로 분리 
- 불용어 처리
- 최빈어를 조회 => 제거 대상 선정

'''

# (168316, 5)
chat_df = pd.read_csv("./chat_anaylsis/data/kakaochat_cleaning.csv")
print(chat_df.head())
print(chat_df.shape) 

print("---------------------품사부착 및 파일 저장 (PoS Tagging)------------------------")

# 명사 추출 (단, 1글자는 제외)
# chat_df["noun_token"] = chat_df["content"].apply(WordTagging.okt_noun_tagging_remove_one_char)
# print(chat_df.head())

# chat_df[['date','time','dayname','nickname','content','noun_token']].to_csv("./chat_anaylsis/data/chat_noun_tagging.csv", index=False, encoding='utf-8-sig')

print("---------------------불용어 처리------------------------")

chat_nouns = pd.read_csv("./chat_anaylsis/data/chat_noun_tagging.csv")

chat_nouns['noun_token'] = chat_nouns['noun_token'].apply(literal_eval)
# print(chat_nouns['noun_token'].head())

#불용어 처리
stopwords_file = "./chat_anaylsis/data/stopwords.txt"
chat_nouns["content"] = chat_nouns['noun_token'].apply(lambda x: TextCleaner.process_text_with_stop_words(stopwords_file, x))

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in chat_nouns['content'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(40)
print("불용어 처리 후 최빈어 조회 : ", most_common_words)

chat_nouns[["date","time","dayname","nickname","content"]].to_csv("./chat_anaylsis/data/chat_tokenized.csv",index=False, encoding='utf-8-sig')
