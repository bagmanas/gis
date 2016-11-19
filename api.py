__author__ = 'Bagman'
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin

api_entry = 'http://localhost:8080/geoserver/rest/'
credential = ('admin', 'geoserver')


def send_style_to_server(name, style):
    # Добавляем пустой стиль в базу
    resource = 'styles'
    payload = '<style><name>{}_style</name><filename>{}.sld</filename></style>'.format(
        name, name)
    request_url = urljoin(api_entry, resource)
    headers = {'content-type': 'text/xml'}

    r = requests.post(request_url,
                      data=payload,
                      headers=headers,
                      auth=credential)

    # Загружаем
    resource = 'styles/{}_style'.format(name)
    headers = {'content-type': 'application/vnd.ogc.sld+xml'}

    request_url = urljoin(api_entry, resource)
    r = requests.put(
        request_url,
        data=style,
        headers=headers,
        auth=credential
    )
    return r
