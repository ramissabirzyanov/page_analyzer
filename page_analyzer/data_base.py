import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import DictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connect():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


class URL_DB:
    def get_data_by_name(self, name):
        conn = get_db_connect()
        conn.autocommit = True
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.name=%s;", (name,))
            data = cursor.fetchone()
        return data
    
    def save_to_db(self, url):
        conn = get_db_connect()
        conn.autocommit = True
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
            "INSERT INTO urls (name, created_at)\
            VALUES (%s, NOW())",
            (url,))

    def get_id_by_name(self, name):
        conn = get_db_connect()
        conn.autocommit = True
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id FROM urls WHERE urls.name=%s;", (name,))
            id = cursor.fetchone()['id']
        return id
