import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import openpyxl


def db_read(path_to_db: str, sheet_name: str):
    return pd.read_excel(path_to_db, sheet_name=sheet_name)


def graph_bar_films_by_views(db, is_show: bool):
    """
    графический отчет «кластеризованная столбчатая диаграмма»
    для пары «качественный атрибут —качественный атрибут»,
    следует использовать matplotlib.pyplot.bar();
    """
    ser = db['Название Фильма'].value_counts()
    data_values = ser.array
    data_keys = list(ser.to_dict().keys())
    y_pos = np.arange(1, len(data_values)+1)

    fig, ax = plt.subplots()
    hbars = ax.barh(y_pos, data_values, align='center')
    ax.set_title('Фильмы по просмотрам')
    ax.set_xlabel('Количество просмотров')
    ax.set_ylabel('Место')
    ax.bar_label(hbars, labels=data_keys, label_type='center')
    ax.bar_label(hbars, fmt='%.2f', label_type='edge')
    if is_show:
        plt.show()
    else:
        return ax


def graph_bar_films_by_rating(db, is_show: bool):
    data = pd.pivot_table(db, values='Оценка', index='Название Фильма').to_dict()
    data = data['Оценка']
    data_keys = list(data.keys())
    y_pos = np.arange(1, 1 + len(data_keys))
    data_values = list(data.values())

    fig1, ax = plt.subplots()
    hbars = ax.barh(y_pos, data_values, align='center')
    ax.invert_yaxis()
    ax.set_xlabel('Оценка')
    ax.set_ylabel('Место')
    ax.set_title('Рейтинг фильмов')
    ax.bar_label(hbars, fmt='%.2f', label_type='edge')
    ax.bar_label(hbars, labels=data_keys, label_type='center')
    ax.set_xlim(right=10)
    if is_show:
        plt.show()
    else:
        return ax


def graph_hist_avg_marks(db, is_show: bool):
    """
    графический отчет «категоризированная гистограмма»
    для пары «количественный атрибут—качественный атрибут»,
    следует использовать matplotlib.pyplot.hist();
    """
    fig1, ax = plt.subplots()
    ax.hist(films_views(db))
    ax.set_title('Оценки по частоте')
    ax.set_ylabel('Количество фильмов')
    ax.set_xlabel('Количество просмотров')
    if is_show:
        plt.show()
    else:
        return ax


def graph_boxplot(db, is_show: bool):
    """
    графический отчет «категоризированная диаграмма Бокса-Вискера»
    для пары «количественный атрибут—качественный атрибут» ,
    следует использовать matplotlib.pyplot.boxplot();
    """
    ser = films_views(db)

    fig1, ax = plt.subplots()
    ax.set_title('Диаграмма Бокса-Вискера для среднего количеста просмотров')
    ax.set_ylabel('Количество просмотров')
    ax.boxplot(ser)
    if is_show:
        plt.show()
    else:
        return ax


def graph_scatter():
    """
    графический отчет «категоризированная диаграмма рассеивания»
    для двух количественных атрибутов и одного качественного атрибута,
    следует использовать matplotlib.pyplot.scatter().
    """


def films_views(database):
    """
        :param database: DataFrame, объединенная таблица данных:
        :return ser: Series, сводная таблица, отсортированная по Фильмы / Просмотры
    """
    ser = database['Название Фильма'].value_counts()
    return ser


def films_avg_ratings(database):
    """
        :param database: DataFrame, объединенная таблица данных:
        :return pivot: DataFrame, сводная таблица, отсортированная по Фильмы / Средняя оценка
    """
    pivot = pd.pivot_table(database, values='Оценка', index='Название Фильма')
    return pivot


def director_avg_ratings(database):
    """
        :param database: DataFrame, объединенная таблица данных:
        :return pivot: DataFrame, сводная таблица, отсортированная по Режиссер / Средняя оценка фильмов
    """
    pivot = pd.pivot_table(database, values='Оценка', index='Режиссер')
    return pivot


def users_email_subs(database):
    """
        :param database: DataFrame, объединенная таблица данных:
        :return user_info: DataFrame, сводная таблица, отсортированная по Пользователи / Email / Наличие подписки
    """
    user_info = pd.DataFrame(database, database.index, ['Имя пользователя', 'E-mail пользователя', 'Наличие Подписки'])
    # user_info = pd.crosstab(database, database.index, ['Имя пользователя', 'E-mail пользователя', 'Наличие подписки'])
    user_info = user_info.drop_duplicates(keep='first', subset=['Имя пользователя', 'E-mail пользователя', 'Наличие Подписки'])

    #print(database.index)
    return user_info




