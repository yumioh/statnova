import pandas as pd
import os
from ast import literal_eval
from dotenv import load_dotenv
from matplotlib import font_manager, rc
from data_visualizer import DataVisualizer
from gensim.models import LdaMulticore, TfidfModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.corpora import Dictionary
import matplotlib.pyplot as plt


"""
3. 데이터 시각화 

- 채팅 내용 기반 워드클라우드
- LDA 만들기

"""

# 해당하는 기간만 데이터 뽑기
def filter_date(df, start_date, end_date):
    """
    - start_date : 필터링 시작 날짜 (포맷: 'YYYY-MM-DD')
    - end_date : 필터링 종료 날짜 (포맷: 'YYYY-MM-DD')

    """
    # 'date' 열을 datetime 형식으로 변환
    if df['date'].dtype == 'object':  # 문자열인 경우만 변환
        df['date'] = pd.to_datetime(df['date'], format='%y-%m-%d')
    # 날짜 형식 변환
    condition_date = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
    return df[condition_date]

#LDA 모델링 및 파일 저장
def lda_modeling_and_visualization(corpus, dictionary,start_date):
    num_topics = 15  # 원하는 주제 수
    lda_model = LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary, passes=10, workers=6, random_state=42)

    # 각 주제별로 중요한 단어 확인
    for idx, topic in enumerate(lda_model.print_topics(num_words=5)):
        print(f"Topic {idx}: {topic}")

    # 문서별 주제 분포 확인
    for index, topic_dist in enumerate(lda_model[corpus][:5]):
        print(f"Document {index}: {topic_dist}")

    # pyLDAvis로 시각화 준비 및 저장
    filename = f'./chat_anaylsis/img/lda_{start_date}.html'
    vis = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, filename)

print("---------------------워드 클라우드------------------------")

# 한글 폰트 설정
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

chat_df = pd.read_csv("./chat_anaylsis/data/chat_tokenized.csv")

# 빈리스트 삭제 (135964, 5)
chat_df["content"] = chat_df["content"].apply(literal_eval)
chat_df = chat_df[chat_df['content'].apply(len) > 0]
print(chat_df.shape) 
print(chat_df.head())

# 날짜별 키워드 검색
start_date = '2021-01-01'
end_date = '2024-12-31'
filtered_data = filter_date(chat_df, start_date, end_date)
print(filtered_data)

filename = f"./chat_anaylsis/img/wordcloud_{start_date}.png"
DataVisualizer.create_wordcloud(filtered_data, font_path, filename)

print("---------------------LDA 학습------------------------")
# #multiprocessing을 사용하는 코드로 main을 넣어줘어야함
# if __name__ == '__main__':
#     #딕셔너리 생성 
#     dictionary = Dictionary(filtered_data['content'])
#     # 앞에서 10개의 항목을 출력
#     print("idword : ", list(dictionary.items())[:10])

#     #LDA 모델링을 위해 벡터화된 문서(코퍼스) 확인
#     corpus = [dictionary.doc2bow(tokens) for tokens in filtered_data['content']]

#     #tfidf로 벡터화 적용
#     tfidf = TfidfModel(corpus)
#     corpus_TFIDF = tfidf[corpus]

#     lda_modeling_and_visualization(corpus_TFIDF, dictionary, start_date)

print("---------------------감정 분석 결과 원그래프------------------------")

# 원 그래프 저장 위치
pieGraph_path = f"./chat_anaylsis/img/pie_graph_sentiment.png"

sentiment_chat = pd.read_csv("./chat_anaylsis/data/predicted_sentiment_chat.csv")
print(sentiment_chat.head())

sentiment_chat =  sentiment_chat[["content","predicted_emotion"]]
print(sentiment_chat["predicted_emotion"].value_counts())

colors= ['red','yellow','purple','goldenrod','blue','lightcoral']
plt.figure(figsize=(8, 6))
plt.pie(sentiment_chat["predicted_emotion"].value_counts(), labels=sentiment_chat["predicted_emotion"].value_counts().index, autopct='%1.1f%%', colors=colors, startangle=140)
plt.axis('equal')
plt.title('채팅 감정 비율', fontsize=20)
plt.axis('equal')
plt.savefig(pieGraph_path, dpi=300)