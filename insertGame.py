import psycopg2


def insert_tuple():
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute(sql, (value1,value2))

