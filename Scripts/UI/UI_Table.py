import tkinter as tk
from tkinter import *
import pandas as pd
import time
from Scripts.UI import parser

excel_path = parser.read_config().DIRECTORY_PATH + "\\Data\\DB.xlsx"

COLOR_ITEM_R = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
COLOR_ITEM_G = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
COLOR_ITEM_B = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
FONT_SIZE = 10
COLOR_ITEM_TEXT_R = parser.read_config().TABLE_ITEM_TEXT_COLOR_R
COLOR_ITEM_TEXT_G = parser.read_config().TABLE_ITEM_TEXT_COLOR_G
COLOR_ITEM_TEXT_B = parser.read_config().TABLE_ITEM_TEXT_COLOR_B
TABLE_ROWS_MAX = 20
FONT_STYLE = parser.read_config().FONT_STYLE
"""
    Описание класса Table
    Создание таблицы для вывода основной Базы Данных
"""
class Table:
    # Initialize a constructor
    def __init__(self, gui):
        self.cellsValues = []
        self.indexCellsValues = []
        self.currentRow = 0
        self.gui = gui
        self.total_rows = 0
        self.total_columns = 0
        self.df = pd.read_excel(excel_path, sheet_name='First normal form')
        self.db = self.df.to_dict('list')
        self.df_out = pd.read_excel(excel_path, sheet_name='First normal form')
        self.updateTable(self.currentRow, self.db)
        # An approach for creating the table

    """
        Метод обновления таблицы
        Принимает на вход текущую позицию в таблице и Словарь Базы Данных
    """
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
                        self.entry = Entry(self.gui, width=2, bg='LightSteelBlue',
                                           fg=f'#{COLOR_ITEM_TEXT_R:02x}{COLOR_ITEM_TEXT_G:02x}{COLOR_ITEM_TEXT_B:02x}',
                                           font=(FONT_STYLE, FONT_SIZE),
                                           background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
                        self.entry.insert(END, str(i + 1 + self.currentRow))
                        self.indexCellsValues.append(self.entry)
                        self.entry.grid(row=i + 1, column=j)
                    if i == 0:
                        self.entry = Entry(self.gui, width=18, bg='LightSteelBlue',
                                           fg=f'#{COLOR_ITEM_TEXT_R:02x}{COLOR_ITEM_TEXT_G:02x}{COLOR_ITEM_TEXT_B:02x}',
                                           font=(FONT_STYLE, FONT_SIZE),
                                           background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
                        self.entry.insert(END, list(data.keys())[j])
                        self.entry.grid(row=i, column=j + 1)

                    self.entry = Entry(self.gui, width=18,
                                       fg=f'#{COLOR_ITEM_TEXT_R:02x}{COLOR_ITEM_TEXT_G:02x}{COLOR_ITEM_TEXT_B:02x}',
                                       font=(FONT_STYLE, FONT_SIZE),
                                       background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
                    self.cellsValues.append(self.entry)

                    self.entry.insert(END, str(self.db[list(self.db.keys())[j]][i + start]))
                    self.entry.grid(row=i + 1, column=j + 1)

    """
        Метод сохранения данных таблицы в Excel
        Принимает на вход текущую позицию в таблице
    """
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
            self.df_out = pd.read_excel(excel_path, sheet_name='First normal form')
            self.updateTable(start, self.db)
        else:
            print("Incorrect Data")

    """
        Метод для прокручивания таблицы на один элемент вниз
    """
    def scrollDown(self):
        if self.currentRow < len(self.db['ID пользователя']) - self.total_rows:
            self.currentRow += 1
        self.updateTable(self.currentRow, self.db)

    """
        Метод для прокручивания таблицы на один элемент вверх
    """
    def scrollUp(self):
        if self.currentRow > 0:
            self.currentRow -= 1
        self.updateTable(self.currentRow, self.db)
    """
        Метод для прокручивания таблицы к 1 элементу
    """
    def scrollTop(self):
        self.currentRow = 0
        self.updateTable(self.currentRow, self.db)
    """
        Метод для прокручивания таблицы к введенной позиции элемента
    """
    def scrollTo(self, index):
        if len(self.db['ID пользователя']) > TABLE_ROWS_MAX:
            if index > 0:
                if index < len(self.db['ID пользователя']) - self.total_rows:
                    self.currentRow = index - 1
                else:
                    self.currentRow = len(self.db['ID пользователя']) - TABLE_ROWS_MAX
            self.updateTable(self.currentRow, self.db)
    """
        Метод для прокручивания таблицы к самому нижнему элементу
    """
    def scrollBottom(self):
        if len(self.db['ID пользователя']) > TABLE_ROWS_MAX:
            self.currentRow = len(self.db['ID пользователя']) - TABLE_ROWS_MAX
            self.updateTable(self.currentRow, self.db)
    """
        Метод для удаления строки в таблице и Excel
        Принимает на вход индекс строки
    """
    def deleteRow(self, index):
        if len(self.db['ID пользователя']) < TABLE_ROWS_MAX:
            self.total_rows = len(self.db['ID пользователя'])
        else:
            self.total_rows = TABLE_ROWS_MAX

        if len(self.db['ID пользователя']) > 0:
            for j in range(self.total_columns):
                self.db[list(self.db.keys())[j]].pop(index - 1)

        # print(len(self.db['ID пользователя']))
        # print(self.total_rows)
        self.scrollUp()
        self.updateTable(self.currentRow, self.db)
    """
        Метод для экспорта данных в Excel
        Принимает на вход Словарь базы данных
    """
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
        df_export.to_excel(excel_path, index=False, sheet_name='First normal form')
    """
        Вспомогательный Метод для конвертации Dictionary в DataFrame
        Принимает на вход Словарь базы данных
        Возвращает DataFrame
    """
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
    """
        Метод для добавления строки в таблицу
        Принимает на вход словарь добавляемой строки
    """
    def new_line(self, entry_list):
        db_keys = list(self.db.keys())
        # label = tk.Label(root, text='Damn', font=('Impact', 18))
        if self.validateEntryRow(entry_list):
            for j in range(self.total_columns):
                self.db[list(self.db.keys())[j]].append(str(entry_list[j].get()))
                entry_list[j].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
                entry_list[j].delete(0, END)
                entry_list[j].put_placeholder()
            self.total_rows += 1
            self.updateTable(self.currentRow, self.db)
    """
        Метод для проверки вводимых данных
        Принимает на вход словарь проверяемой строки
    """
    # Блок валидации
    def validateEntryRow(self, entry_list):
        isValid = True
        db_keys = list(self.db.keys())
        line_data = dict.fromkeys(db_keys)
        if tk.Entry.get(entry_list[0]).isdigit() and tk.Entry.get(entry_list[0]) != db_keys[0]:
            line_data[db_keys[0]] = tk.Entry.get(entry_list[0])
            entry_list[0].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[0].configure(background="red")

        if not tk.Entry.get(entry_list[1]).isdigit() and tk.Entry.get(entry_list[1]) != db_keys[1]:
            line_data[db_keys[1]] = tk.Entry.get(entry_list[1])
            entry_list[1].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[1].configure(background="red")

        if not tk.Entry.get(entry_list[2]).isdigit() and tk.Entry.get(entry_list[2]) != db_keys[2]:
            line_data[db_keys[2]] = tk.Entry.get(entry_list[2])
            entry_list[2].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[2].configure(background="red")

        if not tk.Entry.get(entry_list[3]).isdigit() and tk.Entry.get(entry_list[3]) != db_keys[3]:
            line_data[db_keys[3]] = tk.Entry.get(entry_list[3])
            entry_list[3].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[3].configure(background="red")

        if tk.Entry.get(entry_list[4]).isdigit() and tk.Entry.get(entry_list[4]) != db_keys[4]:
            line_data[db_keys[4]] = tk.Entry.get(entry_list[4])
            entry_list[4].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[4].configure(background="red")

        if not tk.Entry.get(entry_list[5]).isdigit() and tk.Entry.get(entry_list[5]) != db_keys[5]:
            line_data[db_keys[5]] = tk.Entry.get(entry_list[5])
            entry_list[5].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[5].configure(background="red")

        if tk.Entry.get(entry_list[6]).isdigit() and tk.Entry.get(entry_list[6]) != db_keys[6]:
            line_data[db_keys[6]] = tk.Entry.get(entry_list[6])
            entry_list[6].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[6].configure(background="red")

        if not tk.Entry.get(entry_list[7]).isdigit() and tk.Entry.get(entry_list[7]) != db_keys[7]:
            line_data[db_keys[7]] = tk.Entry.get(entry_list[7])
            entry_list[7].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
        else:
            isValid = False
            entry_list[7].configure(background="red")

        if not tk.Entry.get(entry_list[8]).isdigit() and tk.Entry.get(entry_list[8]) != db_keys[8]:
            entry_list[8].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
            line_data[db_keys[8]] = tk.Entry.get(entry_list[8])
        else:
            isValid = False
            entry_list[8].configure(background="red")

        if tk.Entry.get(entry_list[9]).isdigit() and tk.Entry.get(entry_list[9]) != db_keys[9]:
            entry_list[9].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
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
            entry_list[10].configure(background=f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}')
            line_data[db_keys[10]] = tk.Entry.get(entry_list[10])
        return isValid