import psycopg2
import json
import random

MGENGRES = ['Rock', 'Electronic', 'Soul/R&B', 'Funk', 'Country', 'Reggae', 'Classical']
INSTRUMENTS = ['piano', 'guitar', 'violin', 'flute', 'drum']
PAYMENTS = ['money', 'cheque', 'debit', 'credit', 'bank transfers']

def insert_tuple(table, columns, value_form, values, pw='5882'):
    conn = psycopg2.connect(host='35.243.220.243', database='proj1part2', user='ph2587', password=pw)
    cur = conn.cursor()
    for v in values:
        sql = "INSERT INTO %s (%s) VALUES" % (table, columns)
        sql += value_form
        try:
            cur.execute(sql, v)
        except (Exception, psycopg2.DatabaseError) as error:
            if type(error) is not psycopg2.errors.UniqueViolation and\
                    type(error) is not psycopg2.errors.NotNullViolation:
                print(type(error))
                print(error)
        conn.commit()
    cur.close
    conn.close()

def read_tuple(query, pw='5882'):
    conn = psycopg2.connect(host='35.243.220.243', database='proj1part2', user='ph2587', password=pw)
    cur = conn.cursor()
    rows = []
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cur.close()
    conn.close()
    return rows

def update_tuple(table, value_col, value, condition_col, condition, pw='5882'):
    conn = psycopg2.connect(host='35.243.220.243', database='proj1part2', user='ph2587', password=pw)
    cur = conn.cursor()
    sql = 'UPDATE %s SET %s=' % (table, value_col)
    sql += '%s'
    sql += 'WHERE %s=' % condition_col
    sql += '%s'
    try:
        cur.execute(sql, (value, condition))
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    conn.commit()
    cur.close
    conn.close()

def read_list(path):
    with open(path) as f:
        d = json.load(f)
    return d

def escape_quotation(s):
    if not s or len(s) == 0 or type(s) is not str:
        return None
    new_s = ''
    for char in s:
        if char == '\'':
            new_s += '\'\''
        else:
            new_s += char
    return new_s

def insert_games():
    table = 'game'
    columns = 'gname, description, genre, date, price'
    value_form = "(%s, %s, %s, %s, %s)"
    for char in ['Numerical']:
        path = 'List_of_PC_games_(%s).json' % char
        d = read_list(path)
        values = []
        for name in d:
            price = random.random() * 40.0
            values.append((escape_quotation(name), escape_quotation(d[name].get('description')), d[name].get('genre'), d[name].get('date_release'), price))
        insert_tuple(table, columns, value_form, values)

def insert_developers():
    path = 'vidio_game_developer.json'
    table = 'developer'
    columns = 'dname, started, location'
    d = read_list(path)
    values = []
    value_form = "(%s, %s, %s)"
    for dname in d:
        year = d[dname]['found_year']
        date = None
        if year:
            date = '%s-01-01' % str(year)
        values.append((dname, date, escape_quotation(d[dname]['city'])))
    insert_tuple(table, columns, value_form, values)

def insert_produce():
    table = 'produce'
    columns = 'gname, dname'
    value_form = "(%s, %s)"
    path = 'List_of_PC_games_(%s).json' % 'Numerical'
    d = read_list(path)
    values = []
    for name in d:
        values.append((escape_quotation(name), escape_quotation(d[name].get('developer'))))
    insert_tuple(table, columns, value_form, values)
    for char in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        path = 'List_of_PC_games_(%s).json' % char
        d = read_list(path)
        values = []
        for name in d:
            price = random.random() * 40.0
            values.append((escape_quotation(name), escape_quotation(d[name].get('developer'))))
        insert_tuple(table, columns, value_form, values)

def insert_composer():
    table = 'composer'
    columns = 'cname'
    value_form = "(%s)"
    path = 'List_of_PC_games_(%s).json' % 'Numerical'
    d = read_list(path)
    values = []
    for name in d:
        values.append((escape_quotation(d[name].get('composer')),))
    insert_tuple(table, columns, value_form, values)
    for char in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        path = 'List_of_PC_games_(%s).json' % char
        d = read_list(path)
        values = []
        for name in d:
            values.append((escape_quotation(d[name].get('composer')), ))
        insert_tuple(table, columns, value_form, values)

def insert_dub():
    table = 'dub'
    columns = 'gname, cname'
    value_form = "(%s, %s)"
    path = 'List_of_PC_games_(%s).json' % 'Numerical'
    d = read_list(path)
    values = []
    for name in d:
        values.append((name, escape_quotation(d[name].get('composer'))))
    insert_tuple(table, columns, value_form, values)
    for char in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        path = 'List_of_PC_games_(%s).json' % char
        d = read_list(path)
        values = []
        for name in d:
            values.append((name, escape_quotation(d[name].get('composer'))))
        insert_tuple(table, columns, value_form, values)

def insert_producer():
    table = 'producer'
    columns = 'pname'
    value_form = "(%s)"
    path = 'List_of_PC_games_(%s).json' % 'Numerical'
    d = read_list(path)
    values = []
    for name in d:
        values.append((escape_quotation(d[name].get('producer')), ))
    insert_tuple(table, columns, value_form, values)
    for char in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        path = 'List_of_PC_games_(%s).json' % char
        d = read_list(path)
        values = []
        for name in d:
            values.append((escape_quotation(d[name].get('producer')), ))
        insert_tuple(table, columns, value_form, values)

def insert_notablework():
    table = 'notablework'
    columns = 'gname, pname'
    value_form = "(%s, %s)"
    path = 'List_of_PC_games_(%s).json' % 'Numerical'
    d = read_list(path)
    values = []
    for name in d:
        values.append((name, escape_quotation(d[name].get('producer'))))
    insert_tuple(table, columns, value_form, values)
    for char in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        path = 'List_of_PC_games_(%s).json' % char
        d = read_list(path)
        values = []
        for name in d:
            values.append((name, escape_quotation(d[name].get('producer'))))
        insert_tuple(table, columns, value_form, values)

def insert_instrument():
    table = 'instrument'
    columns = 'iname'
    value_form = "(%s)"
    values = []
    for iname in INSTRUMENTS:
        values.append((iname, ))
    insert_tuple(table, columns, value_form, values)

def insert_musicgenre():
    table = 'musicgenre'
    columns = 'mgenre'
    value_form = "(%s)"
    values = []
    for mgenre in MGENGRES:
        values.append((mgenre, ))
    insert_tuple(table, columns, value_form, values)

def insert_player():
    table = 'player'
    columns = 'account, name, age, country, email'
    value_form = "(%s, %s, %s, %s, %s)"
    values = []
    for i in range(10):
        values.append(('test%s' % str(i), str(i), 18+i, 'Taiwan', 'test%s@gamil.com' % str(i)))
    insert_tuple(table, columns, value_form, values)

def insert_canplay_hasperformed(is_canplay):
    cnames = read_tuple('SELECT c.cname FROM composer c')
    if is_canplay:
        table = 'canplay'
        columns = 'cname, iname'
        choices = INSTRUMENTS
    else:
        table = 'hasperformed'
        columns = 'cname, mgenre'
        choices = MGENGRES
    value_form = "(%s, %s)"
    values = []
    for cname in cnames:
        values.append((cname, random.choice(choices)))
    insert_tuple(table, columns, value_form, values)

def insert_attend_transaction():
    table = 'attend_transaction'
    columns = 'tid, timestamp, account, payment '
    value_form = "(%s, %s, %s, %s)"
    values = []
    for i in range(10):
        values.append((str(i), '2019-10-%s'% (i+9), 'test%s' % str(i), random.choice(PAYMENTS)))
    insert_tuple(table, columns, value_form, values)

def insert_contain():
    table = 'contain'
    columns = 'tid, gname'
    value_form = "(%s, %s)"
    values = []
    gnames = read_tuple('SELECT g.gname FROM game g')
    for i in range(10):
        values.append((str(i), random.choice(gnames)))
        if i < 6:
            values.append((str(i), random.choice(gnames)))
    insert_tuple(table, columns, value_form, values)

def update_price():
    table = 'attend_transaction'
    tuples = read_tuple('SELECT c.tid, sum(g.price) FROM contain c, game g WHERE g.gname=c.gname GROUP BY c.tid')
    for tid, price in tuples:
        update_tuple(table, 'price', price, 'tid', tid)

def insert_wish_list():
    accounts = read_tuple('SELECT p.account from player p')
    gnames = read_tuple('SELECT g.gname from game g')
    table = 'wish_list'
    columns = 'gname, account'
    values = []
    value_form = '(%s, %s)'
    for account in accounts:
        values.append((random.choice(gnames), account))
    insert_tuple(table, columns, value_form, values)



if __name__ == '__main__':
    insert_wish_list()
