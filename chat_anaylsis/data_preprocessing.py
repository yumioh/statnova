import pandas as pd

'''
2. 데이터 전처리
- 불용어 처리 
- 조사 분리 
'''

chat_df = pd.read_csv("./chat_anaylsis/data/kakaochat_cleaning.csv")
print(chat_df.head())
print(chat_df.shape)
