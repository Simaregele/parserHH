from bs4 import BeautifulSoup
import requests



# use + for query
search_query = "машинное+обучение" # use + for query
# area: moscow - 1, spb - 2
area = 1
# page number, start from 0
page = 0

url = f"https://hh.ru/search/vacancy?clusters=true&area={area}&enable_snippets=true&salary=&st=searchVacancy&text={search_query}&page={page}"

headers = {'accept': '*/*', 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}



page = requests.get(url)
def hh_parse(base_url, headers):
    session = requests.Session()
    requests = session.get(base_url, headers)

soup_page = BeautifulSoup(page.text, 'html-parser')

vacancy_card = soup_page.find_all(class_="vacancy-serp-item")
