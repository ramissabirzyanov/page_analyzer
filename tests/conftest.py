import pytest
# import psycopg2
# import os
from page_analyzer.app import app
# from dotenv import load_dotenv


# load_dotenv()
# TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


# @pytest.fixture
# def test_urls():
#     connection = psycopg2.connect(TEST_DATABASE_URL)
#     connection.autocommit = True
#     with connection.cursor() as cursor:
#         cursor.execute('''CREATE TABLE test_urls (
#                        id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
#                        name VARCHAR(255) UNIQUE,
#                        created_at DATE default NOW());''')
#         yield connection


# @pytest.fixture
# def test_url_checks():
#     connection = psycopg2.connect(TEST_DATABASE_URL)
#     connection.autocommit = True
#     with connection.cursor() as cursor:
#         cursor.execute('''CREATE TABLE test_url_checks(
#                 id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
#                 url_id BIGINT REFERENCES test_urls(id) NOT NULL,
#                 status_code BIGINT,
#                 h1 VARCHAR(255),
#                 title VARCHAR(255),
#                 description TEXT,
#                 created_at DATE default NOW());''')
#         yield connection
#         cursor.execute('''DROP TABLE test_url_checks;''')
#         cursor.execute('''DROP TABLE test_urls;''')
