# 2019/11/8
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_conn
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    conn = my_db.get_conn()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif conn.execute("SELECT account FROM Player P WHERE P.account = '%s'" % username).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            conn.execute("INSERT INTO Player (account, email) VALUES ('%s', '%s')" % (username, email))
            #conn.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        conn = my_db.get_conn()
        error = None
        user = conn.execute("SELECT * FROM Player P WHERE P.account = '%s'" % username).fetchone()

        if user is None:
            error = 'Incorrect username.'

        if error is None:
            session.clear()
            session['user_id'] = user['account']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        #g.user = conn.execute("SELECT account FROM Player P WHERE P.account = '%s'" % user_id).fetchone()
        g.user = user_id
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
