import tkinter as tk
from tkinter import StringVar
from logic import Logic
from user_avatar_api import Logo


class AppInterface(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Typing Test")
        self.geometry("1050x450")
        self.frame = AppAccountPage(self)
        # self.frame = AppPage(self)
        # self.bind("<Key>", self.frame.key_pressed)


class AppAccountPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.geometry("700x300")
        self.grid()
        self.logo_api = Logo()

        # label for the name of the app and logo
        self.app_name = tk.Label(self, text="Pro Typer", font=("Arial, 30 bold"))
        self.app_name.grid(padx=(40, 0), row=1, column=0)

        # typing logo
        self.image_canvas = tk.Canvas(self, width=100, height=100)
        self.image_canvas.grid(row=0, column=0, padx=(40, 0), pady=(50, 0))
        self.image_canvas.create_image(53, 50, image=self.logo_api.logo)

        # line
        self.line_canvas = tk.Canvas(self)
        self.line_canvas.grid(row=0, column=1, rowspan=2, pady=(30, 0))
        self.line_canvas.create_line(20, 10, 20, 400, width=3)


class AppPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.logic = Logic()

        # user information frame
        self.user_info_frame = tk.Frame(
            self, highlightthickness=1, highlightbackground="black"
        )
        self.user_info_frame.grid(column=1, row=2)
        # creating the image canvas
        self.image_canvas = tk.Canvas(self.user_info_frame, width=20, height=20)
        self.image_canvas.grid(column=1, row=1)

        # need to implement the image api
        # self.image_canvas.create_image(10, 10, anchor="nw", image="#")

        # User Name or Account Label
        self.user_label = tk.Label(
            self, text="Newton", textvariable="", font=("Arial, 25 bold")
        )
        self.user_label.grid(row=2, column=1)

        # Label for the tracking lesson number
        self.lesson_label = tk.Label(
            self, text="Lesson 1", textvariable="", font=("Arial", 40)
        )
        self.lesson_label.grid(column=0, row=1, pady=10, columnspan=2)

        ## ---------------------------- Character UI -------------------------- ##
        # ----
        # main frame for characters to display
        self.outer_canvas_frame = tk.Frame(
            self, highlightbackground="black", highlightthickness=2
        )
        self.outer_canvas_frame.grid(column=0, row=2, padx=10, rowspan=3)

        # char_canvas_
        self.char_canvas = tk.Canvas(self.outer_canvas_frame, width=810, height=275)
        self.char_canvas.grid(row=0, column=0, sticky="news")

        # create a frame to hold the characters
        self.char_frame = tk.Frame(self.char_canvas)
        self.char_canvas.create_window((0, 0), window=self.char_frame, anchor="nw")

        # add an scroll bar to the right of char_canvas
        self.scroll_bar = tk.Scrollbar(
            self.outer_canvas_frame, orient="vertical", command=self.char_canvas.yview
        )

        # self.char_canvas.configure(scrollregion=self.char_canvas.bbox("all"))

        # update the scrollregion of the canvas to allow scrolling
        self.outer_canvas_frame.bind_all("<MouseWheel>", self._on_mousewheel)

        ### ------------------------------------measurement UI ------------------------###

        # frame to inclue all the right side characters
        self.measure_info_frame = tk.Frame(
            self, highlightbackground="black", highlightthickness=1
        )
        self.measure_info_frame.grid(column=1, row=3, ipadx=20, ipady=30, sticky="NW")

        # label to track the accuracy of typing
        self.accuracy = tk.Label(
            self.measure_info_frame,
            text=f"Accuracy: {0}",
            textvariable="",
            font=("Arial, 20 bold"),
        )
        self.accuracy.grid(column=1, row=0, sticky="NW", pady=5)

        # label to Words Per Minute
        self.wpm = tk.Label(
            self.measure_info_frame,
            text=f"WPM: {self.logic.wpm_v}",
            textvariable="",
            font=("Arial, 20 bold"),
        )
        self.wpm.grid(column=1, row=1, sticky="NW", pady=5, ipady=0)

        # label to track Character Per Minute
        self.cpm = tk.Label(
            self.measure_info_frame,
            text=f"CPM: {self.logic.cpm_v}",
            textvariable="",
            font=("Arial, 20 bold"),
        )
        self.cpm.grid(column=1, row=2, sticky="NW", pady=5, ipady=0)

        # buttons for next lessons
        self.next_lesson = tk.Button(
            self,
            text="Next Lesson",
            command="#",
            font=("Arial", 20),
            state="disabled",
        )
        self.next_lesson.grid(column=0, columnspan=2, row=10)

        self.bind("<Key>", self.key_pressed)

        # -------- Functions to load ui items------ #
        self.logic.load_lessons()
        self.gen_words_interface()

    def gen_words_interface(self):
        """creates characters to display on the canvas"""
        create_frame = True
        row = 0
        width_sum = 0
        anchor_e = True

        for n, char in enumerate(self.logic.lesson):
            # it will create a frame for every row to display words
            if create_frame:
                frame = tk.Frame(self.char_frame)
                frame.grid(column=0, row=row, pady=5)
                create_frame = False
            # creatine the label on that frame
            label = tk.Label(
                frame,
                text=char,
                font=("Arial, 30"),
                width=0,
                justify="right",
                highlightthickness=0,
                borderwidth=0,
            )
            # if the length is greater create a new frame and move it to new row
            if n != 0 and n % 41 == 0:
                create_frame = True
                row = row + 1
                # width_sum = 0
            # packing the label on that frame on specific row
            label.pack(side=tk.LEFT, ipadx=0, padx=0)

            # coloring the space so that it will be detected
            if char == " ":
                label.config(text=" _ ")

            # addding all the labels to the list
            self.logic.word_list.append(label)

    def _on_mousewheel(self, event):
        self.char_canvas.yview_scroll(event.delta, "units")

    def key_pressed(self, event):
        """activates when user pressed any keys"""
        # checking the key
        self.logic.timer()
        if event.char != "":
            self.logic.check_key(event.char)
        self.automatic_scroll()
        # updating cpm and wpm and accuracy
        self.cpm.config(text=f"CPM : {self.logic.cpm_v}")
        self.wpm.config(text=f"WPM : {self.logic.wpm_v}")
        self.accuracy.config(text=f"Accuracy: {self.logic.accuracy} %")

        self.update()

    def automatic_scroll(self):
        scroll_units = 1
        if self.logic.index != 0 and self.logic.index % 43 == 0:
            self.char_canvas.yview_scroll(scroll_units, what=["units"])
            scroll_units = 2

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
        self.next_lesson.config(state="disabled")

        # set the scroll bar to the top again
        self.char_canvas.yview_moveto(0.0)
