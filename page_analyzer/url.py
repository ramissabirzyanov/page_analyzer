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
    h1 = soup.find('h1').text
    title = soup.find('title').text
    description = soup.find('meta', attrs={'name': 'description'})['content']
    if h1:
        seo['h1'] = h1
    if title:
        seo['title'] = title
    if description:
        seo['description'] = description
    return seo
