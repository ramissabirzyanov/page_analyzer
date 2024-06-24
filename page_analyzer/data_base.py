import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import DictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


CONNECTION = psycopg2.connect(DATABASE_URL)
CONNECTION.autocommit = True


class URL_DB:
    def get_data_by_name(self, name):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.name=%s;", (name,))
            data = cursor.fetchone()
        return data

    def save_to_db(self, url):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("INSERT INTO urls (name, created_at)\
                           VALUES (%s, NOW())",
                           (url,))

    def get_id_by_name(self, name):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id FROM urls WHERE urls.name=%s;", (name,))
            id = cursor.fetchone()['id']
        return id

    def get_urls(self):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT DISTINCT ON (urls.id)\
                           urls.id,\
                           urls.name,\
                           url_checks.created_at AS last_check,\
                           url_checks.status_code\
                           FROM urls LEFT JOIN url_checks\
                           ON urls.id = url_checks.url_id\
                           ORDER BY urls.id DESC;")
            urls = cursor.fetchall()
        return urls

    def get_data_by_id(self, id):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.id=%s;", (id,))
            data = cursor.fetchone()
        return data
    
    def save_check_to_db(self, url_id):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("INSERT INTO  url_checks (url_id, created_at)\
                           VALUES (%s, NOW())",
                           (url_id,))
    
    def get_check_by_url_id(self, url_id):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_checks.url_id=%s ORDER BY id DESC;", (url_id,))
            check = cursor.fetchall()
        return check
