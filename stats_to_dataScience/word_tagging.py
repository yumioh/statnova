from konlpy.tag import Mecab, Okt

'''
DataPreprocessor 관련한 함수 모은 클래스

'''
class WordTagging:
    @staticmethod
    #mecab을 찾지 못하는 에러로 인한 절대 경로로 지정함 
    def noun_tagging(df) : #명사
        # mecab = Mecab()
        mecab = Mecab('C:\mecab\share\mecab-ko-dic')
        return df.apply(lambda x: [mecab.nouns(word) for word in x])
    
    @staticmethod
    def verb_tagging(df) : #동사
        mecab = Mecab('C:/mecab/share/mecab-ko-dic')
        parsed = mecab.pos(df)
        verbs = [word for word, pos in parsed if pos.startswith('VV')]  # VV는 동사
        return verbs
    
    @staticmethod
    def adjective_tagging(df) : #부사
        mecab = Mecab('C:/mecab/share/mecab-ko-dic')
        parsed = mecab.pos(df)
        adjectives = [word for word, pos in parsed if pos == 'VA']  # VV는 동사
        return adjectives

    @staticmethod
    # 동사 추출 함수
    def okt_verb_tagging(sentence): #동사
        okt = Okt()
        parsed = okt.pos(sentence)
        verbs = [word for word, pos in parsed if pos == 'Verb']  # Verb는 동사
        return verbs

    @staticmethod
    # 형용사 추출 함수
    def okt_adjective_tagging(sentence): #부사
        okt = Okt()
        parsed = okt.pos(sentence)
        adjectives = [word for word, pos in parsed if pos == 'Adjective']  # Adjective는 형용사
        return adjectives
    
    @staticmethod
    # 형용사 추출 함수
    def okt_noun_tagging(sentence): #명사
        okt = Okt()
        # 문자열에서 명사만 추출 (내부적으로 pos 분석 후 Noun만 반환)
        return okt.nouns(sentence)
    
    def okt_noun_tagging_remove_one_char(text):
        """
        text: 문자열(한 문장)
        return: 한 글자짜리 단어를 제거한 명사 리스트
        """
        okt = Okt()
        nouns = okt.nouns(text)  # 명사 추출
        # 길이가 1인 단어 제거
        filtered = [word for word in nouns if len(word) > 1]
        return filtered