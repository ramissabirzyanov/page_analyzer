from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv
from page_analyzer.url import normalize_url, get_info
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
    url = normalize_url(request.form.get('url'))
    if not validators.url(url) or len(url) > 255:
        flash('Некорректный URL', category='danger')
        return render_template('index.html'), 422
    conn = data_base.get_connection(DATABASE_URL)
    data_urls = data_base.get_data_by_name(conn, url)
    if data_urls:
        flash('Страница уже существует', category='info')
        return redirect(url_for('url_page', id=data_urls['id']))
    data_base.save_to_db(conn, url)
    new_data = data_base.get_data_by_name(conn, url)
    flash('Страница успешно добавлена', category='success')
    return redirect(url_for('url_page', id=new_data['id']))


@app.route('/urls', methods=['GET'])
def show_urls():
    conn = data_base.get_connection(DATABASE_URL)
    urls = data_base.get_urls(conn)
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
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
    url_info = get_info(response)
    data_base.save_check_to_db(conn, id, **url_info)
    flash('Страница успешно проверена', category='success')
    return redirect(url_for('url_page', id=id))
