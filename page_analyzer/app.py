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
from validator import validate_url
from page_analyzer.db import get_urls_by_name
import os


load_dotenv()

app = Flask(__name__)
	@@ -18,5 +26,38 @@ def hello():
    )


@app.post('/urls')
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

            flash('Страница уже существует', 'fact')

            return redirect(url_for('url_show', id=id))
        else:
            flash('Некорректный URL', 'error')

            if error == 'URL length = 0':
                flash('URL обязателен', 'error')
            elif error == 'URL length > 255 ':
                flash('URL превышает 255 символов', 'error')

            messages = get_flashed_messages(with_categories=True)



if __name__ == '__main__':
    app.run()