import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from newspaper import Article


def scrape_blog(start_page: int, end_page: int):
    scraped_data = []
    base_url = "coin.space"
    main_page_url = 'https://coin.space/blog/page/'

    for page in tqdm(range(start_page, end_page)):
        current_url = main_page_url + str(page)
        html = requests.get(current_url).content
        soup = BeautifulSoup(html, features='html.parser')
        articles = soup.find_all('article')

        for index, article in enumerate(articles):
            article_dict = {
                'link': 'https://www.' + base_url + article.a['href'],
                'title': article.a.text,
                'author': article.p.text,
                'creation_time': article.find_all('div')[2].text.split('\n')[3],
                'text': ...
            }
            print(article_dict)
            try:
                newspaper_article_instance = Article(article_dict['link'])
                newspaper_article_instance.download()
                newspaper_article_instance.parse()
                article_dict['text'] = newspaper_article_instance.text
                # article_list = [article_dict['title'], article_dict['text']]
                scraped_data.append(article_dict['text'])
            except Exception as e:
                print(e)
    df = pd.DataFrame(scraped_data)
    df.to_csv(f'coin_space.csv')


scrape_blog(1, 2)
