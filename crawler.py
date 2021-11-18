import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_movies_by_country(country_code, max_page=600):
    MOVIE_BASE_URL = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?nation={nation}&page={page}'
    REVIEW_BASE_URL = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page={page}'
    NAVER_FRANCE_MOVIE_LAST_PAGE = max_page

    movie_count = 0
    analyzed_movie_count = 0
    review_list = []

    for movie_page in range(1, NAVER_FRANCE_MOVIE_LAST_PAGE):
        try:
            print(movie_page)
            movie_url = MOVIE_BASE_URL.format(nation=country_code, page=movie_page)
            movie_res = requests.get(movie_url)

            if movie_res.status_code != 200:
                continue

            movie_soup = BeautifulSoup(movie_res.text, 'lxml')
            movies = []
            for a_tag in movie_soup.select('ul.directory_list > li > a'):
                movies.append((a_tag['href'].split('code=')[1], a_tag.get_text()))

            for (movie_code, movie_title) in movies:
                movie_count += 1

                review_first_page_url = REVIEW_BASE_URL.format(movie_code=movie_code, page=1)
                review_first_page_res = requests.get(review_first_page_url)
                review_first_page_soup = BeautifulSoup(review_first_page_res.text, 'lxml')
                review_count_el = review_first_page_soup.select_one('div.score_total > strong.total > em')

                if not review_count_el:
                    continue

                analyzed_movie_count += 1

                review_count_text = review_count_el.get_text()
                review_count = int(int(review_count_text.replace(',', '')) / 10) + 1

                for review_page in range(1, review_count + 1):
                    review_url = REVIEW_BASE_URL.format(movie_code=movie_code, page=review_page)
                    review_res = requests.get(review_url)

                    if review_res.status_code != 200:
                        continue

                    review_soup = BeautifulSoup(review_res.text, 'lxml')
                    lis = review_soup.select('div.score_result > ul > li')
                    for li in lis:
                        score = li.select_one('div.star_score > em').get_text()
                        comment_span = li.select('div.score_reple > p > span')
                        comment = (comment_span[1] if len(comment_span) > 1 else comment_span[0]).get_text().strip()
                        review_list.append((movie_title, score, comment))
        except:
            continue

    df = pd.DataFrame(review_list, columns=['title', 'score', 'comment'])
    df.to_csv(f'data/naver_movie_reviews_{country_code}.csv', encoding='utf-8', index=False)

    df = pd.DataFrame([[movie_count, analyzed_movie_count]], columns=['movie_count', 'analyzed_movie_count'])
    df.to_csv(f'data/naver_movie_reviews_{country_code}_count.csv', encoding='utf-8', index=False)


get_movies_by_country('KR', 108)
# get_movies_by_country('FR', 512)
