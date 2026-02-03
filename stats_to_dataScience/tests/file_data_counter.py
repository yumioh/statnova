import pandas as pd

# 1. 데이터 불러오기
keywords = ['데이터', '통계']
# df = pd.read_csv(f'./stats_to_dataScience/data/merged_news_{keywords}_2025.csv')
df = pd.read_pickle(f"./stats_to_dataScience/data/filtered_news_['데이터', '통계']_2017-10-01_to_2025-09-30_2025.pkl")

# 2. 날짜 컬럼을 datetime 형식으로 변환 (오류 방지를 위해 필수)
df['date'] = pd.to_datetime(df['date'])

# 3. 시작일과 종료일 설정
start_date = '2017-01-01'
end_date = '2025-09-30'

# 4. 해당 기간 데이터 필터링
mask = (df['date'] >= start_date) & (df['date'] <= end_date)
filtered_df = df.loc[mask]

# 필터링된 데이터만 새로운 CSV로 저장
#filtered_df.to_pickle(f'./stats_to_dataScience/data/filtered_news_{keywords}_{start_date}_to_{end_date}_2025.pkl')

# 5. 건수 확인 : 82,624
count = len(filtered_df)

print(f"{start_date}부터 {end_date}까지의 데이터 건수는 총 {count:,}건입니다.")