import pandas as pd
from text_cleaning import TextCleaner

def convert_to_24(ampm, hour, minute):
    hour = int(hour)
    minute = int(minute)
    if ampm == "오전":
        # 오전 12시는 00시
        if hour == 12:
            hour = 0
    else:  # 오후
        # 오후 12시는 그대로 12시, 나머지는 12 더해줌
        if hour != 12:
            hour += 12
            
    return f"{hour:02d}:{minute:02d}"  # 시:분을 00:00 형식으로 반환

chat_df = pd.read_csv("./chat_anaylsis/data/chat_noun_tagging.csv")

print("------------------키워드별 추출-----------------------------")

keyword = "과목"
# filtered_df = chat_df[chat_df['noun_token'].apply(lambda x: any(k in x for k in keywords))]
filtered_df = chat_df[chat_df['noun_token'].apply(lambda x: keyword in x)]
print(filtered_df.head())
filtered_df.to_csv(f"./chat_anaylsis/data/{keyword}_export.csv")

print("------------------나가는 메시지 추출-----------------------------")

chat_xlsx = pd.read_excel("./chat_anaylsis/data/kakaochat.xlsx")

# 닉네임과 내용 분리
chat_xlsx[["nickname", "content"]] = chat_xlsx['Column2'].str.split(":", n=1, expand=True)
chat_xlsx = chat_xlsx.dropna(subset=['nickname'])
chat_keyword = chat_xlsx[["Column1","nickname"]]
print(chat_keyword[:30])

keyword = "나갔습니다."
left_df = chat_keyword[chat_keyword['nickname'].apply(lambda x: keyword in x)]
print(left_df.head())
print(left_df.shape)

#Column1 대화시간으로 date로 컬럼명 변경
left_df = left_df.rename(columns={"Column1":"datetime"})

# 날짜 분리하기
left_df["date"] = left_df["datetime"].str.extract(r'(\d{4}년 \d{1,2}월 \d{1,2}일)')
left_df["date"] = pd.to_datetime(left_df["date"], format="%Y년 %m월 %d일")

# 요일 추출
left_df["dayname"] = left_df["date"].dt.day_name()

# 날짜포맷 변환
left_df["date"] = left_df["date"].dt.strftime("%y-%m-%d")

# 시간 분리하기
pattern = r'(오전|오후)\s*(\d{1,2}):(\d{2})'
left_df[['ampm','hour','minute']] = left_df['datetime'].str.extract(pattern)
print(left_df.head())

#24시간제로 변경
left_df["time"] = left_df.apply(lambda x: convert_to_24(x['ampm'], x['hour'], x['minute']), axis=1)

left_df = left_df[["date","time","dayname","nickname"]]
left_df.to_csv("./chat_anaylsis/data/left_messages.csv")

print("------------------들어오는 메시지 추출-----------------------------")

keyword = "들어왔습니다."
join_df = chat_keyword[chat_keyword['nickname'].apply(lambda x: keyword in x)]
print(join_df.head())
print(join_df.shape)

#Column1 대화시간으로 date로 컬럼명 변경
join_df = join_df.rename(columns={"Column1":"datetime"})

# 날짜 분리하기
join_df["date"] = join_df["datetime"].str.extract(r'(\d{4}년 \d{1,2}월 \d{1,2}일)')
join_df["date"] = pd.to_datetime(join_df["date"], format="%Y년 %m월 %d일")

# 요일 추출
join_df["dayname"] = join_df["date"].dt.day_name()

# 날짜포맷 변환
join_df["date"] = join_df["date"].dt.strftime("%y-%m-%d")

# 시간 분리하기
pattern = r'(오전|오후)\s*(\d{1,2}):(\d{2})'
join_df[['ampm','hour','minute']] = join_df['datetime'].str.extract(pattern)
print(join_df.head())

#24시간제로 변경
join_df["time"] = join_df.apply(lambda x: convert_to_24(x['ampm'], x['hour'], x['minute']), axis=1)

join_df = join_df[["date","time","dayname","nickname"]]
join_df.to_csv("./chat_anaylsis/data/join_messages.csv")