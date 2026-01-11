import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime

'''
셀레리움을 활용한 네이버 뉴스 크롤러
- Selenium과 BeautifulSoup 활용
- 특정 날짜의 뉴스를 키워드로 검색하여 링크 수집
- 해당하는 페이지에서 n.naver.com 도메인의 뉴스 링크만 추출 => 개별 언론사별 페이지에서 소스 구조가 다르기 때문에 일괄 크롤링이 어려움
- 뉴스 본문에서 제목, 본문, 날짜, 언론사 정보 수집
'''

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3') # fatal error만 출력
options.add_argument('--headless')  # 브라우저 창 없이 실행
options.add_argument('--no-sandbox') # 리눅스 환경 대비
options.add_argument('--disable-dev-shm-usage') # 메모리 부족 방지
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#이메일 처리
def email_reg(content) -> str:
    result = re.sub('[\w.+-]+@[\w-]+\.[\w.-]+', '', content)
    return result

#날짜형식 변경
def change_time_prefix(input_str) :
    if not input_str or input_str == "Date Not found":
        return None
    try:
        # 오후, 오전 반환
        clean_date = re.sub(r'기사입력|오후 |오전 ', '', input_str).strip()
        date_obj = datetime.strptime(clean_date, "%Y.%m.%d. %H:%M")
        return date_obj.strftime("%Y.%m.%d")
    
    except ValueError:
        # 만약 형식이 조금 달라서 에러가 나면, 원본에서 날짜 패턴(0000.00.00)만 추출 시도
        match = re.search(r'\d{4}\.\d{2}\.\d{2}', input_str)
        if match:
            return match.group() # 실제 글자 반환
        return "Unknown Date Format"

# Get news links from Naver news based on keyword and date range
def get_news_links(keyword, start_date, end_date):
    # naver news url
    target_url = f"https://search.naver.com/search.naver?where=news&query={keyword}&pd=3&ds={start_date}&de={end_date}"
    driver.get(target_url)
    # wait for page to load 2 seconds
    driver.implicitly_wait(2)

    # 무한 스크롤 모든 뉴스 로드하기 => 네이버 뉴스 JavaScript 동적 로딩 대응을 하기 위함
    # 네이버 뉴스 검색 결과 수에 상관없이 서버에 더 줄 데이터가 없으면 브라우저 전체 길이는 멈추게 되어 있음
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 바닥까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5) # 새 기사가 로드될 때까지의 대기 시간
        
        # 스크롤 후 높이 확인
        new_height = driver.execute_script("return document.body.scrollHeight")
        # 높이가 이전과 같다면(더 이상 로드될 데이터가 없다면) 중단
        if new_height == last_height:
            break
        last_height = new_height
        
    # 모든 데이터가 로드된 후 BeautifulSoup 실행
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 네이버 뉴스 링크 추출
    naver_links = soup.select('a[href*="n.news.naver.com"]')

    link_urls = []
    for link in naver_links:
        link_url = link['href']
        if link_url not in link_urls: ## 중복 링크 제거
            link_urls.append(link_url)

    print(f"{start_date} : 총 {len(link_urls)}건 링크 수집 완료")
    return link_urls

# 뉴스 제목, 본문, 날짜, 언론사 수집 
def get_news_contents(news_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    
    try:
        res = requests.get(news_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 제목
        title_el = soup.select_one('h2#title_area span') 
        title = title_el.text.strip() if title_el else "Title Not found"
        # 날짜
        date_el = soup.select_one('span._ARTICLE_DATE_TIME') 
        date = date_el.text.strip() if date_el else "Date Not found"
        # 언론사    
        press_el = soup.select_one('a.media_end_head_top_logo img')
        press = press_el['title'] if press_el and press_el.has_attr('title') else "Press Not Found"
        # 본문
        content_el = soup.select_one('div#newsct_article')
        if content_el:
            content = " ".join(content_el.get_text().split()) # 공백 여백 제거
            content = email_reg(content)
        else :
            content = "Content Not Found"

        return {
                'title': title,
                'date': change_time_prefix(date),
                'press': press,
                'content': content,
                'url': news_url
        }
    except Exception as e:
        print(f"Error 수집 실패 ({news_url}): {e}")
        return None

# Set date range and keyword for news search
if __name__ == "__main__": # 해당 스크립트가 메인 안에 있는 함수만 실행되도록 함
    start_date = "2026.01.01"
    end_date = "2026.01.11"
    keyword = "데이터사이언스"

    all_news_links = get_news_links(keyword, start_date, end_date)
    print(f"[{start_date} ~ {end_date}] 총 {len(all_news_links)}건 링크 수집 완료")

    news_data = []
    for url in all_news_links:
        news_content = get_news_contents(url)
        if news_content:
            news_data.append(news_content)
        time.sleep(0.5) # 과도한 요청 방지용 미세 대기

    # Save collected data to a DataFrame and CSV
    if news_data :
        df = pd.DataFrame(news_data)
        filet_path = f"./stats_to_dataScience/data/naver_news_{keyword}_{start_date}_to_{end_date}.csv"
        df.to_csv(filet_path, index=False, encoding='utf-8-sig')
        print(f"뉴스 데이터 수집 완료! 총 {len(df)}건의 뉴스가 저장되었습니다.")

driver.quit()


