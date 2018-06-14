
# coding: utf-8

# In[1]:


import nltk


# In[68]:


import math, sys
#from konlpy.tag import Twitter
class BayesianFilter1:
    """ 베이지안 필터 """
    def __init__(self):
        self.words = set() # 출현한 단어 기록
        self.word_dict = {} # 카테고리마다의 출현 횟수 기록
        self.category_dict = {} # 카테고리 출현 횟수 기록
    # 형태소 분석하기 --- (※1)
    def split(self, text):
        return text.split()
        results = []
        twitter = Twitter()
        # 단어의 기본형 사용
        malist = twitter.pos(text, norm=True, stem=True)
        for word in malist:
            # 어미/조사/구두점 등은 대상에서 제외 
            if not word[1] in ["Josa", "Eomi", "Punctuation"]:
                results.append(word[0])
        return results
    # 단어와 카테고리의 출현 횟수 세기 --- (※2)
    def inc_word(self, word, category):
        # 단어를 카테고리에 추가하기
        if not category in self.word_dict:
            self.word_dict[category] = {}
        if not word in self.word_dict[category]:
            self.word_dict[category][word] = 0
        self.word_dict[category][word] += 1
        self.words.add(word)
    def inc_category(self, category):
        # 카테고리 계산하기
        if not category in self.category_dict:
            self.category_dict[category] = 0
        self.category_dict[category] += 1
    
    # 텍스트 학습하기 --- (※3)
    def fit(self, text, category):
        """ 텍스트 학습 """
        word_list = self.split(text)
        for word in word_list:
            self.inc_word(word, category)
        self.inc_category(category)
    
    # 단어 리스트에 점수 매기기--- (※4)
    def score(self, words, category):
        score = math.log(self.category_prob(category))
        for word in words:
            score += math.log(self.word_prob(word, category))
        return score
    
    # 예측하기 --- (※5)
    def predict(self, text):
        best_category = None
        max_score = -sys.maxsize 
        words = self.split(text)
        score_list = []
        for category in self.category_dict.keys():
            score = self.score(words, category)
            score_list.append((category, score))
            if score > max_score:
                max_score = score
                best_category = category
        return best_category, score_list
    # 카테고리 내부의 단어 출현 횟수 구하기
    def get_word_count(self, word, category):
        if word in self.word_dict[category]:
            return self.word_dict[category][word]
        else:
            return 0
    # 카테고리 계산
    def category_prob(self, category):
        sum_categories = sum(self.category_dict.values())
        category_v = self.category_dict[category]
        return category_v / sum_categories
        
    # 카테고리 내부의 단어 출현 비율 계산 --- (※6)
    def word_prob(self, word, category):
        n = self.get_word_count(word, category) + 1 # ---(※6a)
        d = sum(self.word_dict[category].values()) + len(self.words)
        #print(sum(self.word_dict[category].values()))
        return n / d


# In[50]:


bf = BayesianFilter1()
# 텍스트 학습
bf.fit("파격 세일 - 오늘까지만 30% 할인", "광고")
bf.fit("쿠폰 선물 & 무료 배송", "광고")
bf.fit("현데계 백화점 세일", "광고")
bf.fit("봄과 함께 찾아온 따뜻한 신제품 소식", "광고")
bf.fit("인기 제품 기간 한정 세일", "광고")
bf.fit("오늘 일정 확인", "중요")
bf.fit("프로젝트 진행 상황 보고","중요")
bf.fit("계약 잘 부탁드립니다","중요")
bf.fit("회의 일정이 등록되었습니다.","중요")
bf.fit("오늘 일정이 없습니다.","중요")
# 예측
pre, scorelist = bf.predict("재고 정리 할인, 무료 배송")
print("결과 =", pre)
print(scorelist)


# In[132]:


import math, sys
#from konlpy.tag import Twitter
class BayesianFilter:
    """ 베이지안 필터 """
    def __init__(self):
        self.words = set() # 출현한 단어 기록
        self.categories = {} # 카테고리 출현 횟수 기록
        self.cfd = _
 
    # 텍스트 문장 학습하기 --- (※3)
    def sfit(self, data):
        """ 텍스트 학습 """
        train_data = []
        for s, c in data:
            for w in s.split():
                train_data.append((c, w))
                if c in self.categories :
                    self.categories[c] += 1
                else:
                    self.categories[c] = 1
                self.words.add(w)
        self.cfd = nltk.ConditionalFreqDist(train_data)

    # 텍스트 단어 학습하기 --- (※3)
    def fit(self, data):
        """ 텍스트 학습 """
        train_data = []
        for w, c in data:
            train_data.append((c, w))
            if c in self.categories :
                self.categories[c] += 1
            else:
                self.categories[c] = 1
            self.words.add(w)
        self.cfd = nltk.ConditionalFreqDist(train_data)

    # 단어 리스트에 점수 매기기--- (※4)
    def score(self, words, category):
        s_category = sum(self.categories.values())         
        score = math.log( self.categories[category] / s_category )
        for word in words:
            score += math.log( (self.cfd[category][word]+1) / (self.categories[category] + len(self.words)) )
        return score
    
    # 예측하기 --- (※5)
    def predict(self, text):
        best_category = None
        max_score = -sys.maxsize 
        words = text.split()
        score_list = []

        for category in self.categories:
            score = self.score(words, category)
            score_list.append((category, score))
            if score > max_score:
                max_score = score
                best_category = category
        return best_category, score_list
 


# In[54]:



# 텍스트 학습
train = (
("파격 세일 - 오늘까지만 30% 할인", "광고"), 
("쿠폰 선물 & 무료 배송", "광고"), 
("현데계 백화점 세일", "광고"), 
("봄과 함께 찾아온 따뜻한 신제품 소식", "광고"), 
("인기 제품 기간 한정 세일", "광고"),
("오늘 일정 확인", "중요"),
("프로젝트 진행 상황 보고","중요"),
("계약 잘 부탁드립니다","중요"),
("회의 일정이 등록되었습니다.","중요"),
("오늘 일정이 없습니다.","중요"))

bf = BayesianFilter()
bf.sfit( train) # sentence fit
# 예측
pre, scorelist = bf.predict("재고 정리 할인, 무료 배송")
print("결과 =", pre)
print(scorelist)
print(bf.categories)


# In[131]:


# 1. 기존 코드를 cfd를 사용하여 변경
# 2. fit 함수를 train data를 한꺼번에 받아서 처리하도록 변경
# 3. brown corpus에서 특정 카테고리의 데이터로 학습 
# 4. lala land와 god father의 영화 시나리오를 읽어서 학습 
# 5. wordnet으로 synset으로 학습
# 6. lemma, stopword 처리, lower()
# 7. wordnet.synsets

from nltk.corpus import brown 
wnl = nltk.WordNetLemmatizer()

# raw word + lower()
train = [ (word.lower(), genre)  for genre in ['religion','hobbies', 'romance']     for word in brown.words(categories=genre) ]

# stop word removal ==> romance
#train = [ (word, genre)  for genre in ['religion','hobbies', 'romance']     for word in brown.words(categories=genre) if word not in nltk.corpus.stopwords.words('english')]

# wordnet synset
#from nltk.corpus import wordnet as wn
#train = [ (wn.synsets(word)[0], genre)  for genre in ['religion','hobbies', 'romance']     for word in brown.words(categories=genre) if len(wn.synsets(word)) ]

# lemma
#train = [ (wnl.lemmatize(word), genre)  for genre in ['religion','hobbies', 'romance']     for word in brown.words(categories=genre) ]
bf = BayesianFilter()
#bf.fit(train[:1000]+train[-1000:])
bf.fit(train)
# 예측
print(bf.categories)
pre, scorelist = bf.predict(" go fishing with friends food ")
print("결과 =", pre)
print(scorelist)


# In[134]:


# 영화 시나리오 읽어서 학습 
from urllib import request
from nltk import word_tokenize
url = "http://www.imsdb.com/scripts/La-La-Land.html"
html = request.urlopen(url).read()
from bs4 import BeautifulSoup
raw = BeautifulSoup(html, 'lxml').get_text()
#raw = nltk.clean_html(html)
tokens = word_tokenize(raw)

train = [ (word, 'lala')  for word in tokens ]

url = "http://www.imsdb.com/scripts/Godfather.html"
html = request.urlopen(url).read()
#from bs4 import BeautifulSoup
raw = BeautifulSoup(html, 'lxml').get_text()
#raw = nltk.clean_html(html)
tokens = word_tokenize(raw)
train1 = [ (word, 'godfather')  for word in tokens ]

bf = BayesianFilter()
#bf.fit(train[:1000]+train[-1000:])
bf.fit(train+train1)
# 예측
print(bf.categories)
pre, scorelist = bf.predict(" cafe jazz la holywood")
print("결과 =", pre)
print(scorelist)


# In[137]:


# 영화 local file 읽어서 학습 
from nltk import word_tokenize

with open('lalaland.txt') as f:
    raw = f.read()

tokens = word_tokenize(raw)
train = [ (word, 'lala')  for word in tokens ]

with open('raiders.txt') as f:
    raw = f.read()

tokens = word_tokenize(raw)
train1 = [ (word, 'raiders')  for word in tokens ]

bf = BayesianFilter()
#bf.fit(train[:1000]+train[-1000:])
bf.fit(train+train1)
# 예측
print(bf.categories)

pre, scorelist = bf.predict(" cafe jazz la holywood")
print("결과 =", pre)
print(scorelist)

pre1, scorelist1 = bf.predict(" professor treasure cave ")
print("결과 =", pre1)
print(scorelist1)


# In[104]:


from nltk.corpus import brown 

train = [ (genre, word)  for genre in ['humor','science_fiction']     for word in brown.words(categories=genre) ]
bf = BayesianFilter1()
for i in train:
    bf.fit(i[1], i[0])
#print(train[:100]+train[-100:])
# 예측
pre, scorelist = bf.predict(" with  mars space ")
print("결과 =", pre)
print(scorelist)

