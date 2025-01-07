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
- 감정 분석 결과 시각화
- 날짜별, 요일별, 달별 채팅 입출 시각화

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
    num_topics = 7  # 원하는 주제 수
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

chat_df = pd.read_csv("./chat_anaylsis/data/chat_tokenized_강의.csv")

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

filename = f"./chat_anaylsis/img/wordcloud_{start_date}_강의.png"
DataVisualizer.create_wordcloud(filtered_data, font_path, filename)

print("---------------------키워드별 워드 클라우드------------------------")

exclude_keywords = ["강의","과목","수업","시험","문제","과제","출석","혹시","학기","교수"]
keyword = "교수"

# 한글 폰트 설정
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

chat_df = pd.read_csv(f"./chat_anaylsis/data/chat_tokenized_{keyword}.csv")

# 빈리스트 삭제 (135964, 5)
chat_df["content"] = chat_df["content"].apply(literal_eval)
chat_df = chat_df[chat_df['content'].apply(len) > 0]
print(chat_df.shape) 
print(chat_df.head())

# '강의' 키워드 제거
filtered_data['content'] = filtered_data['content'].apply(lambda tokens: [token for token in tokens if token not in exclude_keywords])

filename = f"./chat_anaylsis/img/wordcloud_{keyword}.png"
DataVisualizer.create_wordcloud(filtered_data, font_path, filename)

print("-------------------최빈어별 BAR 그래프------------------------")

keywords = ["과목", "학기", "과제", "수업", "시험", "문제", "출석", "혹시", "통계", "강의", "교수"]
counts = [9656, 6798, 5959, 5316, 5475, 4531, 3965, 3930, 5910, 3652, 3540]

# 막대 그래프 생성
plt.figure(figsize=(12, 6))
plt.bar(keywords, counts, color='#00509E', edgecolor='black')

#custom_colors = ['#4A90E2', '#00509E', '#00274D']
# 그래프 설정
plt.title('키워드 빈도', fontsize=18)
plt.xlabel('Keywords', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("./chat_anaylsis/img/Top_Keywords_bar.png", dpi=300)
plt.tight_layout()

# 그래프 출력
plt.show()

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
pieGraph_path = "./chat_anaylsis/img/pie_graph_sentiment.png"

sentiment_chat = pd.read_csv("./chat_anaylsis/data/predicted_sentiment_chat.csv")
print(sentiment_chat.head())

sentiment_chat =  sentiment_chat[["content","predicted_emotion"]]
print(sentiment_chat["predicted_emotion"].value_counts())

colors= ['red','yellow','purple','goldenrod','blue','lightcoral']
plt.figure(figsize=(8, 6))
plt.pie(sentiment_chat["predicted_emotion"].value_counts(), labels=sentiment_chat["predicted_emotion"].value_counts().index, autopct='%1.1f%%', colors=colors, startangle=140,textprops={'fontsize': 13})
plt.axis('equal')
plt.title('채팅 감정 비율', fontsize=20)
plt.axis('equal')
plt.savefig(pieGraph_path, dpi=300)

print("---------------------감정 분석 결과 긍/부정------------------------")
positive_emotions = ['행복']
negative_emotions = ['공포', '분노', '슬픔', '혐오']

sentiment_chat['emotion'] = sentiment_chat['predicted_emotion'].apply(
    lambda x: '긍정' if x in positive_emotions else ('부정' if x in negative_emotions else '중립')
)

sentiment_chat_cnt = sentiment_chat["emotion"].value_counts()
sentiment_chat_cnt = sentiment_chat_cnt[['긍정', '부정']]

colors = ['#0079FF', '#FF204E']
plt.figure(figsize=(8, 6))
plt.pie(sentiment_chat_cnt, labels=sentiment_chat_cnt.index, autopct='%1.1f%%', colors=colors, startangle=140,textprops={'fontsize': 15})
plt.axis('equal')
plt.title('채팅 긍/부정 비율', fontsize=20)
plt.savefig("./chat_anaylsis/img/pie_graph_sentiment_pn.png", dpi=300)
#plt.show()

print("---------------------요일별 입장하는 채팅 막대그래프------------------------")

join_df = pd.read_csv("./chat_anaylsis/data/join_messages.csv")
print(join_df.shape)

# print(join_df["date"].value_counts())

dayname_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dayname_counts = join_df["dayname"].value_counts().reindex(dayname_order)

plt.figure(figsize=(10, 6))
ax = dayname_counts.plot(kind='line', color='#00509E', label='Join Count', linewidth=2)

# 값 표시
for x, y in enumerate(dayname_counts):
    ax.text(x, y, str(y), fontsize=10, ha='center', va='bottom', color='black')

plt.title('Number of Joins Per Date', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Join Count', fontsize=12)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("./chat_anaylsis/img/line_graph_join_dayname.png", dpi=300)
plt.show()

print("---------------------요일별 나가는 채팅 선그래프------------------------")

left_df = pd.read_csv("./chat_anaylsis/data/left_messages.csv")
print(left_df.shape)

# print(join_df["date"].value_counts())

dayname_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dayname_counts = left_df["dayname"].value_counts().reindex(dayname_order)

plt.figure(figsize=(10, 6))
ax = dayname_counts.plot(kind='line', color='red', label='Join Count', linewidth=2)

# 값 표시
for x, y in enumerate(dayname_counts):
    ax.text(x, y, str(y), fontsize=10, ha='center', va='bottom', color='black')

plt.title('Number of Left Per Date', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Left Count', fontsize=12)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("./chat_anaylsis/img/line_graph_left_dayname.png", dpi=300)
plt.show()

print("---------------------시간별 입장하는 채팅 선그래프------------------------")
join_df = pd.read_csv("./chat_anaylsis/data/join_messages.csv")

# 시간대별 데이터 집계
join_df['datetime'] = pd.to_datetime(join_df['date'] + ' ' + join_df['time'], format="%y-%m-%d %H:%M")
join_df['hour'] = join_df['datetime'].dt.hour

# 시간대별 데이터 집계
join_by_hour = join_df['hour'].value_counts().sort_index().reset_index()
join_by_hour.columns = ["hour", "count"]

plt.figure(figsize=(10, 6))
plt.plot(join_by_hour['hour'], join_by_hour['count'], marker='o', color='#00509E', label='Join Count', linewidth=2)

# 값 표시
for x, y in zip(join_by_hour['hour'], join_by_hour['count']):
    plt.text(x, y, str(y), fontsize=10, ha='center', va='bottom', color='black')

# 그래프 설정
plt.title('Joins by Hour', fontsize=14)
plt.xlabel('Hour', fontsize=12)
plt.ylabel('Join Count', fontsize=12)
plt.xticks(range(24), labels=[f'{h}:00' for h in range(24)], rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("./chat_anaylsis/img/line_graph_join_hour.png", dpi=300)
plt.tight_layout()

#plt.show()

print("---------------------시간별 나가는 채팅 선그래프------------------------")
left_df = pd.read_csv("./chat_anaylsis/data/left_messages.csv")

# 시간대별 데이터 집계
left_df['datetime'] = pd.to_datetime(left_df['date'] + ' ' + left_df['time'], format="%y-%m-%d %H:%M")
left_df['hour'] = left_df['datetime'].dt.hour

# 시간대별 데이터 집계
left_by_hour = left_df['hour'].value_counts().sort_index().reset_index()
left_by_hour.columns = ["hour", "count"]

plt.figure(figsize=(10, 6))
plt.plot(left_by_hour['hour'], left_by_hour['count'], marker='o', color='#00509E', label='Join Count', linewidth=2)

# 값 표시
for x, y in zip(left_by_hour['hour'], left_by_hour['count']):
    plt.text(x, y, str(y), fontsize=10, ha='center', va='bottom', color='black')

# 그래프 설정
plt.title('Lefts by Hour', fontsize=14)
plt.xlabel('Hour', fontsize=12)
plt.ylabel('Left Count', fontsize=12)
plt.xticks(range(24), labels=[f'{h}:00' for h in range(24)], rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("./chat_anaylsis/img/line_graph_left_hour.png", dpi=300)
plt.tight_layout()

#plt.show()

print("---------------------입장하는 채팅 선그래프(년도별 및 달별)------------------------")
# join_df = pd.read_csv("./chat_anaylsis/data/join_messages.csv")

# # 날짜별로 데이터 집계
# join_by_date = join_df["date"].value_counts().reset_index()
# join_by_date.columns = ["date", "count"]

# # 날짜 형식 변환
# join_by_date['date'] = pd.to_datetime(join_by_date['date'], format="%y-%m-%d")

# # 연도와 월 추가
# join_by_date['year'] = join_by_date['date'].dt.year
# join_by_date['month'] = join_by_date['date'].dt.month

# monthly_data = join_by_date.groupby(['year', 'month'])['count'].sum().reset_index()

# print(monthly_data)

# # 연도별로 선 그래프 그리기
# plt.figure(figsize=(10, 6))
# for year in monthly_data['year'].unique():
#     yearly_data = monthly_data[monthly_data['year'] == year]
#     plt.plot(yearly_data['month'], yearly_data['count'], marker='o', label=f'{year}')

# # 그래프 설정
# plt.title('Monthly Joins by Year', fontsize=14)
# plt.xlabel('Month', fontsize=12)
# plt.ylabel('Join Count', fontsize=12)
# plt.xticks(range(1, 13))
# plt.legend(title='Year')
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.savefig("./chat_anaylsis/img/line_graph_join_year_month.png", dpi=300)
# plt.tight_layout()

# # 그래프 출력
# plt.show()


print("--------------------나가는 채팅 선그래프(년도별 및 달별)------------------------")
# left_df = pd.read_csv("./chat_anaylsis/data/left_messages.csv")

# # 날짜별로 데이터 집계
# left_by_date = left_df["date"].value_counts().reset_index()
# left_by_date.columns = ["date", "count"]

# # 날짜 형식 변환
# left_by_date['date'] = pd.to_datetime(left_by_date['date'], format="%y-%m-%d")

# # 연도와 월 추가
# left_by_date['year'] = left_by_date['date'].dt.year
# left_by_date['month'] = left_by_date['date'].dt.month

# monthly_data = left_by_date.groupby(['year', 'month'])['count'].sum().reset_index()
# #print(monthly_data)

# # 연도별로 선 그래프 그리기
# plt.figure(figsize=(10, 6))
# for year in left_by_date['year'].unique():
#     yearly_data = monthly_data[monthly_data['year'] == year]
#     plt.plot(yearly_data['month'], yearly_data['count'], marker='o', label=f'{year}')

# # 그래프 설정
# plt.title('Monthly Lefts by Year', fontsize=14)
# plt.xlabel('Month', fontsize=12)
# plt.ylabel('Left Count', fontsize=12)
# plt.xticks(range(1, 13))
# plt.legend(title='Year')
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.savefig("./chat_anaylsis/img/line_graph_left_year_month.png", dpi=300)
# plt.tight_layout()

# # 그래프 출력
# plt.show()