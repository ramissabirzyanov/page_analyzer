from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv
from page_analyzer.url import normalize_url
from .data_base import URL_DB
from .url import get_seo
import os
import validators
import requests


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
    db = URL_DB()
    data_urls = db.get_data_by_name(url)
    if data_urls:
        id = data_urls['id']
        flash('Страница уже существует', category='info')
        return redirect(url_for('url_page', id=id))
    db.save_to_db(url)
    id = db.get_id_by_name(url)
    flash('Страница успешно добавлена', category='success')
    return redirect(url_for('url_page', id=id))


@app.route('/urls', methods=['GET'])
def get_urls():
    db = URL_DB()
    urls = db.get_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_page(id):
    db = URL_DB()
    url_data = db.get_data_by_id(id)
    checks = db.get_check_by_url_id(id)
    return render_template('url.html', url=url_data, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    db = URL_DB()
    url_data = db.get_data_by_id(id)
    try:
        response = requests.get(url_data['name'])
        response.raise_for_status()
        code = response.status_code
        seo_data = get_seo(response.text)
        title = seo_data['title']
        h1 = seo_data['h1']
        desctiption = seo_data['description']
        db.save_check_to_db(id, code, h1, title, desctiption)
        flash('Страница успешно проверена', category='success')
        return redirect(url_for('url_page', id=id))
    except Exception:
        flash('Произошла ошибка при проверке', category='danger')
        return redirect(url_for('url_page', id=id))
