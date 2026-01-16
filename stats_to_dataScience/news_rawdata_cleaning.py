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

# 수집한 데이터 병합
# 1. 경로 및 설정
input_dir = "./stats_to_dataScience/data/raw_data"  # CSV 파일들이 있는 폴더
keywords = ['데이터','통계']
output_path = f"./stats_to_dataScience/data/merged_news_{keywords}.csv" # 결과 파일 경로
target_columns = ['date', 'title', 'content', 'url'] # 고정할 컬럼 순서

# merged_df = pd.DataFrame()

# # 2. 파일 목록 순회 및 필터링
# if os.path.exists(input_dir):
#     files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
#     print(files)
    
#     for file in files:
#         if all(k in file for k in keywords):
#             file_path = os.path.join(input_dir, file)
#             print(f"작업 중인 파일: {file}")
            
#             try:
#                 # CSV 읽기 (한글 깨짐 방지를 위해 utf-8-sig 사용)
#                 temp_df = pd.read_csv(file_path, encoding='utf-8-sig')
                
#                 # 병합 (전체 데이터프레임에 추가)
#                 merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
#             except Exception as e:
#                 print(f"{file} 읽기 실패: {e}")

#     # 3. 컬럼 순서 재배치 및 저장
#     if not merged_df.empty:
#         # 지정된 컬럼이 데이터에 실제로 있는지 확인 후 순서 변경
#         # (혹시 없는 컬럼이 있을 경우 에러 방지를 위해 존재하는 것만 필터링)
#         existing_cols = [col for col in target_columns if col in merged_df.columns]
#         merged_df = merged_df[existing_cols]
        
#         # 중복 데이터 제거 (필요 시)
#         merged_df.drop_duplicates(inplace=True)
        
#         # 저장
#         merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
#         print(f"--- 병합 완료! 총 {len(merged_df)}행 저장됨 ---")
#         print(f"저장 경로: {output_path}")
#     else:
#         print(f'{keywords}에 맞는 파일이 없거나 데이터가 비어 있습니다.')
# else:
#     print(f"경로를 찾을 수 없습니다: {input_dir}")


# 뉴스 데이터 불려오기
# AI, 통계 : 26207건
# 데이터, 통계 : 77512건
news_txt = pd.read_csv(f'./stats_to_dataScience/data/merged_news_{keywords}.csv')
#(210837, 3)
print("raw data : ", news_txt.shape)
# print("raw data : ",chat_txt[:20])

# nan값 없음
news_txt = news_txt[['date', 'title', 'content', 'url']].dropna()
print("removing missing values shape : ", news_txt.shape)

# 날짜순서대로 정리 
news_txt = news_txt.sort_values(by='date', ascending=True)
# print(news_txt['date'].head())

#특수문자 제거
news_txt["content"] = news_txt["content"].apply(TextCleaner.remove_special_characters)

print(news_txt[:10])
print(news_txt.info())
news_txt[['date', 'title', 'content']].to_csv(f'./stats_to_dataScience/data/news_cleaning_{keywords}.csv',index=False)