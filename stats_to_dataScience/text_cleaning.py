import re
import os

'''
텍스트 불용어 처리 클래스
'''
class TextCleaner :
    
    @staticmethod #불용어 파일 불려오기
    def load_stop_words(stopwords_file):
        with open(stopwords_file, 'r', encoding='utf-8') as file:
            stop_words = [line.strip() for line in file.readlines()]
        return stop_words
    
    @staticmethod #불용어 파일을 읽어서 불용어 처리
    def process_text_with_stop_words(stopwords_file, tokens):
        stop_words = TextCleaner.load_stop_words(stopwords_file)
        filtered_tokens = [token for token in tokens if token not in stop_words]
        return filtered_tokens
    
    @staticmethod #특수문자 제거
    def remove_special_characters(text):
        # 정규식을 사용하여 알파벳, 숫자, 한글만 남기고 나머지 제거
        cleaned_text = re.sub(r"[^a-zA-Z0-9가-힣\s]", "", text)
        return cleaned_text
    
    @staticmethod
    # 특수문자 제거 : 문자 전처리
    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()