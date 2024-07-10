from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv
from page_analyzer.utils import normalize_url, get_page_data
from page_analyzer import data_base
import os
import validators
import requests


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url_name = normalize_url(request.form.get('url'))
    if not validators.url(url_name) or len(url_name) > 255:
        flash('Некорректный URL', category='danger')
        return render_template('index.html'), 422
    conn = data_base.get_connection(DATABASE_URL)
    url = data_base.get_url_by_name(conn, url_name)
    if url:
        flash('Страница уже существует', category='info')
        return redirect(url_for('url_page', id=url['id']))
    data_base.insert_to_db(conn, url_name)
    new_url = data_base.get_url_by_name(conn, url_name)
    flash('Страница успешно добавлена', category='success')
    return redirect(url_for('url_page', id=new_url['id']))


@app.route('/urls', methods=['GET'])
def show_urls():
    conn = data_base.get_connection(DATABASE_URL)
    urls = data_base.get_urls(conn)
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def url_page(id):
    conn = data_base.get_connection(DATABASE_URL)
    url_data = data_base.get_data_by_id(conn, id)
    checks = data_base.get_check_by_url_id(conn, id)
    return render_template('url.html', url=url_data, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    conn = data_base.get_connection(DATABASE_URL)
    url_data = data_base.get_data_by_id(conn, id)
    try:
        response = requests.get(url_data['name'])
        response.raise_for_status()
    except Exception:
        flash('Произошла ошибка при проверке', category='danger')
        return redirect(url_for('url_page', id=id))
    url_info = get_page_data(response)
    data_base.insert_check_to_db(conn, id, **url_info)
    flash('Страница успешно проверена', category='success')
    return redirect(url_for('url_page', id=id))
