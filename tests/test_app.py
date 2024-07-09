# import requests
# from page_analyzer import data_base
# from page_analyzer.url import get_info
# from flask import url_for


# def test_main_page(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert "<title>Анализатор страниц</title>" in response.text


# def test_urls_page(client):
#     response = client.get('/urls')
#     assert response.status_code == 200


# def test_urls(client, test_urls, test_url_checks, url='https://letcode.in'):
#     response = requests.get(url)
#     data_base.save_to_db(test_urls, url, 'test_urls')
#     cursor_test_urls = test_urls.cursor()
#     cursor_test_urls.execute("SELECT * FROM test_urls\
#                              WHERE test_urls.name ='https://letcode.in'")
#     result_url = cursor_test_urls.fetchone()
#     url_page = client.get(f'/urls/{result_url[0]}')
#     info = get_info(response)
#     data_base.save_check_to_db(test_url_checks,
#                         result_url[0],
#                         info['code'],
#                         info['h1'],
#                         info['title'],
#                         info['description'],
#                         'test_url_checks')
#     cursor_test_url_checks = test_url_checks.cursor()
#     cursor_test_url_checks.execute(f"SELECT * FROM test_url_checks\
#                                    WHERE test_url_checks.url_id = {result_url[0]}")
#     result_check = cursor_test_url_checks.fetchone()
#     assert result_url is not None
#     assert url_page.status_code == 200
#     assert result_check is not None
#     assert client.post(url_for('check_url', id=result_url[0])).status_code == 302
