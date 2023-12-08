from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect
)
from dotenv import load_dotenv
from page_analyzer.valid import validate_url, get_url_data
from page_analyzer.db import (
    get_urls_by_name,
    get_urls_by_id,
    get_urls_all,
    add_website,
    add_check
)
import os
from datetime import datetime
import requests
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv(".env")
load_dotenv(env_file)

load_dotenv('../.env')

def urls_post():
    url = request.form.get('url')
    validate = validate_url(url)

    url = validate['url']
    error = validate['error']

    if error:
        if error == 'This URL already exists':
            id = get_urls_by_name(url)['id']

            flash('Странница с таким URL уже существует', 'error')

            return redirect(url_for('url_show', id=id))
        else:
            flash('Некорректный URL адрес', 'error')

    error = validate['error']

    if error:
        if error == 'URL already exists':
            id = get_urls_by_name(url)['id']

            flash('Страница уже существует', 'alert-fact')

            return redirect(url_for('url_by_id', id=id))
        elif error == 'URL length = 0':
            flash('URL обязателен', 'alert-warning')

        elif error == 'Invalid URL name':
            flash('Некорректный URL', 'alert-warning')

        elif error == 'URL length > 255':
            flash('URL превышает 255 символов', 'alert-warning')

        messages = get_flashed_messages(with_categories=True)

        return render_template('index.html',
                               url=url,
                               messages=messages
                               ), 422

@app.post('/urls/<int:id>/checks')
def url_check(id):
    url = get_urls_by_id(id)['name']

    try:
        check = get_url_data(url)

        check['url_id'] = id
        check['checked_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_check(check)

        flash('Страница успешно проверена', 'alert-success')

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')

    return redirect(url_for(
        'url_by_id',
        id=id
    ))


if __name__ == '__main__':
    app.run()