import pandas as pd
import os

input_dir = "./stats_to_dataScience/data"
keywords = ['데이터','통계']
output_path = f"./stats_to_dataScience/data/merged_news_{keywords}_2017_2025.csv" # 결과 파일 경로
target_columns = ['date', 'noun_token'] # 고정할 컬럼 순서

merged_df = pd.DataFrame()

if os.path.exists(input_dir):
    files = [f for f in os.listdir(input_dir) if f.startswith('merged_news_')]
    print(files)

    for file in files:
        if all(k in file for k in keywords):
            file_path = os.path.join(input_dir, file)
            print(f"작업 중인 파일")

            try:
                temp_df = pd.read_csv(file_path, encoding='utf-8')

                merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
            except Exception as e :
                print(f'{file} 읽기 실패 : {e}')

    if not merged_df.empty:
        # 지정된 컬럼이 데이터에 실제로 있는지 확인 후 순서 변경
        # (혹시 없는 컬럼이 있을 경우 에러 방지를 위해 존재하는 것만 필터링)
        existing_cols = [col for col in target_columns if col in merged_df.columns]
        merged_df = merged_df[existing_cols]
        
        # 중복 데이터 제거 (필요 시)
        merged_df.drop_duplicates(inplace=True)
        
        # 저장
        merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"--- 병합 완료! 총 {len(merged_df)}행 저장됨 ---")
        print(f"저장 경로: {output_path}")
    else:
        print(f'{keywords}에 맞는 파일이 없거나 데이터가 비어 있습니다.')
else:
    print(f"경로를 찾을 수 없습니다: {input_dir}")

        