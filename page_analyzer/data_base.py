import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection(db):
    connection = psycopg2.connect(db)
    connection.autocommit = True
    return connection


def get_url_by_name(connection, name):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"SELECT * FROM urls WHERE urls.name='{name}';")
        url = cursor.fetchone()
    return url


def insert_to_db(connection, name, table='urls'):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"INSERT INTO {table} (name, created_at)\
                        VALUES ('{name}', NOW());")


def get_urls(connection):
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


def get_data_by_id(connection, id):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"SELECT * FROM urls WHERE urls.id='{id}';")
        data = cursor.fetchone()
    return data


def insert_check_to_db(connection,
                       url_id, code, h1, title, description,
                       table='url_checks'):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"INSERT INTO {table} (\
            url_id, status_code, h1, title, description, created_at)\
            VALUES ({url_id}, {code}, '{h1}', '{title}', '{description}', NOW());")


def get_check_by_url_id(connection, url_id):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"SELECT * FROM url_checks\
                        WHERE url_checks.url_id={url_id}\
                        ORDER BY id DESC;")
        check = cursor.fetchall()
    return check
