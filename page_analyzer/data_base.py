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
        #conn = get_db_connect()
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
            cursor.execute(
            "SELECT * FROM urls;")
            urls = cursor.fetchall()
        return urls
    
    def get_url_by_id(self, id):
        with CONNECTION.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
            "SELECT * FROM urls WHERE urls.id=%s;", (id,))
            url = cursor.fetchone()
        return url
