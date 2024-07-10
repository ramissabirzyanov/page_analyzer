from urllib.parse import urlparse
from bs4 import BeautifulSoup


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_page_data(response):
    res_text = response.text
    url_info = {
        'code': None,
        'h1': '',
        'title': '',
        'description': '',
    }
    soup = BeautifulSoup(res_text, 'html.parser')
    code = response.status_code
    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})
    url_info['code'] = code
    if h1:
        url_info['h1'] = h1.text
    if title:
        url_info['title'] = title.text
    if description:
        url_info['description'] = description['content']
    return url_info
