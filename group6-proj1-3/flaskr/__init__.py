import os
# accessible as a variable in index.html:
from flask import Flask, request, render_template, redirect, Response
from . import db
from . import index


def create_app(test_config=None):
    # create and configure the app
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, instance_relative_config=True, template_folder=tmpl_dir)
    my_db = db

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # connects to our database
    @app.before_request
    def before_request():
        my_db.start()

    # close our database
    @app.teardown_request
    def teardown_request(exception):
        my_db.close(exception)

    """
    # register home page as blueprint
    app.register_blueprint(index.bp)
    """

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        conn = my_db.get_conn()
        cursor = conn.execute("SELECT cname FROM composer")
        names = []
        for result in cursor:
          names.append(result['cname'])  # can also be accessed using result[0]
        cursor.close()
        context = dict(data = names)
        return render_template("index.html", **context)

    @app.route('/')
    def home_page():
        return index.home_page(my_db)

    @app.route('/add', methods=['POST'])
    def search():
        return index.search(my_db, request)


    return app
