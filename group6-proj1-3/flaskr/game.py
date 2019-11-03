import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game

bp = Blueprint('game', __name__, url_prefix='/game')
my_db = db
# TODO add to wish list

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<string:game_url>', methods=('GET', 'POST'))
def game_page(game_url):
    conn = my_db.get_conn()
    gname = unquote(game_url)
    context = {}
    cursor = conn.execute("SELECT * FROM game WHERE gname='%s'" % gname)
    for result in cursor:
        context[Game.DESCRIPTION.value] = result[Game.DESCRIPTION.value]
        context[Game.GENRE.value] = result[Game.GENRE.value]
        context[Game.DATE.value] = result[Game.DATE.value]
        context[Game.PRICE.value] = result[Game.PRICE.value]
        context[Game.GNAME.value] = result[Game.GNAME.value]
    cursor.close()
    return render_template("game.html", **context)

