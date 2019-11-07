import functools
from sqlalchemy import text
from urllib.parse import quote, unquote
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game

bp = Blueprint('index', __name__)
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<int:page_num>', methods=('GET', 'POST'))
@bp.route('/', methods=('GET', 'POST'))
def home_page(page_num=0, query=None):
    conn = my_db.get_conn()
    if not query:
        cursor = conn.execute("SELECT gname FROM game ORDER BY date LIMIT 10 OFFSET %s;" % (10*page_num))
    else:
        cursor = conn.execute(text(query))
    name_urls = []
    for result in cursor:
        name_urls.append((result[Game.GNAME.value], '/game/' + quote(result[Game.GNAME.value])))
    cursor.close()
    context = {}
    context['name_urls'] = name_urls
    print(name_urls)
    context['next_page'] = page_num + 1
    context['previous_page'] = page_num - 1
    return render_template("index.html", **context)

@bp.route('/search', methods=('GET', 'POST'))
def search():
    query = "SELECT gname FROM game WHERE gname LIKE '%%%s%%' ORDER BY date" % request.form['name']
    return home_page(query=query)

