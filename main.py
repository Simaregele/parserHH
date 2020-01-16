from bs4 import BeautifulSoup
import requests



# use + for query
query = "машинное+обучение" # use + for query
# area: moscow - 1, spb - 2
area = 1
# page number, start from 0
page = 0

baseurl = f"https://hh.ru/search/vacancy?clusters=true&area={area}&enable_snippets=true&salary=&st=searchVacancy&text={query}&page={page}"

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}



def hh_parse(base_url, headers):
    vacancy_list = []
    urls = []
    urls.append(baseurl)
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f"https://hh.ru/search/vacancy?clusters=true&area={area}&enable_snippets=true&salary=&st=searchVacancy&text={query}&page={i}"
                if url not in urls:
                    urls.append(url)

        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        div_vac = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for vac in div_vac:
            vac_link = vac.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            vacancy_list.append({'vac_link': vac_link})

    for i in vacancy_list:
        print(i)
    else:
        print('error')
    return vacancy_list

hh_parse(baseurl, headers)


