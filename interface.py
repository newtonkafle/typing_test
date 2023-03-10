
import tkinter as tk
from PIL import ImageTk, Image
import time
import math
import json


class AppInterface(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Typing Test")
        self.geometry('1200x500')
        self.frame = AppPage(self)
        self.bind("<Key>", self.frame.key_pressed)

    # def key_pressed(self, event):
    #     print(event.char)


class AppPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.data = None

        # more ui
        self.user_label = tk.Label(
            self, text='User : Newton', textvariable='', font=('Arial, 15'))
        self.user_label.grid(row=0, column=0, columnspan=2,
                             sticky='W', padx=0, pady=0)
        self.lesson_label = tk.Label(
            self, text='Lesson 1', textvariable='', font=("Arial", 40))
        self.lesson_label.grid(column=0, row=1, pady=10, columnspan=2)

        # setuping the box for the characters
        self.char_var = None
        self.canvas_frame = tk.Frame(self,
                                     highlightbackground='black', highlightthickness=2)
        self.canvas_frame.grid(column=0, row=2, padx=50,
                               ipadx=20, columnspan=2)

        # char_canvas
        self.char_canvas = tk.Canvas(
            self.canvas_frame, width=1000, height=265)
        self.char_canvas.grid(row=1, column=1, sticky='news', padx=15)
        self.char_canvas.config(scrollregion=self.char_canvas.bbox("all"))

        # add an scroll bar
        self.scroll_bar = tk.Scrollbar(
            self.canvas_frame, orient="vertical", command=self.char_canvas.yview)
        self.scroll_bar.grid(column=2, row=1, sticky='ns')
        self.char_canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config()

        # automatic scroll units
        self.scroll_units = 0

        # create a frame for all the labels
        self.char_frame = tk.Frame(self.char_canvas,)
        self.char_canvas.create_window(
            (0, 0), window=self.char_frame, anchor='nw')

        self.accuracy = tk.Label(
            self, text=f'Accuracy: {0}', textvariable='', font=("Arial, 20"))
        self.accuracy.grid(column=0, row=3)
        self.speed = tk.Label(
            self, text=f'Speed: {0}', textvariable='', font=("Arial, 20"))
        self.speed.grid(column=1, row=3)

        # buttons for next lessons
        self.next_lesson = tk.Button(self,
                                     text='Next Lesson', command=self.set_next_lesson, font=("Arial", 20), state='disabled')
        self.next_lesson.grid(column=0, columnspan=2, row=4)
     # generating the characters
        self.bind("<Key>", self.key_pressed)

        self.index = 0

        # inaccurace word count
        self.inacc_word_count = 0
        self.correct_word_count = 0
        self.halt_until_correct = False
        self.inacc_word_limit = 0

        # for timer
        self.start_time = None
        self.timer_start = True

        # set initial lesson
        self.lesson_no = 1
        self.lesson = None

        # load the lesson
        self.load_lessons()

        # generate the characters
        self.gen_char()

    def gen_char(self):
        """ create the series of the labels to show the sentences into the user interface """
        row = 0
        col = 0
        self.box_list = []
        for num, char in enumerate(self.lesson):
            # creating the variable from string
            my_box = f'self.char_boxes_{num}'
            myVars = vars()
            # creating the label using the variable generated
            myVars[my_box] = tk.Label(
                self.char_frame, text=char, font=('Arial', 30), highlightthickness=0, borderwidth=0, padx=0,
                width=1)
            if col % 50 == 0:
                row = row + 1
                col = 0
            myVars[my_box].grid(column=col, pady=10,
                                padx=1, row=row, ipadx=1, sticky='EW')
            col = col + 1

            # appending the label into the list
            self.box_list.append(myVars[my_box])

    def key_pressed(self, event):
        """ activates when user pressed any keys """
        # checking the key
        self.timer()
        print(event.char)
        if event.char != "":
            self.check_key(event.char)
            self.calc_cps()

    def check_key(self, key):

        if self.index < len(self.box_list):
            box_key = self.box_list[self.index].cget('text')
            if box_key == key:
                self.halt_until_correct = False
                self.inacc_word_limit = 0

                self.correct_word_count += 1
                # coloring the key green when it matches
                self.box_list[self.index].config(bg='green')

            elif self.halt_until_correct:
                return
            else:
                # coloring the key red when it doesn't matches
                self.inacc_word_count += 1
                self.inacc_word_limit += 1
                self.box_list[self.index].config(bg='red')

                if self.inacc_word_limit != 0 and self.inacc_word_limit % 3 == 0:
                    self.halt_until_correct = True

                # calculating the accuracy
                self.calc_accuracy()
            # increasing the index to check next key
            self.index += 1
        else:
            self.next_lesson.config(state='normal')
            self.master.unbind("<Key>")
        total_word_count = self.correct_word_count + self.inacc_word_count
        if total_word_count != 0 and total_word_count % 50 == 0:
            self.scroll_units = 2
            self.char_canvas.yview_scroll(self.scroll_units, what=['units'])

    def calc_stats(self,):
        # this will check the accuracy and the typing the speed of the user
        pass

    def calc_accuracy(self):
        inaccuracy = self.inacc_word_count/len(self.box_list) * 100
        acc = 100 - inaccuracy
        self.accuracy.config(text=f'{math.floor(acc)} %')

    def timer(self):
        if self.timer_start:
            self.start_time = time.time()
            self.timer_start = False

    def calc_cps(self):
        end_time = time.time()
        time_elpased = end_time - self.start_time
        char_per_second = self.correct_word_count/(time_elpased/60)
        self.speed.config(text=f'{math.floor(char_per_second)} CPM')

    def set_next_lesson(self):
        self.reset_ui()
        self.lesson = self.data[f'lesson_{self.lesson_no + 1}']
        self.gen_char()

    def load_lessons(self):
        with open("data.json") as file:
            self.data = json.load(file)
        # self.data = {value for item in self.data for value in item.values()}
        self.data = {key: val for k in self.data for key, val in k.items()}
        self.lesson = self.data[f'lesson_{self.lesson_no}']

    def reset_ui(self):
        # activating the events
        self.master.bind("<Key>", self.key_pressed)

        # resetting the timer
        self.timer_start = True

        # resetting the index
        self.index = 0

        # resetting the word counds
        self.correct_word_count = 0
        self.inacc_word_count = 0

        # restting the widgets in the char frame
        for widget in self.char_frame.winfo_children():
            widget.destroy()

        # diable the next button
        self.next_lesson.config(state='disabled')

        # set the scroll bar to the top again
        self.char_canvas.yview_moveto(0.0)
