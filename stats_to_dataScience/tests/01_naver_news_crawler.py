import os
import sys
import urllib.request
import json
import pandas as pd
from dotenv import load_dotenv

'''
네이버 뉴스 크롤러 API
 - 호출 한도 : 25,000건/일
 - JSON/XML 형식 지원 : 해당 프로젝트에서 JSON 형식 사용
 - Display : 검색 결과 출력 건수 지정(기본값 10, 최대값 100)
 - Start : 검색 시작 위치 지정(기본값 1, 최대값 1000)
 - Sort : 검색 결과 정렬 방식 지정 (sim(유사도순), date(날짜순))
 - 특정 날짜별로 수집이 불가능 =>sort=date로 정렬 후 날짜별로 필터링 필요 => 최대 수집이 가능한 뉴스가 1000건이므로 API로 호출 방법은 어려움
 - 다음 뉴스는 각 언론사별로 페이지로 되어 있어 뉴스 내용 크롤링이 어려움
 - selelium으로 활용한 개별 뉴스 크롤링
 '''

# You need to create a .env file with CLIENT_ID and CLIENT_SECRET
# Load environment variables from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")  

encText = urllib.parse.quote("데이터사이언스")

# start_num = 1
# url = f'https://openapi.naver.com/v1/search/news.json?query={encText}&display=5&start={start_num}&sort=date' # JSON 결과
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)

# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if(rescode==200):
#     response_body = response.read()
#     print(response_body.decode('utf-8'))
# else:
#     print("Error Code:" + rescode)


def get_news_data(query, display, start=1, sort='date'):
    encText = urllib.parse.quote(query)
    url = f'https://openapi.naver.com/v1/search/news.json?query={encText}&display={display}&start={start}&sort={sort}'
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
        return None
    
news = []
for i in range(1, 250000, 10):
    news_data = get_news_data("데이터사이언스", 10, start=i, sort='date')
    if news_data:
        for item in news_data['items']:
            print(item['title'], item['link'], item['pubDate'])
            news.append(item)

df_news = pd.DataFrame(news)
print(df_news.head())
df_news.to_csv('./Stats_to_DataScience/data/naver_news_data.csv', index=False, encoding='utf-8-sig')
