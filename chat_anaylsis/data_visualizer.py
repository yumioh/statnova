from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import font_manager
import os

''''
데이터 시각화를 위한 클래스
- 워드클라우드 

'''
class DataVisualizer : 

    # #데이터프레임으로부터 워드 클라우드를 생성하는 함수
    # def create_wordcloud(df, font_path, image_path, width=800, height=400, background_color='white', max_words=60):
    #     # 모든 토큰을 하나의 리스트로 합치기
    #     all_tokens = [token for tokens in df['content'] for token in tokens]
    #     # all_tokens = [token for tokens in tokens_column for token in eval(tokens)]

    #     # 단어 빈도 계산
    #     word_freq = Counter(all_tokens)

    #     # 워드 클라우드 생성
    #     wordcloud = WordCloud(
    #         font_path=font_path, 
    #         width=width, 
    #         height=height, 
    #         background_color=background_color, 
    #         colormap = "YlGnBu",
    #         max_words=max_words
    #         ).generate_from_frequencies(word_freq)
        
    #     #print(plt.colormaps())

    #     # 워드 클라우드 이미지를 파일로 저장
    #     wordcloud.to_file(image_path)

    @staticmethod
    def create_wordcloud(df, font_path, image_path, width=800, height=400, background_color='white', max_words=60):
        """
        데이터프레임으로부터 워드클라우드를 생성하고 저장.
        """
                
        # # 마스크 이미지 불러오기 및 변환
        # icon = Image.open('./chat_anaylsis/data/mask1.png').convert("L")  # 단일 채널로 변환
        # mask = np.array(icon)  # 넘파이 배열로 변환

        # 모든 토큰을 하나의 리스트로 합치기
        all_tokens = [token for tokens in df['content'] for token in tokens]

        # 단어 빈도 계산
        word_freq = Counter(all_tokens)
        
        print(word_freq.most_common(40))

        # 워드 클라우드 생성
        wordcloud = WordCloud(
            font_path=font_path,
            width=width,
            height=height,
            background_color=background_color,
            colormap="YlGnBu",
            max_words=max_words,
        ).generate_from_frequencies(word_freq)

        # 워드 클라우드 이미지를 파일로 저장
        wordcloud.to_file(image_path)
        print(f"워드클라우드가 {image_path}에 저장되었습니다.")