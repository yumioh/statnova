import pandas as pd
from text_cleaning import TextCleaner

'''
1. data cleaning : 데이터의 불필요한 요소를 제거하거나 데이터를 분석 가능하게 만드는 초기 작업
- 컬럼명 변경 및 추가 : column1 -> data, nickname(대화닉네임), content(대화내용용)
- 닉네임과 채팅 내용 분리
- NaN값 제거
- 시간, 날짜 요일 분리 및 추출
- 특수문자 제거

'''

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

# 카톡 데이터 불려오기
chat_txt = pd.read_excel("./chat_anaylsis/data/kakakochat.xlsx")
#(210837, 3)
print("raw data : ",chat_txt.shape)
# print("raw data : ",chat_txt[:20])

# 닉네임과 내용 분리
chat_txt[["nickname", "content"]] = chat_txt['Column2'].str.split(":", n=1, expand=True)

#Column1 대화시간으로 date로 컬럼명 변경
chat_txt = chat_txt.rename(columns={"Column1":"datetime"})

# nan값 제거 : (168441, 3)
chat_df = chat_txt[["datetime","nickname", "content"]].dropna()
print("removing missing values shape : ", chat_txt.shape)

# 날짜 분리하기
chat_df["date"] = chat_df["datetime"].str.extract(r'(\d{4}년 \d{1,2}월 \d{1,2}일)')
chat_df["date"] = pd.to_datetime(chat_df["date"], format="%Y년 %m월 %d일")

# 요일 추출
chat_df["dayname"] = chat_df["date"].dt.day_name()
print(chat_df["dayname"].head())
# 날짜포맷 변환
chat_df["date"] = chat_df["date"].dt.strftime("%y-%m-%d")
#print(chat_df['datetime'])

# 시간 분리하기
pattern = r'(오전|오후)\s*(\d{1,2}):(\d{2})'
chat_df[['ampm','hour','minute']] = chat_df['datetime'].str.extract(pattern)

# 날짜 nan값 제거
chat_df.dropna(subset=['ampm','hour','minute'], inplace=True)

#24시간제로 변경
chat_df["time"] = chat_df.apply(lambda x: convert_to_24(x['ampm'], x['hour'], x['minute']), axis=1)

#특수문자 제거
chat_df["content"] = chat_df["content"].apply(TextCleaner.remove_special_characters)

#데이터 저장 : 168316건
print(chat_df[:10])
print(chat_df.info())
chat_df[["date","time","dayname","nickname","content"]].to_csv("./chat_anaylsis/data/kakaochat_cleaning.csv",index=False)
