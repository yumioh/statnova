import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from ast import literal_eval
from dotenv import load_dotenv
import os
from matplotlib import font_manager, rc

# 한글 폰트 설정
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

chat_df = pd.read_csv("./chat_anaylsis/data/chat_tokenized.csv")

# 토큰 데이터를 리스트 형태로 변환
chat_df['content'] = chat_df['content'].apply(literal_eval)

# 날짜 열을 datetime 형식으로 변환
chat_df['date'] = pd.to_datetime(chat_df['date'], format='%y-%m-%d')

# 월별로 데이터를 집계하고 히트맵 생성
chat_df['month'] = chat_df['date'].dt.month  # 월만 추출

# 모든 키워드를 하나의 리스트로 합치기
all_tokens = [token for tokens in chat_df['content'] for token in tokens]

# 키워드 상위 15개 추출
top_keywords = [word for word, count in Counter(all_tokens).most_common(10)]

# 월별 키워드 빈도수 계산
heatmap_data = pd.DataFrame(0, index=range(1, 13), columns=top_keywords)

for month, tokens in chat_df.groupby('month')['content']:
    token_counts = Counter([token for token_list in tokens for token in token_list])
    for keyword in top_keywords:
        heatmap_data.loc[month, keyword] = token_counts[keyword]

# 히트맵 시각화
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", cbar=True)
plt.title('Monthly Keyword Frequency Heatmap (Top 10)', fontsize=16)
plt.xlabel('Keywords', fontsize=12)
plt.ylabel('Month', fontsize=12)
plt.xticks(fontsize=15)
plt.yticks(ticks=range(1, 13), labels=[f'{m}월' for m in range(1, 13)], rotation=0,fontsize=15)
plt.tight_layout()
plt.savefig("./chat_anaylsis/img/keyword_heatmap.png", dpi=300)
plt.show()


