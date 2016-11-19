# -*- coding: utf-8 -*-


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
