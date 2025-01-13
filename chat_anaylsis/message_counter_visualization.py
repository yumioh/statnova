import pandas as pd
import matplotlib.pyplot as plt

# 연별 막대 그래프
yearly_df = pd.read_csv("./data/yearly_messages.csv")
yearly_df.plot(
    x='date',
    y='message_count',
    kind='bar',
    figsize=(10, 6),
    color='#00509E',
    edgecolor='black'
)

plt.title('Yearly Message Count')
plt.xlabel('Year')
plt.ylabel('Number of Messages')

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 요일별 막대 그래프
day_of_week_df = pd.read_csv("./data/day_of_week_message.csv")
day_of_week_df.plot(
    x='dayname',
    y='message_count',
    kind='bar',
    figsize=(10, 6),
    color='#00509E',
    edgecolor='black'
)

plt.title('Day of week Message Count')
plt.xlabel('Day of week')
plt.ylabel('Number of Messages')

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 시간별 라인 차트
hourly_df = pd.read_csv("./data/hourly_messages.csv")
hourly_df.plot(
    kind='line',
    x='date',
    y='message_count',
    marker='o',
    color='#00509E',
    figsize=(10, 6)
)

plt.xticks(hourly_df.index)
plt.title('Hourly Message Count', fontsize=16)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Message Count', fontsize=12)
plt.grid(True)  # 그리드 표시
#plt.tight_layout()  # 레이아웃 자동 조정
plt.show()

# 월별/연별 누적 막대 그래프
df = pd.read_csv("./data/yearly_by_monthly_message.csv")

monthly_df = df.pivot(index='month', columns='year', values='message_count')
custom_colors = ['#4A90E2', '#00509E', '#00274D']  # 각각 밝은 파랑, 중간 파랑, 어두운 파랑
monthly_df.plot(
    kind='bar',
    stacked=True,
    figsize=(12, 6),
    color=custom_colors,
    width=0.8
)
plt.title("Monthly Message Count (Stacked by Year)", fontsize=16)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Message Count", fontsize=12)
plt.legend(title="Year", fontsize=10, loc="upper left")
plt.xticks(range(12), [f"{i}" for i in range(1, 13)], rotation=0)  # X축에 월 표시
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()