import requests
import codecs
from bs4 import BeautifulSoup as BS
from user_agent import generate_user_agent


__all__ = (
    'get_vac_from_indeed',
    'get_vac_from_olx',
    'get_vac_from_jooble',
    'get_vac_from_nofluffjobs',
)

USER_AGENT = generate_user_agent(os=None, navigator=None, platform=None, device_type=None)

headers = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


def get_vac_from_indeed(url):
    # url = 'https://pl.indeed.com/jobs?q=python%20junior&l=Warszawa%2C%20mazowieckie&vjk=e9f46c76587e2d7b'
    jobs = []
    errors = []

    domain = 'https://pl.indeed.com'
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='mosaic-provider-jobcards')
        if main_div:
            div_lst = main_div.find_all('a', attrs={'class': 'resultWithShelf'})
        # print(soup)
            for d in div_lst:
                title = d.find('h2').text
                if 'nowa oferta' in title:
                    title = d.find('h2').text[:11] + ' (new)'
                
                href = domain + d['href']
                description = d.find('div', attrs={'class': 'job-snippet'}).text
                city = d.find('div', attrs={'class': 'companyLocation'}).text
                company = d.find('span', attrs={'class': 'companyName'}).text

                jobs.append(
                    {'title': title, 'url': href, 'description': description, 'city': city, 'company': company}
                )
        else:
            errors.append({'url': url, 'title': 'Main div does not exitst'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})
    return jobs, errors



def get_vac_from_olx(url):
    # url = 'https://www.olx.pl/praca/informatyka/warszawa/q-python/'
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        table = soup.find('table', id='offers_table')
        if table:
            tr_lst = table.find_all('tr', attrs={'class': 'wrap'})
        # print(soup)
            for div in tr_lst:
                title = div.find('h3').text
                
                href = div.a['href']
                description = div.find('span', attrs={'class': 'price-label'}).text
                city = div.find('small', attrs={'class': 'breadcrumb'}).text

                jobs.append(
                    {'title': title, 'url': href, 'description': description, 'city': city, 'company': 'no name'}
                )
        else:
            errors.append({'url': url, 'title': 'Table does not exitst'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})
    return jobs, errors


def get_vac_from_jooble(url):
    # url = 'https://pl.jooble.org/SearchResult?date=3&rgns=Warszawa&ukw=junior%20python'
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', attrs={'class': 'infinite-scroll-component'})
        if main_div:
            articles = main_div.find_all('article', id=True)

            for art in articles:
                title = art.find('h2').text
                
                href = art.a['href']
                description = art.find('div', attrs={'class': '_037ff'}).text
                city = art.find('div', attrs={'class': '_88a24'}).text
                company = art.find('p', attrs={'class': 'e2601'}).text

                jobs.append(
                    {'title': title, 'url': href, 'description': description, 'city': city, 'company': company}
                )
        else:
            errors.append({'url': url, 'title': 'Main div does not exitst'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})
    return jobs, errors


def get_vac_from_nofluffjobs(url, city=None, language=None):
    domain = 'https://nofluffjobs.com'

    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'main-content__outlet'})
            if main_div:
                div_lst = main_div.find_all('a', attrs={'class': 'posting-list-item--backend'})
                for div in div_lst:
                    href = div['href']
                    title = div.find('h3', attrs={'class': 'posting-title__position'})
                    company = div.find('span', attrs={'class': 'd-block'})
                    description = div.find('span', attrs={'class': 'salary'})

                    jobs.append({
                        'title': title.text ,
                        'url': domain + href,
                        'description': description.text,
                        'company': company.text,
                        # 'city_id': city,
                        # 'language_id': language,
                    })
            else:
                errors.append({
                    'url': url,
                    'title': 'Div does not exists',
                })
        else:
            errors.append({
                'url': url,
                'title': 'Page do not response',
            })
    return jobs, errors

        

# if __name__ == '__main__':
#     url = 'https://nofluffjobs.com/pl/praca-it/warszawa/backend?criteria=seniority%3Djunior%20requirement%3Dpython&page=1'
#     jobs, errors = get_vac_from_nofluffjobs(url)
#     with codecs.open('work.json', 'w', 'utf-8') as f:
#         f.write(str(jobs))
