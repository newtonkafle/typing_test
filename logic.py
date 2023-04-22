import json
import time
import math


class Logic:
    def __init__(self) -> None:
        self.index = 0
        self.word_list = []

        # triggers for check logic
        self.halt_until_correct = True
        self.inacc_word_limit = 0

        # counting the correct and incorrect words
        self.correct_word_count = 0
        self.incorrect_word_count = 0

        # Lesson Variables
        self.lesson = None
        self.lesson_number = 1

        # Variable for timer function
        self.timer_start = True
        self.start_time = None

        # counting the words
        self.word_count = 1

        # # cpm wpm and acc
        self.cpm_v = 0
        self.wpm_v = 0
        self.accuracy = 0

    def check_key(self, key):
        if self.index >= len(self.word_list):
            self.next_lesson.config(state="normal")
            self.master.unbind("<Key>")
            return

        char = self.word_list[self.index].cget("text")
        if char == " _ ":
            char = " "

        if char == key:
            # increasing the word count
            self.word_count = self.word_count + 1 if char == " " else self.word_count

            # coloring the key green when it matches
            self.word_list[self.index].config(bg="green")

            # changing the triggers to halt the checking process to false if true it will halt the code until the
            # key matches with user key
            self.halt_until_correct = False

            # this clears the count to start again if any inaccuracy
            self.inacc_word_limit = 0

            # increasing the counts for the correct char
            self.correct_word_count += 1

            # calc cpm and wpm
            self.calc_cpm_and_wpm()

        # it will stop the checking process if the trigger was true
        elif self.halt_until_correct:
            return
        else:
            # coloring the key red when it doesn't matches
            # self.incorrect_word_count += 1
            self.inacc_word_limit += 1
            self.word_list[self.index].config(bg="red")

            # stops checking inaccuracy when limit is 3
            if self.inacc_word_limit == 3:
                self.halt_until_correct = True

        # calculating the accuracy
        self.calc_accuracy()

        # increasing the index to check next key
        self.index += 1

    def load_lessons(self):
        with open("data.json") as file:
            self.data = json.load(file)
        # self.data = {value for item in self.data for value in item.values()}
        self.data = {key: val for k in self.data for key, val in k.items()}
        self.lesson = self.data[f"lesson_{self.lesson_number}"]

    def calc_cpm_and_wpm(self):
        end_time = time.time()
        time_elpased = end_time - self.start_time
        a_minute = time_elpased / 60
        self.cpm_v = math.floor(self.correct_word_count / a_minute)
        self.wpm_v = math.floor(self.word_count / a_minute)

    def timer(self):
        if self.timer_start:
            self.start_time = time.time()
            self.timer_start = False

    def calc_accuracy(self):
        inacc_word = 1 + self.index - self.correct_word_count
        inaccuracy = math.ceil((inacc_word / (self.index + 1)) * 100)
        self.accuracy = 100 - inaccuracy
