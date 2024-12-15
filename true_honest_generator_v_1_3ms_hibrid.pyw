"""This module contains only one class with the most honest random winner generator
v. 1.1
Changelog:
- Add autoscroll
"""
import tkinter as tk
from tkinter import filedialog, scrolledtext
from time import sleep
from tkinter import ttk
from tkinter import *
from tkinter import Checkbutton
import random

from numpy.ma.core import count


class TrueHonestGenerator:
    """The most honest random winner generator!"""
    data = []
    check_state_checkbox = 0
    WINNERS_PER_CLICK = 1
    DELAY_TO_CHOOSE = 3
    phrases = ['Считываем случайные биты с микрофона',
               'Замешываем случайность',
               'Рандомизируем выбор',
               'Ищем источник случайности в космосе',
               'Спрашиваем случайно число у дворника дяди Васи',
               'Заглядываем в хрустальный шар',
               'Подсовываем своего кандидата',
               'Подбрасываем монету',
               'Тянем случайную карту',
               'Открываем книгу на случайной странице',
               'Просто выбираем участника с красивой фамилией',
               ]

    def __init__(self):
        """Creating Window"""
        self.window = tk.Tk()
        self.window.title("Самый честный генератор"
                          "(ещё честнее, чем тот, который нашли в интернете)")
        # Text field
        self.output_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD,
                                                     font=("Arial Bold", 15))  # Увеличивает шрифт и делает жирненьким
        self.output_text.pack(expand=True, fill='both')
        self.output_text.bind("<Control-c>", self.copy_text_to_clipboard)
        self.output_text.bind("<Control-C>", self.copy_text_to_clipboard)
        # "Open" button
        self.open_button = tk.Button(self.window, text="Открыть файл", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)
        # "Choose winner" button
        self.choose_button = tk.Button(self.window,
                                       text="Выбрать победителя",
                                       command=self.choose_random_element,
                                       state=tk.DISABLED)
        self.choose_button.pack(side=tk.LEFT, padx=10, pady=10)
        #Numbers of winners
        self.check_state_checkbox = IntVar()
        self.check_button = tk.Checkbutton(text="Делает быстро", variable=self.check_state_checkbox)
        self.check_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.enter_button = tk.Button(self.window, text="принять", command=self.set_winners_per_click)
        self.enter_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.entry_winner = tk.Entry(self.window)
        self.entry_winner.pack(side = tk.RIGHT, padx=5, pady=5)

        self.window.mainloop()

    def copy_text_to_clipboard(self):
        """Abiblity to copy text from ScrolledText"""
        try:
            selected_text = self.output_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return
        self.window.clipboard_clear()
        self.window.clipboard_append(selected_text)
        self.window.update()

    def open_file(self):
        """Open file and load participants"""
        file_path = filedialog.askopenfilename(title="Выберите файл",
                                               filetypes=(("Text file", "*.txt"),
                                                          ("All files", "*.*"),
                                                          ("Text file", "*.csv")))
        if file_path:
            self.output_text.delete(1.0, tk.END)  # Clear input field
            # self.print_to_form(f"Загрузили участников из файла: {file_path}")

            self.data.clear()
            with open(file_path, mode='r', encoding="utf-8") as file:
                self.data = file.readlines()

            if self.data:
                self.print_to_form(f"Количесвто участников = {len(self.data)}")
                self.print_to_form(f"Количество будущих победителей: {self.WINNERS_PER_CLICK}\n")
                self.choose_button.config(state=tk.NORMAL)  # Activate "Choose winner" button
            else:
                self.print_to_form("Участников нет.")

    def choose_random_element(self):
        """Choose random winner"""

        self.choose_button.config(state=tk.DISABLED)  # Deactivate "Choose winner" button

        sys_random = random.SystemRandom()

        if len(self.data) == 0:
            self.print_to_form("\nСписок участников пуст")
            return

        if self.check_state_checkbox.get() == 0:
            for i in range(self.WINNERS_PER_CLICK):

                if len(self.data) == 0:
                    self.print_to_form("\nУчастники кончились, а призы - нет!")
                    return

                probability_to_win = round((self.WINNERS_PER_CLICK - i) / (len(self.data)) * 100, 2)
                if probability_to_win > 100:
                    probability_to_win = 100
                self.print_to_form(f"\nОсталось призов: {self.WINNERS_PER_CLICK - i}. "
                                   f"Ваш шанс сорвать джекпот: {probability_to_win}%")

                self.print_to_form(f"{sys_random.choice(self.phrases)}", no_new_line=True)

                for _ in range(self.DELAY_TO_CHOOSE):
                    self.output_text.insert(tk.END, ".")
                    self.window.update()
                    sleep(1)

                # randint in SystemRandom include both boundaries
                winner_id = sys_random.randint(0, len(self.data) - 1)

                self.print_to_form(f"\nНаш победитель: {self.data.pop(winner_id).strip()}")

                if i != self.WINNERS_PER_CLICK - 1:
                    sleep(0.5)
        else:
            self.DELAY_TO_CHOOSE = 0.2
            self.print_to_form("Наши победители:\n")

            for i in range(self.WINNERS_PER_CLICK):

                if len(self.data) == 0:
                    self.print_to_form("\nУчастники кончились, а призы - нет!")
                    return

                # randint in SystemRandom include both boundaries
                probability_to_win = round(
                    (self.WINNERS_PER_CLICK - i) / (len(self.data)) * 100, 2)
                winner_id = sys_random.randint(0, len(self.data) - 1)

                self.print_to_form(f"{i + 1}. {self.data.pop(winner_id).strip()} / {probability_to_win}%")

                sleep(self.DELAY_TO_CHOOSE)

        self.print_to_form("\nВсе призы разыграны!")
        self.choose_button.config(state=tk.NORMAL)  # Activate "Choose winner" button

    def print_to_form(self, text, no_new_line=False):
        """Pretty print to form"""
        self.output_text.insert(tk.END, text + ("" if no_new_line else "\n"))
        self.output_text.see(tk.END)
        self.window.update()

    # set winner per click button
    def set_winners_per_click(self):
        try:
            self.WINNERS_PER_CLICK = int(self.entry_winner.get())
            self.print_to_form(f"Количество будущих победителей: {self.WINNERS_PER_CLICK}\n")
        except ValueError:
            self.print_to_form("Пожалуйста, введите корректное число.")

if __name__ == "__main__":
    gen = TrueHonestGenerator()
