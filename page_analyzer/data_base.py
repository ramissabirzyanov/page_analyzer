import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection(db):
    connection = psycopg2.connect(db)
    connection.autocommit = True
    return connection


class URL_DB:
    def get_data_by_name(self, connection, name):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.name=%s;", (name,))
            data = cursor.fetchone()
        return data

    def save_to_db(self, connection, url, table='urls'):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"INSERT INTO {table} (name, created_at)\
                           VALUES (%s, NOW())",
                           (url,))

    def get_id_by_name(self, connection, name):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id FROM urls WHERE urls.name=%s;", (name,))
            id = cursor.fetchone()['id']
        return id

    def get_urls(self, connection):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
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

    def get_data_by_id(self, connection, id):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE urls.id=%s;", (id,))
            data = cursor.fetchone()
        return data

    def save_check_to_db(self, connection,
                         url_id, code, h1, title, description,
                         table='url_checks'):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"INSERT INTO {table} (\
                           url_id, status_code, h1, title, description, created_at)\
                           VALUES (%s, %s, %s, %s, %s, NOW());",
                           (url_id, code, h1, title, description,))

    def get_check_by_url_id(self, connection, url_id):
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks\
                           WHERE url_checks.url_id=%s\
                           ORDER BY id DESC;", (url_id,))
            check = cursor.fetchall()
        return check
