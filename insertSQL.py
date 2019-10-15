import psycopg2
import json
import random


def insert_tuple(table, columns, value_form, values, pw='5882'):
    conn = psycopg2.connect(host='35.243.220.243', database='proj1part2', user='ph2587', password=pw)
    cur = conn.cursor()
    for v in values:
        sql = "INSERT INTO %s (%s) VALUES" % (table, columns)
        sql += value_form
        try:
            cur.execute(sql, v)
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
    if not s:
        return s
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

if __name__ == '__main__':
    return
