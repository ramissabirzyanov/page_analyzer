import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connect():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
