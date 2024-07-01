import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor, RealDictRow


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)
connection.autocommit = True


class URL_DB:
    def get_data_by_name(self, name):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.name=%s;", (name,))
            data = cursor.fetchone()
        return data

    def save_to_db(self, url, table='urls'):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"INSERT INTO {table} (name, created_at)\
                           VALUES (%s, NOW())",
                           (url,))

    def get_id_by_name(self, name):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id FROM urls WHERE urls.name=%s;", (name,))
            id = cursor.fetchone()['id']
        return id

    def get_urls(self):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT DISTINCT ON (urls.id)\
                           urls.id,\
                           urls.name,\
                           url_checks.created_at AS last_check,\
                           url_checks.status_code\
                           FROM urls LEFT JOIN url_checks\
                           ON urls.id = url_checks.url_id\
                           ORDER BY urls.id DESC;")
            urls = []
            for row in cursor.fetchall():
                urls.append(
                    RealDictRow({k: '' if v is None else v for k, v in row.items()})
                )
        return urls

    def get_data_by_id(self, id):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.id=%s;", (id,))
            data = cursor.fetchone()
        return data

    def save_check_to_db(self, url_id, code, h1, title, descr, table='url_checks'):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"INSERT INTO {table} (\
                           url_id, status_code, h1, title, description, created_at)\
                           VALUES (%s, %s, %s, %s, %s, NOW());",
                           (url_id, code, h1, title, descr,))

    def get_check_by_url_id(self, url_id):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks\
                           WHERE url_checks.url_id=%s\
                           ORDER BY id DESC;", (url_id,))
            check = cursor.fetchall()
        return check
