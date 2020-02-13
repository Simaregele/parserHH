from bs4 import BeautifulSoup
import requests
import csv



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
            vacancy_list.append(vac_link)

    # for i in vacancy_list:
    #     print(i)
    else:
        print('error')
    return vacancy_list

hh_parse(baseurl, headers)

na = 'NA'

def get_page_info(url, headers):
    session = requests.session()
    request = session.get(url, headers=headers)
    inner_soup = BeautifulSoup(request.content, 'lxml')
    work_dict = {}
    try:
        work_dict['title'] = inner_soup.find('h1', attrs={'data-qa': 'vacancy-title'}).text
    except:
        work_dict['title'] = na
    try:
        work_dict['salary'] = inner_soup.find('p', class_="vacancy-salary").text
    except:
        work_dict['salary'] = na
    try:
        work_dict['company_name'] = inner_soup.find('p', class_="vacancy-company-name-wrapper").text
    except:
        work_dict['company_name'] = na
    try:
        work_dict['work_exp'] = inner_soup.find('span', attrs={'data-qa': 'vacancy-experience'}).text
    except:
        work_dict['work_exp'] = na
    try:
        work_dict['job_location'] = inner_soup.find('span', attrs={'itemprop': 'jobLocation'}).text
    except:
        work_dict['job_location'] = na
    try:
        work_dict['duties'] = inner_soup.find('div', attrs={'data-qa': 'vacancy-description'}).find_all('ul')[0].text
    except:
        work_dict['duties'] = na

    try:
        skills = inner_soup.find_all('span', attrs={'data-qa: skills-element'})
        skills_list = []
        for skill in skills:
            print(skill.text)
            skills_list.append(skill.text)
        work_dict['skills'] = skills_list
    except:
        work_dict['skills'] = na

    try:
        work_dict['start_date'] = inner_soup.find('div', class_='vacancy-section').text
    except:
        work_dict['start_date'] = na
    return work_dict

header_list = ['title', 'salary', 'company_name', 'work_exp', 'job_location', 'duties',
               'skills', 'start_date']

def write_to_csv(list):
    with open('hh.csv', 'w') as file:
        writer = csv.DictWriter(file)
        writer.writeheader()
        writer.writerow(('Url', 'Title', 'Salary', 'CompName', 'Experience', 'JobLoc'))

for i in hh_parse(baseurl, headers):
    get_page_info(i, headers)
    print(get_page_info(i, headers))