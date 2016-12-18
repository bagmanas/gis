# -*- coding: utf-8 -*-
import urllib.request as rq
import urllib.parse as pa
import xml.etree.ElementTree as ET
import xml
import html
import sys
from lxml import html
import re
import requests
import utils
url_template = """http://www.gks.ru/dbscripts/munst/munst{}/DBInet.cgi"""
url_template2 = """http://www.gks.ru/scripts/db_inet2/passport/munr.aspx?base=munst{}"""

for i in range(1, 100):
    url = url_template.format(i)
df = {}
df["href"] = ['http://www.gks.ru/dbscripts/munst/munst99/DBInet.cgi']

r = requests.post("http://www.gks.ru/dbscripts/munst/munst99/DBInet.cgi",
                  data={'pl': [8112027]})

params = {'Format': 'CSV',
          'YearTo': 2016,
          'YearFrom': 2009,
          'Qry':{'Pokazateli':8112027,
                 'munr' :[111],
                 'tippos':10,
                 'oktmo':[111],
                 'mest':[],
                 'god':[],
                 'period':[]},
          'QryGm':[11],
          'QryFootNotes':'111',
          'YearsList':[111]
          }


qru_path = "/html/body/div[3]/div/font/center/input[1]"
qry_gm_path = "/html/body/div[3]/div/font/center/input[2]"
qry_foot_notes = "/html/body/div[3]/div/font/center/input[3]"
yeat_path = "/html/body/div[3]/div/font/center/input[4]"

html.open_in_browser(html.fromstring(r.text))
for url in df["href"]:
    try:
        page = rq.urlopen(url)
        tree = html.fromstring(page.read().decode('cp1251'))
        html.open_in_browser(tree)
        pro = tree.xpath('//*/tr/td[1]/span/img[@onclick]')
        urls = list()
        names = list()
        for p in pro:
            print(dir(p.xpath('@onclick')[0]))
            # url = 'http://zakupki.gov.ru'+nr(r_get_url.search(p.xpath('@onclick')[0]))
            # urls.append(url)
            # name = nr(r_trim.search(p.xpath('span/text()')[0]))
            # names.append(name)

        tdf = pd.DataFrame({"name": names, "url": urls})
        tdf["noticeId"] = nr(r_notice.search(url_params))
        pdf = pdf.append(tdf, ignore_index=True)
        # print(tdf)

    except rq.HTTPError as e:
        print(e.code)
pdf.to_csv("prot_list.csv")
