# -*- coding: utf-8 -*-
from add_data_base import add_file_in_data_base
from style_generator.style_gen import make_style
from api import send_style_to_server



if __name__ == '__main__':
    res = add_file_in_data_base('adm4_region', './data/2013-04.txt')
    for key, value in res.items():
        style = make_style(value, key.strip('"'))
        send_style_to_server('{}_style'.format(key.strip('"')),  style)