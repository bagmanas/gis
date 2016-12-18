# -*- coding: utf-8 -*-
import psycopg2
import requests
from lxml import html
import urllib.request as rq
connection_string = "dbname=student user=postgres password=postgres host=localhost port=5432"


def mean(iterable):
    return sum(iterable) / len(iterable)


def hamming(first, second):
    return sum(x != y for x, y in zip(first, second)) + abs(
        len(first) - len(second))


def get_data(file_name):
    data = []
    with open(file_name, 'r', encoding='cp1251') as csvfile:
        for line in csvfile:
            data.append(line.split(';'))
    return data[0], data[1:]


def oktmo_dict():
    answer = {}
    conn = psycopg2.connect(connection_string)

    cur = conn.cursor()
    cur.execute("""SELECT "oktmo_name", "oktmo_code" FROM adm4_region;""")
    for oktmo_name, oktmo_code in cur:
        answer[str(oktmo_name).strip().strip('"')] = oktmo_code

    cur = conn.cursor()
    cur.execute("""SELECT "oktmo_name", "oktmo_code" FROM adm6_district;""")
    for oktmo_name, oktmo_code in cur:
        answer[str(oktmo_name).strip().strip('"')] = oktmo_code


    cur = conn.cursor()
    cur.execute("""SELECT "oktmo_name", "oktmo_code" FROM adm8_municipal;""")
    for oktmo_name, oktmo_code in cur:
        answer[str(oktmo_name).strip().strip('"')] = oktmo_code

    return answer


if __name__ == '__main__':
    oktmo = oktmo_dict()
    url = "http://www.gks.ru/dbscripts/munst/munst99/DBInet.cgi"
    '/html/body/div[3]/div/font/center/table/tbody/tr[1]/td/form/table[3]/tbody/tr[2]/td/select/option'

    r = requests.post("http://www.gks.ru/dbscripts/munst/munst99/DBInet.cgi",
                  data={'pl': [8112027]})
    print(r.content)
    tree = html.fromstring(r.content.decode('cp1251'))
    # html.open_in_browser(tree)

    pro = tree.xpath(''' //*/td/select''')
    print(pro)

    munr = []
    oktm = []
    years = []
    pro = tree.xpath(''' //*/td/select[@name='munr']/option''')
    for p in pro:
        key = oktmo.get(p.text.strip().strip('"/').strip(), None)
        if key is not None:
            munr.append(key)

    print(munr)

    pro = tree.xpath(''' //*/td/select[@name='oktmo']/option''')
    for p in pro:
        key = oktmo.get(p.text.strip().strip('"/').strip(), None)
        if key is not None:
            oktm.append(key)

    print(oktm)

    pro = tree.xpath(''' //*/td/select[@name='god']/option''')
    for p in pro:
        years.append(p.text.strip())

    print(years)
