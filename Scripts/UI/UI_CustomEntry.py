import tkinter as tk
from Scripts.UI import parser
COLOR_ITEM_R = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
COLOR_ITEM_G = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R
COLOR_ITEM_B = parser.read_config().TABLE_BACKGROUND_ITEM_COLOR_R

COLOR_ITEM_TEXT_R = parser.read_config().TABLE_ITEM_TEXT_COLOR_R
COLOR_ITEM_TEXT_G = parser.read_config().TABLE_ITEM_TEXT_COLOR_G
COLOR_ITEM_TEXT_B = parser.read_config().TABLE_ITEM_TEXT_COLOR_B
FONT_SIZE = 10
FONT_STYLE = parser.read_config().FONT_STYLE
"""
    Расширение класса Entry
    Добавлены подсказки для пользовательского ввода
"""
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER",
                 color=f'#{COLOR_ITEM_TEXT_R:02x}{COLOR_ITEM_TEXT_G:02x}{COLOR_ITEM_TEXT_B:02x}', ):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self['bg'] = f'#{COLOR_ITEM_R:02x}{COLOR_ITEM_G:02x}{COLOR_ITEM_B:02x}'
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