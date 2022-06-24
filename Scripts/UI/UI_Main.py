import tkinter as tk
from tkinter import *  # Для вкладок
from tkinter import ttk  # Для вкладок
import pandas as pd
import Scripts.DB as DB
import time
from Scripts import parser

excel_path = parser.read_config("Test-Config.ini")
# CONST FOR PARSER
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 600

FONT_STYLE = 'Arial'
FONT_SIZE = 10

NUM_OF_COLUMNS = 7

# NOT FOR PARSER
WIDTH_OF_COLUMNS = int(WINDOW_WIDTH / ((FONT_SIZE / 1.3) * NUM_OF_COLUMNS + 1) + 1)  # zalupa
TABLE_ROWS_MAX = 20

root = tk.Tk()
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()
x = (ws / 2) - (WINDOW_WIDTH / 2)
y = (hs / 2) - (WINDOW_HEIGHT / 2)
# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
root.title("Выгуляйка")

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


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='black'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class Table:
    # Initialize a constructor
    def __init__(self, gui):
        self.cellsValues = []
        self.indexCellsValues = []
        self.currentRow = 0
        self.gui = gui
        self.total_rows = 0
        self.total_columns = 0
        self.df = pd.read_excel('C:\\Work\\Data\\DB.xlsx', sheet_name='First normal form')
        self.db = self.df.to_dict('list')
        self.df_out = pd.read_excel('C:\\Work\\Data\\DB.xlsx', sheet_name='First normal form')
        self.updateTable(self.currentRow, self.db)
        # An approach for creating the table

    def updateTable(self, start, data):

        if len(self.db['ID пользователя']) < TABLE_ROWS_MAX:
            self.total_rows = len(self.db['ID пользователя'])
        else:
            self.total_rows = TABLE_ROWS_MAX

        for i in range(len(self.cellsValues)):
            self.cellsValues[i].destroy()
        for i in range(len(self.indexCellsValues)):
            self.indexCellsValues[i].destroy()

        self.total_columns = len(self.db)
        self.indexCellsValues = []
        self.cellsValues = []
        for i in range(self.total_rows):
            if i + start < len(self.db['ID пользователя']):
                for j in range(self.total_columns):
                    if j == 0:
                        self.entry = Entry(self.gui, width=2, bg='LightSteelBlue', fg='Black',
                                           font=(FONT_STYLE, FONT_SIZE))
                        self.entry.insert(END, str(i + 1 + self.currentRow))
                        self.indexCellsValues.append(self.entry)
                        self.entry.grid(row=i + 1, column=j)
                    if i == 0:
                        self.entry = Entry(self.gui, width=18, bg='LightSteelBlue', fg='Black',
                                           font=(FONT_STYLE, FONT_SIZE))
                        self.entry.insert(END, list(data.keys())[j])
                        self.entry.grid(row=i, column=j + 1)

                    self.entry = Entry(self.gui, width=18, fg='blue',
                                       font=(FONT_STYLE, FONT_SIZE))
                    self.cellsValues.append(self.entry)

                    self.entry.insert(END, str(self.db[list(self.db.keys())[j]][i + start]))
                    self.entry.grid(row=i + 1, column=j + 1)

    def saveTable(self, start):
        isValid = True
        for i in range(self.total_rows - 1):
            validation_list = []
            for j in range(self.total_columns):
                if i == 0:
                    validation_list.append(self.cellsValues[j])
                    self.db[list(self.db.keys())[j]][i + start] = self.cellsValues[j].get()
                else:
                    validation_list.append(self.cellsValues[j + i * 11])
                    self.db[list(self.db.keys())[j]][i + start] = self.cellsValues[j + i * 11].get()
            if not self.validateEntryRow(validation_list):
                isValid = False
        if isValid:
            print("update")
            self.exportData(self.db)
            self.df_out = pd.read_excel('C:\\Work\\Data\\DB.xlsx', sheet_name='First normal form')
            self.updateTable(start, self.db)
            update_table(tabControl)
        else:
            print("Incorrect Data")

    def scrollDown(self):
        if self.currentRow < len(self.db['ID пользователя']) - self.total_rows:
            self.currentRow += 1
        self.updateTable(self.currentRow, self.db)

    def scrollUp(self):
        if self.currentRow > 0:
            self.currentRow -= 1
        self.updateTable(self.currentRow, self.db)

    def scrollTop(self):
        self.currentRow = 0
        self.updateTable(self.currentRow, self.db)

    def scrollTo(self, index):
        if index > 0:
            if index < len(self.db['ID пользователя']) - self.total_rows:
                self.currentRow = index - 1
            else:
                self.currentRow = len(self.db['ID пользователя']) - TABLE_ROWS_MAX
        self.updateTable(self.currentRow, self.db)

    def scrollBottom(self):
        self.currentRow = len(self.db['ID пользователя']) - TABLE_ROWS_MAX
        self.updateTable(self.currentRow, self.db)

    def deleteRow(self, index):
        if len(self.db['ID пользователя']) < TABLE_ROWS_MAX:
            self.total_rows = len(self.db['ID пользователя'])
        else:
            self.total_rows = TABLE_ROWS_MAX

        if len(self.db['ID пользователя'])>0:
            for j in range(self.total_columns):
                self.db[list(self.db.keys())[j]].pop(index - 1)

        # print(len(self.db['ID пользователя']))
        # print(self.total_rows)
        self.scrollUp()
        self.updateTable(self.currentRow, self.db)

    def exportData(self, data):
        columnHeaders = []
        for j in range(11):
            columnHeaders.append(list(data.keys())[j])
        df_export = pd.DataFrame(columns=columnHeaders)
        for i in range(len(data['ID пользователя'])):
            for j in range(self.total_columns):
                if i == 0:
                    df_export.at[i, columnHeaders[j]] = data[list(data.keys())[j]][i]
                else:
                    df_export.at[i, columnHeaders[j]] = data[list(data.keys())[j]][i]
        df_export.to_excel('C:\\Work\\Data\\DB.xlsx', index=False, sheet_name='First normal form')

    def makeDataFrame(self, data):
        columnHeaders = []
        for j in range(11):
            columnHeaders.append(list(data.keys())[j])
        df_export = pd.DataFrame(columns=columnHeaders)
        for i in range(len(data['ID пользователя'])):
            for j in range(self.total_columns):
                if i == 0:
                    df_export.at[i, columnHeaders[j]] = data[list(data.keys())[j]][i]
                else:
                    df_export.at[i, columnHeaders[j]] = data[list(data.keys())[j]][i]
        return df_export

    def new_line(self, entry_list):
        db_keys = list(self.db.keys())
        # label = tk.Label(root, text='Damn', font=('Impact', 18))
        if self.validateEntryRow(entry_list):
            for j in range(self.total_columns):
                self.db[list(self.db.keys())[j]].append(str(entry_list[j].get()))
                entry_list[j].configure(background="white")
                entry_list[j].delete(0, END)
                entry_list[j].put_placeholder()
            self.total_rows += 1
            self.updateTable(self.currentRow, self.db)

    # Блок валидации
    def validateEntryRow(self, entry_list):
        isValid = True
        db_keys = list(self.db.keys())
        line_data = dict.fromkeys(db_keys)
        if tk.Entry.get(entry_list[0]).isdigit() and tk.Entry.get(entry_list[0]) != db_keys[0]:
            line_data[db_keys[0]] = tk.Entry.get(entry_list[0])
            entry_list[0].configure(background="white")
        else:
            isValid = False
            entry_list[0].configure(background="red")

        if not tk.Entry.get(entry_list[1]).isdigit() and tk.Entry.get(entry_list[1]) != db_keys[1]:
            line_data[db_keys[1]] = tk.Entry.get(entry_list[1])
            entry_list[1].configure(background="white")
        else:
            isValid = False
            entry_list[1].configure(background="red")

        if not tk.Entry.get(entry_list[2]).isdigit() and tk.Entry.get(entry_list[2]) != db_keys[2]:
            line_data[db_keys[2]] = tk.Entry.get(entry_list[2])
            entry_list[2].configure(background="white")
        else:
            isValid = False
            entry_list[2].configure(background="red")

        if not tk.Entry.get(entry_list[3]).isdigit() and tk.Entry.get(entry_list[3]) != db_keys[3]:
            line_data[db_keys[3]] = tk.Entry.get(entry_list[3])
            entry_list[3].configure(background="white")
        else:
            isValid = False
            entry_list[3].configure(background="red")

        if tk.Entry.get(entry_list[4]).isdigit() and tk.Entry.get(entry_list[4]) != db_keys[4]:
            line_data[db_keys[4]] = tk.Entry.get(entry_list[4])
            entry_list[4].configure(background="white")
        else:
            isValid = False
            entry_list[4].configure(background="red")

        if not tk.Entry.get(entry_list[5]).isdigit() and tk.Entry.get(entry_list[5]) != db_keys[5]:
            line_data[db_keys[5]] = tk.Entry.get(entry_list[5])
            entry_list[5].configure(background="white")
        else:
            isValid = False
            entry_list[5].configure(background="red")

        if tk.Entry.get(entry_list[6]).isdigit() and tk.Entry.get(entry_list[6]) != db_keys[6]:
            line_data[db_keys[6]] = tk.Entry.get(entry_list[6])
            entry_list[6].configure(background="white")
        else:
            isValid = False
            entry_list[6].configure(background="red")

        if not tk.Entry.get(entry_list[7]).isdigit() and tk.Entry.get(entry_list[7]) != db_keys[7]:
            line_data[db_keys[7]] = tk.Entry.get(entry_list[7])
            entry_list[7].configure(background="white")
        else:
            isValid = False
            entry_list[7].configure(background="red")

        if not tk.Entry.get(entry_list[8]).isdigit() and tk.Entry.get(entry_list[8]) != db_keys[8]:
            entry_list[8].configure(background="white")
            line_data[db_keys[8]] = tk.Entry.get(entry_list[8])
        else:
            isValid = False
            entry_list[8].configure(background="red")

        if tk.Entry.get(entry_list[9]).isdigit() and tk.Entry.get(entry_list[9]) != db_keys[9]:
            entry_list[9].configure(background="white")
            line_data[db_keys[9]] = tk.Entry.get(entry_list[9])
        else:
            isValid = False
            entry_list[9].configure(background="red")

        try:
            time.strptime(tk.Entry.get(entry_list[10]), '%H:%M:%S')
        except ValueError:
            isValid = False
            entry_list[10].configure(background="red")
        else:
            entry_list[10].configure(background="white")
            line_data[db_keys[10]] = tk.Entry.get(entry_list[10])
        return isValid


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


def delete_line(root):
    delete_frame = tk.Frame(root)
    empty_label = tk.Label(delete_frame, text='Введите номер строки для удаления', font=(FONT_STYLE, FONT_SIZE))
    empty_label.grid(row=0, column=0)
    delete_entry = EntryWithPlaceholder(delete_frame, "№")
    delete_entry.grid(row=0, column=1)
    delete_butt = tk.Button(delete_frame, font=(FONT_STYLE, FONT_SIZE), text="Удалить строку",
                            command=lambda: (table.deleteRow(int(delete_entry.get())),
                                             delete_entry.configure(background="white")
                                             , delete_entry.delete(0, END)
                                             , delete_entry.put_placeholder()) if delete_entry.get().isdigit()
                            else delete_entry.configure(background="red")
                            )
    delete_butt.grid(row=0, column=2)
    delete_frame.pack(pady=10)


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
    my_game.column("Название фильма", anchor=CENTER, width=180)
    my_game.column("Количество просмотров", anchor=CENTER, width=180)

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
    my_game.column("Название фильма", anchor=CENTER, width=180)
    my_game.column("Рейтинг", anchor=CENTER, width=180)

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
    my_game.column("Режиссер", anchor=CENTER, width=180)
    my_game.column("Рейтинг", anchor=CENTER, width=180)

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
    my_game.column("Имя пользователя", anchor=CENTER, width=180)
    my_game.column("E-mail пользователя", anchor=CENTER, width=180)
    my_game.column("Наличие Подписки", anchor=CENTER, width=180)

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

tk.Button(tab_main, text="Up", font=(FONT_STYLE, FONT_SIZE), image=ico_up_arrow,
          command=lambda: table.scrollUp()).place(x=WINDOW_WIDTH - 50, y=50)
tk.Button(tab_main, text="Down", font=(FONT_STYLE, FONT_SIZE), image=ico_down_arrow,
          command=lambda: table.scrollDown()).place(x=WINDOW_WIDTH - 50,
                                                    y=160)
tk.Button(tab_main, text="Save", font=(FONT_STYLE, FONT_SIZE), image=ico_save,
          command=lambda: table.saveTable(table.currentRow)).place(
    x=WINDOW_WIDTH - 50, y=100)
tk.Button(tab_main, text="Top", font=(FONT_STYLE, FONT_SIZE), image=ico_top_arrow,
          command=lambda: table.scrollTop()).place(x=WINDOW_WIDTH - 50, y=0)
tk.Button(tab_main, text="Bottom", font=(FONT_STYLE, FONT_SIZE), image=ico_bottom_arrow,
          command=lambda: table.scrollBottom()).place(
    x=WINDOW_WIDTH - 50, y=220)
tk.Button(tab_main, text="Go to", font=(FONT_STYLE, FONT_SIZE), image=ico_search, command=lambda: (
    table.scrollTo(int(search_entry.get())), search_entry.configure(background="white"), search_entry.delete(0, END)
) if search_entry.get().isdigit()
else search_entry.configure(background="red")).place(x=WINDOW_WIDTH - 50, y=380)
search_entry = Entry(tab_main, font=(FONT_STYLE, FONT_SIZE), width=4, bg='LightSteelBlue', fg='Black',
                     )

search_entry.place(x=WINDOW_WIDTH - 50, y=360)

table = Table(tab_main)
table.updateTable(table.currentRow, table.db)

DB.director_avg_ratings(table.df_out).to_excel("avg_rait.xlsx")

graph_buttons(tab_graph)
films_views(tab_films_views)
films_avg_ratings(tab_films_avg_ratings)
director_avg_ratings(tab_director_avg_ratings)
users_email_subs(tab_users_email_subs)

footer(root, tabs, tabControl)
root.mainloop()
