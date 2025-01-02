import pandas as pd
import os
from ast import literal_eval
from dotenv import load_dotenv
from matplotlib import font_manager, rc
from data_visualizer import DataVisualizer

"""
3. 데이터 시각화 

- 채팅 데이터 워드클라우드

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

print("---------------------워드 클라우드------------------------")

#워드 클라우드 폰트 경로 설정
font_directory = os.getenv("FONT_PATH")
print(font_directory)
font_file = "NanumBarunGothic.ttf"
font_path = os.path.join(font_directory, font_file)
font_name = font_manager.FontProperties(fname=font_path).get_name()

chat_df = pd.read_csv("./chat_anaylsis/data/chat_tokenized.csv")

# 빈리스트 삭제 (135964, 5)
chat_df["content"] = chat_df["content"].apply(literal_eval)
chat_df = chat_df[chat_df['content'].apply(len) > 0]
print(chat_df.shape) 
print(chat_df.head())

# 날짜별 키워드 검색
start_date = '2022-01-01'
end_date = '2024-01-02'
filtered_data = filter_date(chat_df, start_date, end_date)
print(filtered_data)

filename = f"./chat_anaylsis/img/wordcloud_{start_date}.png"
DataVisualizer.create_wordcloud2(filtered_data, font_path, filename)