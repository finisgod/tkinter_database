import tkinter as tk
from tkinter import *  # Для вкладок
from tkinter import ttk  # Для вкладок
import Scripts.DB as DB
from Scripts.UI import parser , UI_Table
from Scripts.UI.UI_CustomEntry import EntryWithPlaceholder
from Scripts.UI.UI_Table import Table

excel_path = parser.read_config().DIRECTORY_PATH + "\\Data\\DB.xlsx"
# CONST FOR PARSER
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 600

COLOR_ITEM_R = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
COLOR_ITEM_G = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
COLOR_ITEM_B = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R

COLOR_ITEM_TEXT_R = parser.read_config().TABLE_ITEM_TEXT_COLOR_R
COLOR_ITEM_TEXT_G = parser.read_config().TABLE_ITEM_TEXT_COLOR_G
COLOR_ITEM_TEXT_B = parser.read_config().TABLE_ITEM_TEXT_COLOR_B

FONT_STYLE = parser.read_config().FONT_STYLE
FONT_SIZE = 10

NUM_OF_COLUMNS = 7

# NOT FOR PARSER
WIDTH_OF_COLUMNS = int(WINDOW_WIDTH / ((FONT_SIZE / 1.3) * NUM_OF_COLUMNS + 1) + 1)  # zalupa
"""
    Инициализация главного экрана
"""
root = tk.Tk()
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()
x = (ws / 2) - (WINDOW_WIDTH / 2)
y = (hs / 2) - (WINDOW_HEIGHT / 2)
# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
root.title("Путеводитель маркетолога")
root.configure(background=parser.read_config().APP_COLOR)
"""
    Инициализация переменных с иконками
"""
# ICONS
ico_up_arrow = PhotoImage(file=r'icons\up_arrow.png')
ico_up_arrow = ico_up_arrow.subsample(10, 10)

ico_down_arrow = PhotoImage(file=r'icons\down_arrow.png')
ico_down_arrow = ico_down_arrow.subsample(10, 10)

ico_search = PhotoImage(file=r'icons\search.png')
ico_search = ico_search.subsample(20, 20)

ico_save = PhotoImage(file=r'icons\save.png')
ico_save = ico_save.subsample(10, 10)

ico_top_arrow = PhotoImage(file=r'icons\top_arrow.png')
ico_top_arrow = ico_top_arrow.subsample(10, 10)

ico_bottom_arrow = PhotoImage(file=r'icons\bottom_arrow.png')
ico_bottom_arrow = ico_bottom_arrow.subsample(10, 10)

"""
    Инициализация элемента для добавления новой строки
"""
def entry_list_frame(root):
    entry_list = []
    entry_frame = tk.Frame(root)
    for i in range(11):
        entry_list.append(EntryWithPlaceholder(entry_frame, list(table.df_out.keys())[i]))
        # entry_list[i].insert(0, list(db.keys())[i])
        entry_list[i].grid(row=0, column=i)

    empty_label = tk.Label(entry_frame, text=' ', font=(FONT_STYLE, 18))
    empty_label.grid(row=0, column=12)
    entry_butt = tk.Button(entry_frame, font=(FONT_STYLE, FONT_SIZE), text="Добавить строку",
                           command=lambda: table.new_line(entry_list))
    entry_butt.grid(row=0, column=13)
    entry_frame.pack()

"""
    Метод для удаления строки
"""
def delete_line(root):
    delete_frame = tk.Frame(root)
    empty_label = tk.Label(delete_frame, text='Введите номер строки для удаления', font=(FONT_STYLE, FONT_SIZE))
    empty_label.grid(row=0, column=0)
    delete_entry = EntryWithPlaceholder(delete_frame, "№")
    delete_entry.grid(row=0, column=1)
    delete_butt = tk.Button(delete_frame, font=(FONT_STYLE, FONT_SIZE), text="Удалить строку",
                            command=lambda: (table.deleteRow(int(delete_entry.get())),
                                             delete_entry.configure(
                                                 background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
                                             , delete_entry.delete(0, END)
                                             , delete_entry.put_placeholder()) if delete_entry.get().isdigit()
                            else delete_entry.configure(background="red")
                            )
    delete_butt.grid(row=0, column=2)
    delete_frame.pack(pady=10)

"""
    Методы для построения графических отчетов
"""
def graph_buttons(window):
    tk.Label(window, text='').pack(pady=50)
    fbv_btn = tk.Button(window, text="График фильмов по просмотрам",
                        command=lambda: DB.graph_bar_films_by_views(table.df_out, True),
                        font=(FONT_STYLE, FONT_SIZE))
    fbv_btn.pack()

    fbr_btn = tk.Button(window, text="График фильмов по рейтингу",
                        command=lambda: DB.graph_bar_films_by_rating(table.df_out, True),
                        font=(FONT_STYLE, FONT_SIZE))
    fbr_btn.pack()

    am_btn = tk.Button(window, text="График средних оценок",
                       command=lambda: DB.graph_hist_avg_marks(table.df_out, True),
                       font=(FONT_STYLE, FONT_SIZE))
    am_btn.pack()

    bxp_btn = tk.Button(window, text="Диаграмма Бокса-Вискера для среднего количеста просмотров",
                        command=lambda: DB.graph_boxplot(table.df_out, True),
                        font=(FONT_STYLE, FONT_SIZE))
    bxp_btn.pack()


def films_views(window):
    # DB
    ser = DB.films_views(table.df_out)
    ser = ser.to_dict()
    keys_list = list(ser.keys())

    # Fill table

    my_game = ttk.Treeview(window)
    my_game['columns'] = ("Название фильма", "Количество просмотров")

    my_game.column("#0", width=0, stretch='NO')
    my_game.column("Название фильма", anchor=CENTER, width=int(WINDOW_WIDTH / 2 - 50))
    my_game.column("Количество просмотров", anchor=CENTER, width=int(WINDOW_WIDTH / 2 - 50))

    my_game.heading("#0", text="", anchor=CENTER)
    my_game.heading("Название фильма", text="Название фильма", anchor=CENTER)
    my_game.heading("Количество просмотров", text="Количество просмотров", anchor=CENTER)

    for i in range(len(keys_list)):
        my_game.insert(parent='', index='end', iid=i, text='',
                       values=(keys_list[i], ser[keys_list[i]]))

    my_game.pack(pady=10)


def films_avg_ratings(window):
    pivot = DB.films_avg_ratings(table.df_out)
    pivot_dst = pivot.to_dict()
    pivot_dst = pivot_dst['Оценка']
    pivot_keys = list(pivot_dst.keys())

    my_game = ttk.Treeview(window)
    my_game['columns'] = ("Название фильма", "Рейтинг")

    my_game.column("#0", width=0, stretch='NO')
    my_game.column("Название фильма", anchor=CENTER, width=int(WINDOW_WIDTH / 2 - 50))
    my_game.column("Рейтинг", anchor=CENTER, width=int(WINDOW_WIDTH / 2 - 50))

    my_game.heading("#0", text="", anchor=CENTER)
    my_game.heading("Название фильма", text="Название фильма", anchor=CENTER)
    my_game.heading("Рейтинг", text="Рейтинг", anchor=CENTER)

    for i in range(len(pivot_keys)):
        my_game.insert(parent='', index='end', iid=i, text='',
                       values=(pivot_keys[i], pivot_dst[pivot_keys[i]]))

    my_game.pack(pady=10)


def director_avg_ratings(window):
    pivot_frame = tk.Frame(window)
    pivot = DB.director_avg_ratings(table.df_out)

    pivot_dst = pivot.to_dict()
    pivot_dst = pivot_dst['Оценка']

    pivot_keys = list(pivot_dst.keys())

    my_game = ttk.Treeview(window)
    my_game['columns'] = ("Режиссер", "Рейтинг")

    my_game.column("#0", width=0, stretch='NO')
    my_game.column("Режиссер", anchor=CENTER, width=int(WINDOW_WIDTH / 2 - 50))
    my_game.column("Рейтинг", anchor=CENTER, width=int(WINDOW_WIDTH / 2 - 50))

    my_game.heading("#0", text="", anchor=CENTER)
    my_game.heading("Режиссер", text="Режиссер", anchor=CENTER)
    my_game.heading("Рейтинг", text="Рейтинг", anchor=CENTER)

    for i in range(len(pivot_keys)):
        my_game.insert(parent='', index='end', iid=i, text='',
                       values=(pivot_keys[i], pivot_dst[pivot_keys[i]]))

    my_game.pack(pady=10)


def users_email_subs(window):
    pivot = DB.users_email_subs(table.df_out)
    pivot_dst = pivot.to_dict()

    my_game = ttk.Treeview(window)
    my_game['columns'] = ("Имя пользователя", "E-mail пользователя", "Наличие Подписки")

    my_game.column("#0", width=0, stretch='NO')
    my_game.column("Имя пользователя", anchor=CENTER, width=int(WINDOW_WIDTH / 3 - 50))
    my_game.column("E-mail пользователя", anchor=CENTER, width=int(WINDOW_WIDTH / 3 - 50))
    my_game.column("Наличие Подписки", anchor=CENTER, width=int(WINDOW_WIDTH / 3 - 50))

    my_game.heading("#0", text="", anchor=CENTER)
    my_game.heading("Имя пользователя", text="Имя пользователя", anchor=CENTER)
    my_game.heading("E-mail пользователя", text="E-mail пользователя", anchor=CENTER)
    my_game.heading("Наличие Подписки", text="Наличие Подписки", anchor=CENTER)

    user = list(pivot_dst['Имя пользователя'].items())
    email = list(pivot_dst['E-mail пользователя'].items())
    subs = list(pivot_dst['Наличие Подписки'].items())

    for i in range(len(pivot_dst['Имя пользователя'])):
        my_game.insert(parent='', index='end', iid=i, text='',
                       values=(user[i][1], email[i][1], subs[i][1]))

    my_game.pack(pady=10)

"""
    Метод для обновления данных во всех вкладках
"""
def update_table(tabControl):
    global tabs
    for i in tabs:
        i.destroy()

    tab_graph = ttk.Frame(tabControl)
    tab_films_views = ttk.Frame(tabControl)
    tab_films_avg_ratings = ttk.Frame(tabControl)
    tab_director_avg_ratings = ttk.Frame(tabControl)
    tab_users_email_subs = ttk.Frame(tabControl)

    tabControl.add(tab_graph, text='Графики')
    tabControl.add(tab_films_views, text='Просмотры фильмов')
    tabControl.add(tab_films_avg_ratings, text='Рейтинги фильмов')
    tabControl.add(tab_director_avg_ratings, text='Рейтинги режиссеров')
    tabControl.add(tab_users_email_subs, text='Информация о пользователях')
    tabControl.pack(expand=1, fill="both")

    tabs = [tab_graph,
            tab_films_views, tab_films_avg_ratings,
            tab_director_avg_ratings, tab_users_email_subs]

    graph_buttons(tab_graph)
    films_views(tab_films_views)
    films_avg_ratings(tab_films_avg_ratings)
    director_avg_ratings(tab_director_avg_ratings)
    users_email_subs(tab_users_email_subs)


def footer(root, tabs, tab_contr):
    label = tk.Label(root, text='Для создания новой строки введите данные', font=(FONT_STYLE, FONT_SIZE))
    label.pack()
    entry_list_frame(root)
    delete_line(root)

"""
    Инициализация вкладок
"""
tabControl = ttk.Notebook(root)

tab_main = ttk.Frame(tabControl)
tab_graph = ttk.Frame(tabControl)
tab_films_views = ttk.Frame(tabControl)
tab_films_avg_ratings = ttk.Frame(tabControl)
tab_director_avg_ratings = ttk.Frame(tabControl)
tab_users_email_subs = ttk.Frame(tabControl)

tabs = [tab_graph,
        tab_films_views, tab_films_avg_ratings,
        tab_director_avg_ratings, tab_users_email_subs]

tabControl.add(tab_main, text='База данных')
tabControl.add(tab_graph, text='Графики')
tabControl.add(tab_films_views, text='Просмотры фильмов')
tabControl.add(tab_films_avg_ratings, text='Рейтинги фильмов')
tabControl.add(tab_director_avg_ratings, text='Рейтинги режиссеров')
tabControl.add(tab_users_email_subs, text='Информация о пользователях')
tabControl.pack(expand=1, fill="both")

"""
    Инициализация кнопок для работы с таблицей
"""
tk.Button(tab_main, text="Up", font=(FONT_STYLE, FONT_SIZE), image=ico_up_arrow,
          command=lambda: table.scrollUp()).place(x=WINDOW_WIDTH - 50, y=50)
tk.Button(tab_main, text="Down", font=(FONT_STYLE, FONT_SIZE), image=ico_down_arrow,
          command=lambda: table.scrollDown()).place(x=WINDOW_WIDTH - 50,
                                                    y=160)
tk.Button(tab_main, text="Save", font=(FONT_STYLE, FONT_SIZE), image=ico_save,
          command=lambda: (table.saveTable(table.currentRow), update_table(tabControl))).place(
    x=WINDOW_WIDTH - 50, y=100)
tk.Button(tab_main, text="Top", font=(FONT_STYLE, FONT_SIZE), image=ico_top_arrow,
          command=lambda: table.scrollTop()).place(x=WINDOW_WIDTH - 50, y=0)
tk.Button(tab_main, text="Bottom", font=(FONT_STYLE, FONT_SIZE), image=ico_bottom_arrow,
          command=lambda: table.scrollBottom()).place(
    x=WINDOW_WIDTH - 50, y=220)
tk.Button(tab_main, text="Go to", font=(FONT_STYLE, FONT_SIZE), image=ico_search, command=lambda: (
    table.scrollTo(int(search_entry.get())),
    search_entry.configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}'
                           , fg=f'#{COLOR_ITEM_TEXT_R:02x}{COLOR_ITEM_TEXT_G:02x}{COLOR_ITEM_TEXT_B:02x}'),
    search_entry.delete(0, END)) if search_entry.get().isdigit()
else search_entry.configure(background="red")).place(x=WINDOW_WIDTH - 50, y=380)
search_entry = Entry(tab_main, font=(FONT_STYLE, FONT_SIZE), width=4,
                     background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}'
                     , fg=f'#{COLOR_ITEM_TEXT_R:02x}{COLOR_ITEM_TEXT_G:02x}{COLOR_ITEM_TEXT_B:02x}'
                     )

search_entry.place(x=WINDOW_WIDTH - 50, y=360)

table = Table(tab_main)
table.updateTable(table.currentRow, table.db)

graph_buttons(tab_graph)
films_views(tab_films_views)
films_avg_ratings(tab_films_avg_ratings)
director_avg_ratings(tab_director_avg_ratings)
users_email_subs(tab_users_email_subs)

"""
    Запуск главного UI
"""
footer(root, tabs, tabControl)
root.mainloop()
