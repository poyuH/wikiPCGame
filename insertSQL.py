import psycopg2
import json
import random


def insert_tuple(table, columns, value_form, values, pw):
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
    for iname in ['piano', 'guitar', 'violin', 'flute', 'drum']:
        values.append((iname, ))
    insert_tuple(table, columns, value_form, values)

def insert_musicgenre():
    table = 'musicgenre'
    columns = 'mgenre'
    value_form = "(%s)"
    values = []
    for mgenre in ['Rock', 'Electronic', 'Soul/R&B', 'Funk', 'Country', 'Reggae', 'Classical']:
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

    return


if __name__ == '__main__':
    insert_player()
