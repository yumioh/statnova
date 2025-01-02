import re
import os

class TextCleaner :
    
    @staticmethod
    def load_stop_words(stopwords_file):
        #불용어 파일 읽어 오기 
        with open(stopwords_file, 'r', encoding='utf-8') as file:
            stop_words = [line.strip() for line in file.readlines()]
        return stop_words
    
    @staticmethod
    def process_text_with_stop_words(stopwords_file, tokens):
        #불용어 파일 불려오는 함수
        stop_words = TextCleaner.load_stop_words(stopwords_file)
        filtered_tokens = [token for token in tokens if token not in stop_words]
        return filtered_tokens
    
    @staticmethod
    def remove_special_characters(text):
        # 정규식을 사용하여 알파벳, 숫자, 한글만 남기고 나머지 제거
        cleaned_text = re.sub(r"[^a-zA-Z0-9가-힣\s]", "", text)
        return cleaned_text