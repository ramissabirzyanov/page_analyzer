from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv
from page_analyzer.url import normalize_url
from page_analyzer.data_base import get_db_connect
from psycopg2.extras import DictCursor
import os
import validators


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def add_url():
    url = normalize_url(request.form.get('url'))
    if not validators.url(url) or len(url) > 255:
        flash('Некорректный URL', category='danger')
        return render_template('index.html'), 422
    conn = get_db_connect()
    conn.autocommit = True
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE urls.name=%s;", (url,))
        data_urls = cursor.fetchone()
        if data_urls:
            id = data_urls['id']
            flash('Страница уже существует', category='info')
            return redirect(url_for('url_page', id=id))
        cursor.execute(
            "INSERT INTO urls (name, created_at)\
            VALUES (%s, NOW())\
            RETURNING id;",
            (url,))
        id = cursor.fetchone()['id']
    flash('Страница успешно добавлена', category='success')
    return redirect(url_for('url_page', id=id))


@app.route('/urls', methods=['GET'])
def get_urls():
    conn = get_db_connect()
    conn.autocommit = True
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM urls;")
        urls = cursor.fetchall()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_page(id):
    conn = get_db_connect()
    conn.autocommit = True
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM urls WHERE urls.id=%s;", (id,))
        url = cursor.fetchone()
    return render_template('url.html', url=url)
