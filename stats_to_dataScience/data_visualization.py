import pandas as pd
import os
from dotenv import load_dotenv
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import seaborn as sns
import networkx as nx
from itertools import combinations
# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import apriori, association_rules

"""
3. 데이터 시각화 

- 년도별 뉴스 기사 빈도수 추출
- 학과명 명칭이 변경된 시점에서 두 그룹으로 나눈뒤 키워드 분석 : 2020년 10월 변경
   변경 전 : 2017년 10월 ~ 2020년 9월 30일 / 변경 후 : 2020 10월 01일 ~ 2025년 10월 30일
- 학과명 전후 시점에서 키워드 분석을 하는데 networkx 활용 : 2023년 기점 / 2020년 10월 기점 
- 17~20년도 상위 키워드와 21~24년도 상위 키워드 뽑아 순위변화 확인 
- 전체 vs 시점별 관계 빈도 비교 및 분석 

"""

# 한글 폰트 설정
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 파일 저장 코드
def save_fig(filename):
    plt.savefig(f'./stats_to_dataScience/data/img/{filename}_corona_2025.png', dpi=300, bbox_inches='tight')
    print(f"이미지가 저장되었습니다: {filename}.png")

print("---------------------년도별 뉴스 기사 빈수도 추출------------------------")

# [데이터, 통계] 총 건수 : 77508
keywords = ['데이터','통계']
#news_df = pd.read_pickle(f"./stats_to_dataScience/data/news_tokenized_{keywords}_2025.pkl")
news_df = pd.read_pickle(f"./stats_to_dataScience/data/filtered_news_['데이터', '통계']_2020-10-01_to_2025-09-30_2025.pkl")
print(news_df.info())

# 문자열인 date 컬럼을 날짜 형식으로 변환
news_df['date'] = pd.to_datetime(news_df['date'], errors='coerce')
yearly_counts = news_df['date'].dt.year.value_counts().sort_index()

x_years = yearly_counts.index.astype(int).tolist()
y_values = yearly_counts.values.tolist()

plt.plot(x_years, y_values, marker='o', markersize=8, color='#1f77b4', linewidth=2, linestyle='-')
plt.title('연도별 "데이터/통계" 관련 뉴스 기사 수 추이', fontsize=15, pad=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('기사 수 (건)', fontsize=12)
plt.xticks(x_years) 

# y축 범위를 데이터에 맞게 자동 조정 (0부터 시작)
plt.ylim(0, max(y_values) * 1.2)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 데이터 라벨링 (점 위에 숫자 표시)
for i, v in enumerate(y_values):
    plt.text(x_years[i], v + (max(y_values) * 0.03), f'{int(v):,}건', 
             ha='center', fontsize=10, fontweight='bold')

plt.savefig("./stats_to_dataScience/data/img/yearly_news_trend_corona_2025.png", dpi=300)
plt.tight_layout()
#plt.show()

print("---------------------학과명 명칭이 변경된 시점에서 두 그룹으로 나눈뒤 키워드 분석 : 2020년 10월 변경------------------------")
# 빈도수 비교 
def generate_compare_cloud(df, title, filename, colormap):
    # 단어 리스트 추출
    all_words = []
    for word_list in df['noun_contents']:
        all_words.extend(word_list)
    
    counts = Counter(all_words)

    # 워드클라우드 생성
    wc = WordCloud(
        font_path='malgun', 
        background_color='white',
        width=500, height=500,
        colormap=colormap,
        max_words=55
    ).generate_from_frequencies(counts)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.title(title, fontsize=25, pad=20)
    plt.axis('off')

    save_fig(filename) 
    plt.show() # 창 띄우기

    print("상위 50개 : ", counts.most_common(50))
    print("상위 10개 : ", counts.most_common(10))
    
    # 상위 키워드 반환 (막대그래프용 50개, 출력용 10개)
    return counts.most_common(50), counts.most_common(10)

# 데이터 그룹 나누기 
# 1. 날짜 데이터 형식 확인 및 그룹 분할
#split_date = pd.Timestamp('2020-09-30') # 학과 변경 날짜 시점
split_date = pd.Timestamp('2023-05-01') # 코로나 종식 시점

# 2020년 10월 이전 (기존 학과명 시기)
group_before = news_df[news_df['date'] < split_date]
# 2020년 10월 이후 (명칭 변경 및 데이터 강조 시기)
group_after = news_df[news_df['date'] >= split_date]

# 변경 전 기사 수: 29303건
# 변경 후 기사 수: 48205건
print(f"변경 전 기사 수: {len(group_before)}건") 
print(f"변경 후 기사 수: {len(group_after)}건") 

# 변경 전/후 워드 클라우드
bf_top50, bf_top10 = generate_compare_cloud(group_before, "변경전", 'wc_before_stat_corona_2025', 'YlGnBu')
af_top50, af_top10 = generate_compare_cloud(group_after, "변경후", 'wc_after_ds_corona_2025', 'Accent')

print("---------------------변경전 상위 키워드와 변경후 상위 키워드 뽑아 순위변화 확인------------------------")
def plot_top_keywords_bar(common_words, title, filename, color):
    # 데이터 준비: (단어, 빈도) 튜플 리스트를 데이터프레임으로 변환
    df = pd.DataFrame(common_words, columns=['Keyword', 'Count'])
    
    # 그래프 설정
    plt.figure(figsize=(10, 13))
    sns.barplot(x='Count', y='Keyword', data=df, palette=color)
    
    # 순위를 알 수 있도록 그래프 옆에 텍스트 표시
    for i, count in enumerate(df['Count']):
        plt.text(count, i, f'  {i+1}위', va='center', fontsize=13, color='gray')
    
    plt.title(title, fontsize=20, fontweight='bold', pad=20)
    plt.yticks(fontsize=15, fontweight='bold')
    plt.xlabel('출현 빈도', fontsize=15)
    plt.ylabel('키워드', fontsize=15)
    plt.tight_layout()
    
    # 이미지 저장 및 출력
    plt.savefig(f'./stats_to_dataScience/data/img/{filename}_1.png')
    plt.show()

# 변경 전 상위 키워드 vs 변경 후 상위 키워드 bar 그래프
plot_top_keywords_bar(bf_top10, "변경 전 상위 키워드 Top 50", "bar_rank_before_corona_2025", "Blues_d")
plot_top_keywords_bar(af_top10, "변경 후 상위 키워드 Top 50", "bar_rank_after_corona_2025", "Oranges_d")

print("---------------------전체 vs 시점별 연관성 그래프 : networkx------------------------")
def build_keyword_network(df, title, filename, top_n=30):
    # 1. 상위 키워드 추출 (너무 많은 단어는 그래프를 복잡하게 만듦)
    all_words = []
    for words in df['noun_contents']:
        all_words.extend(words)
    
    top_keywords = [word for word, count in Counter(all_words).most_common(top_n)]
    
    # 2. 동시 출현(Co-occurrence) 빈도 계산
    count_dict = Counter()
    for words in df['noun_contents']:
        # 상위 키워드에 포함된 단어들만 필터링
        filtered_words = [w for w in set(words) if w in top_keywords]
        # 한 기사 내에서 두 단어씩 조합 생성
        for pair in combinations(sorted(filtered_words), 2):
            count_dict[pair] += 1

    # 3. NetworkX 그래프 객체 생성
    G = nx.Graph()
    
    # 노드 추가 (빈도수에 비례한 크기 설정을 위해 빈도수 정보 포함)
    word_counts = Counter(all_words)
    for word in top_keywords:
        G.add_node(word, size=word_counts[word])

    # 엣지(선) 추가 (동시 출현 빈도가 일정 수준 이상인 경우만)
    # 데이터 양에 따라 min_cut 수치를 조절하세요 (예: 50회 이상 동시 출현)
    min_cut = df.shape[0] * 0.01  # 전체 기사의 1% 이상 동시 출현 기준
    for (node1, node2), weight in count_dict.items():
        if weight >= min_cut:
            G.add_edge(node1, node2, weight=weight)

    # 4. 시각화 설정
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(G, k=0.8, iterations=50) # 노드 배치 알고리즘
    
    # 노드 크기 계산 (최소/최대 크기 조정)
    node_sizes = [G.nodes[n]['size'] * 0.1 for n in G.nodes]
    
    # 엣지 굵기 계산
    weights = [G[u][v]['weight'] * 0.005 for u, v in G.edges()]

    # 그래프 그리기
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.6)
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='gray', alpha=0.3)
    
    # 레이블(글자) 크기 키우기
    nx.draw_networkx_labels(G, pos, font_family=font_name, font_size=16, font_weight='bold')

    plt.title(title, fontsize=25, pad=30)
    plt.axis('off')
    
    save_fig(filename)
    plt.show()

# 실행: 변경 전과 후 비교, 전체기간
build_keyword_network(group_before, "변경 전: 키워드 연관 네트워크", "network_before_corona_2025", top_n=25)
build_keyword_network(group_after, "변경 후: 키워드 연관 네트워크", "network_after_corona_2025", top_n=25)
build_keyword_network(news_df, "전체 기간: 키워드 연관 네트워크", "network_total_corona_2025", top_n=25)

print("---------------------전체 vs 시점별 관계 수 : networkx------------------------")
def compare_keyword_relations(total_df, before_df, after_df, top_n=10):
    def get_top_pairs(df):
        count_dict = Counter()
        top_words = [w for w, c in Counter([word for words in df['noun_contents'] for word in words]).most_common(top_n)]
        for words in df['noun_contents']:
            filtered = [w for w in set(words) if w in top_words]
            for pair in combinations(sorted(filtered), 2):
                count_dict[pair] += 1
        return count_dict.most_common(5)

    print(f"=== [전체 기간] 가장 강한 관계 Top 5 ===")
    for pair, score in get_top_pairs(total_df):
        print(f"{pair[0]} - {pair[1]} : {score}회 동시출현")

    print(f"\n=== [변경 전] 가장 강한 관계 Top 5 ===")
    for pair, score in get_top_pairs(before_df):
        print(f"{pair[0]} - {pair[1]} : {score}회 동시출현")

    print(f"\n=== [변경 후] 가장 강한 관계 Top 5 ===")
    for pair, score in get_top_pairs(after_df):
        print(f"{pair[0]} - {pair[1]} : {score}회 동시출현")

# 실행
compare_keyword_relations(news_df, group_before, group_after)