import requests
from page_analyzer.data_base import URL_DB
from page_analyzer.url import get_seo


def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "<title>Анализатор страниц</title>" in response.text


def test_urls_page(client):
    response = client.get('/urls')
    assert response.status_code == 200


# def test_urls(client, test_urls, test_url_checks, url='https://letcode.in'):
#     response = requests.get(url)
#     db = URL_DB()
#     db.save_to_db(url, 'test_urls')
#     cursor_test_urls = test_urls.cursor()
#     cursor_test_urls.execute("SELECT * FROM test_urls\
#                              WHERE test_urls.name ='https://letcode.in'")
#     result_url = cursor_test_urls.fetchone()
#     url_page = client.get(f'/urls/{result_url[0]}')
#     seo = get_seo(response.text)
#     db.save_check_to_db(result_url[0],
#                         response.status_code,
#                         seo['h1'],
#                         seo['title'],
#                         seo['description'],
#                         'test_url_checks')
#     cursor_test_url_checks = test_url_checks.cursor()
#     cursor_test_url_checks.execute(f"SELECT * FROM test_url_checks\
#                                    WHERE test_url_checks.url_id = {result_url[0]}")
#     result_check = cursor_test_url_checks.fetchone()
#     assert result_url is not None
#     assert url_page.status_code == 200
#     assert result_check is not None
