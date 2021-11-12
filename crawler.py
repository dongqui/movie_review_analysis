import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = 'https://movie.naver.com/movie/point/af/list.naver?&page={page}'
review_list = []
for page in range(1, 1001):
    url = BASE_URL.format(page=page)
    res = requests.get(url)

    if res.status_code != 200:
        continue

    soup = BeautifulSoup(res.text, 'lxml')
    tds = soup.select('table.list_netizen > tbody > tr > td.title')

    for td in tds:
        title = td.select_one('a.movie').get_text()
        score = td.select_one('div.list_netizen_score > em').get_text()
        comment = td.select_one('br').next_sibling.strip()
        review_list.append((title, score, comment))

df = pd.DataFrame(review_list, columns=['title', 'score', 'comment'])
df.to_csv('data/naver_movie_reviews.csv', encoding='utf-8', index=False)

