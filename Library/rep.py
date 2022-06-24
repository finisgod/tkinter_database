# -*- coding: utf-8 -*-
"""
Различные операции с базой данных

Автор: Поляков К. Л.
"""

def ret_key(db, sel=2):
    """
    Извлечение имен или фамилий
    Входные атрибуты:
    db - база данных
    sel имя (2) по умолчанию, фамилия (1)
    Возвращает:
    список списков [[key, имя или фамилия]]
    Автор: Поляков К. Л.
    """
    z = [[key, '=>', db[key]['имя'].split()[-sel]] for key in db]
    return z


def ret_field(db, field="дети"):
    """
    Извлечение заданного поля
    Входные атрибуты:
    db - база данных
    field имя поля
    Возвращает:
    список списков ["имя", "поле"]
    Автор: Поляков К. Л.
    """
    z = [[record["имя"], record[field]] for record in db.values()]
    return z

# Вариант - вывод в файл и по значениям, а не по ключам
def statement(db, depart="маркетинг"):
    """
    Создает ведомость по департаменту
    Входные атрибуты:
    db - база данных
    field имя поля
    Возвращает:
    список списков ["ФИО", "зарплата"]
    Автор: Поляков К. Л.
    """
    z = [[db[key]["имя"], db[key]["зарплата"]] for key in db 
             if db[key]["департамент"] == "маркетинг"]
    return z

dep = "финансы"
# Список количеств детей
child = lambda x: [len(x[key]["дети"]) for key in x 
                   if x[key]["департамент"] == dep]
# Список списков: ["имя"б количество детей]
childn = lambda x: [[x[key]["имя"], len(x[key]["дети"])] for key in x 
                     if x[key]["департамент"] == dep]

def wage(db, depart="маркетинг"):
    """
    Извлекает зарплаты по департаменту
    Входные атрибуты:
    db - база данных
    depart имя поля
    Возвращает:
    список ["зарплата"]
    Автор: Поляков К. Л.
    """
    z = [db[key]["зарплата"] for key in db 
             if db[key]["департамент"] == depart]
    return z

ave = lambda x: sum(x)/len(x)
var = lambda x: sum([key*key for key in x])/(len(x)-1) - ave(x)**2

def wage_rep(db, depart="маркетинг"):
    from math import sqrt
    x = wage(db, depart)
    return [ave(x), var(x), sqrt(var(x))]
