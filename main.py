__author__ = 'Bagman'
# -*- coding: utf-8 -*-
import psycopg2
import pprint
from collections import defaultdict


def get_data(file_name):
    data = []
    with open(file_name, 'r', encoding='cp1251') as csvfile:
        for line in csvfile:
            data.append(line.split(';'))
    return data[0], data[1:]


def mean(x):
    return sum(x) / len(x)


def hamming(first, second):
    return sum(x != y for x, y in zip(first, second)) + abs(
        len(first) - len(second))


def make_map_region(region_from_db, region_from_file):
    """
    Принемает регионы из БД, и регионы из файлов
    Возращает отображение регионов из файла в регионы в БД
    :param region_from_db:
    :param region_from_file:
    :return:
    """
    answer = {}
    for region_file in region_from_file:
        for region_db in region_from_db:
            dist = hamming(region_file, region_db)
            if dist < 2 or region_db.find(
                    region_file) != -1 or region_file.find(region_db) != -1:
                assert region_file not in answer, 'Error'
                answer[region_file] = region_db

    answer.update({'Kамчатская область': 'Камчатский край',
                   'Чувашская Республика': 'Чувашия',
                   'Республика Северная Осетия-Алания': 'Северная Осетия - Алания',
                   'Чукотский авт. округ': 'Чукотский автономный округ',
                   'Читинская область': 'Забайкальский край',
                   'Еврейская авт. область': 'Еврейская автономная область',
                   'Республика Mарий Эл': 'Марий Эл',
                   'Республика Саха(Якутия)': 'Республика Саха (Якутия)'})
    return answer


def add_column(cursor, table, name, type):
    sql = """ ALTER TABLE {} ADD {}  {};"""
    cursor.execute(sql.format(table, name, type))


def type_definition(value):
    try:
        float(str(value).replace(',', '.'))
        return 'numeric'
    except Exception:
        return 'text'


def file_prepare(file, new_name):
    conn = psycopg2.connect(
        "dbname=student user=postgres password=postgres host=localhost port=5432")
    cur = conn.cursor()
    cur.execute("""SELECT distinct("name") FROM adm4_region;""")
    region_from_table = set(record[0] for record in cur)
    cur.close()

    colum_name, data = get_data(file)
    reg_file = set(row[2] for row in data)
    reg_file_to_db = make_map_region(region_from_table, list(reg_file))

    print('+')
    with open(new_name, 'w') as output:
        print(';'.join(colum_name), end='', file=output)
        for row in data:
            if row[2] in reg_file_to_db:
                row[2] = reg_file_to_db[row[2]]
                print(';'.join(row), end='', file=output)


def add_data_base(table, columns, data):
    connection_string = "dbname=student user=postgres password=postgres host=localhost port=5432"
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    for i, column in enumerate(columns):
        # Добавляем колонку в БД
        add_column(cur, table, column, type_definition(data[0][i]))
        data_for_sql = defaultdict(list)
        # Берем данные из этой колонки
        for row in data:
            key = row[2].strip().strip('"')
            data_for_sql[key].append(float(row[i].replace(',', '.')))

        add_data = {}
        # Считаем среднее
        for key in data_for_sql:
            add_data[key] = mean(data_for_sql[key])




if __name__ == '__main__':
    file_prepare('./data/2013-04.txt', 'new_f')

    colum_name, data = get_data('./data/2013-04.txt')
    money = defaultdict(list)
    for row in data:
        key = row[2].strip().strip('"')
        money[key].append(float(row[11].replace(',', '.')))

    reg_file_to_db = make_map_region(region_from_table, list(money.keys()))

    add_money = {}
    for key in money:
        if key in reg_file_to_db:
            add_money[reg_file_to_db[key]] = mean(money[key])

    pp = pprint.PrettyPrinter()
    pp.pprint(add_money)

    for key, value in add_money.items():
        cur.execute(
            """UPDATE adm4_region set average_income={} where "name"='{}'""".format(
                value, key))
    conn.commit()
    cur.close()

