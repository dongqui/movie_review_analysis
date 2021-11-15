import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from konlpy.tag import Mecab
from tqdm import tqdm

df = pd.read_csv('./data/naver_movie_reviews.csv')
df['label'] = np.select([df.score <= 5, df.score > 5], [0, 1])

mecab = Mecab()
print(mecab.morphs('와 이런 것도 상품이라고 차라리 내가 만드는 게 나을 뻔'))
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

X_train = []


# def tokenize(data):
#     for sentence in tqdm(data['comment']):
#         tokenized_sentence = okt.morphs(sentence, stem=True)  # 토큰화
#         stopwords_removed_sentence = [word for word in tokenized_sentence if word not in stopwords]  # 불용어 제거
#         X_train.append(stopwords_removed_sentence)


def pre_processing(data):
    data.drop_duplicates(subset=['comment'], inplace=True)  # 중복 제거
    data['comment'] = data['comment'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '')  # 한글만
    data['comment'] = data['comment'].str.replace('^ +', '')
    data['comment'].replace('', np.nan, inplace=True)
    data.dropna(how='any')
    return data


train_data, test_data = map(pre_processing, train_test_split(df, test_size=0.25, random_state=42))
print(train_data.isnull().sum())
