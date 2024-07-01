from urllib.parse import urlparse
from bs4 import BeautifulSoup


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_seo(res_text):
    seo = {
        'h1': '',
        'title': '',
        'description': '',
    }
    soup = BeautifulSoup(res_text, 'html.parser')
    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})
    if h1:
        seo['h1'] = h1.text
    if title:
        seo['title'] = title.text
    if description:
        seo['description'] = description['content']
    return seo
