from flask import Flask, request, render_template, redirect, Response
from sqlalchemy import text


def home_page(db, query=None):
    conn = db.get_conn()
    print(query)
    if not query:
        cursor = conn.execute("SELECT gname FROM game ORDER BY date LIMIT 10 OFFSET 0")
    else:
        cursor = conn.execute(query)
    names = []
    for result in cursor:
      names.append(result['gname'])
    cursor.close()
    context = dict(data = names)
    return render_template("index.html", **context)

def search(db, request):
    query = "SELECT gname FROM game WHERE gname LIKE '%%%s%%' ORDER BY date" % request.form['name']
    return home_page(db, query=text(query))

