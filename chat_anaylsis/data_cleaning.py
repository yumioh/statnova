import pandas as pd

'''
1. data cleaning

데이터의 불필요한 요소를 제거하거나 데이터를 분석 가능하게 만드는 초기 작업
- 컬럼명 변경 및 추가 : column1 -> data, nickname(대화닉네임), content(대화내용용)
- 닉네임과 내용 분리 
- NaN값 제거

'''
# 카톡 데이터 불려오기
chat_txt = pd.read_excel("./chat_anaylsis/data/kakakochat.xlsx")
#(210837, 3)
print("raw data : ",chat_txt.shape)

# 닉네임과 내용 분리
chat_txt[["nickname", "content"]] = chat_txt['Column2'].str.split(":", n=1, expand=True)

#Column1 대화시간으로 date로 컬럼명 변경
chat_txt = chat_txt.rename(columns={"Column1":"date"})

# 닉네임, 대화내용, 날짜만 뽑기기
chat_txt = chat_txt[["date","nickname","content"]]

# nan 값 갯수
# nickname    32743
# content     42396
# date         7182
print(chat_txt.isna().sum())

# nan값 제거 
chat_txt = chat_txt.dropna()

#데이터 저장 : (168441, 3)
chat_txt[["date","nickname","content"]].to_csv("./chat_anaylsis/data/kakaochat_cleaning.csv",index=False)
