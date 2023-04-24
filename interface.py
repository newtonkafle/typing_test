import tkinter as tk
from tkinter import StringVar, font
from logic import Logic
from user_avatar_api import Logo
import random
from useraccount import Account



class AppInterface(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Typing Test")
        self.geometry("1050x450")
        self.frame = AppAccountPage(self)
        # self.frame = AppPage(self)
        self.bind("<Key>", self.frame.key_pressed)


class AppAccountPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.geometry("700x300")
        self.master = master
        self.pack()
        # initilzing the logo class
        self.logo_api = Logo()
        
        # initializing the account class
        self.db = Account()
        
        
        self.heading_text = "PROTYPER"
        self.color_list = ['white', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'pink', 'gray', 'lightgray', 'darkgray', 'brown', 'navy', 'turquoise', 'violet', 'gold', 'silver']
        #binding the key pressed
        self.bind("<Key>", self.key_pressed)
        
        # name of the person
        self.name = []
        
        #last item last text
        self.name_container = []
        self.name_text = []
        
    
        #initializing the co-ordinate\
        self.co_ord = {"x1":200,
                       "x2": 230,
                       "y1": 150,
                       "y2": 180,
                       "r": 5}
        
        # pencil location
        self.pencil_location = None
        
        # creating the canvas for background image 
        self.background_canvas = tk.Canvas(self, width=700, height=300)
        self.background_canvas.create_image(350, 150, image = self.logo_api.background)
        self.background_canvas.pack(fill=tk.BOTH, expand=True)
        
        # creating the outer frame
        self.outer_frame = tk.Frame(self.background_canvas, highlightthickness=0)
        
        # creating the window to add frame on top of that canvas
        self.background_canvas.create_window(350, 150, window=self.outer_frame)
        
        # frame for the logo and the name
        self.logo_frame = tk.Frame(self.outer_frame, highlightthickness=0, highlightbackground="#000000")
        self.logo_frame.grid(row=0, column=0)
        
        # label for asking the user name
        self.app_name = self.background_canvas.create_text(350, 120, text="Enter Your Name.", font=('Press Start 2P', 20, 'bold'))
        # self.app_name.grid(padx=(40, 0), row=1, column=0)

        #typing logo
        self.pencil_logo = self.background_canvas.create_image(230, 150, image=self.logo_api.pencil_image)

# --------------------------# ----------------------------------------
        # # # # line
        # self.background_canvas.create_line(20, 10, 20, 400, width=3)
# -------------------#-----------------------#-------------------------
        # user avatar
        self.background_canvas.create_image(100, 150, image=self.logo_api.avatar)
        
        self.buid_text_container()
        
        # go button 
        self.button_image = self.background_canvas.create_image(350, 240, image=self.logo_api.button_image)
        self.background_canvas.itemconfig(self.button_image, tags='button')
        
        # binding the button go button image to button click
        self.background_canvas.tag_bind('button', '<Button-1>', self.on_go_button_click)

        # go label
        self.background_canvas.create_text(350, 280, text="Let's Go", font=(('Press Start 2P', 15, 'bold')))
        

    def buid_text_container(self):
        x1, y1 = 200, 10
        x2, y2 = 250, 60
        r = 20  # radius of corners
        
        for char in self.heading_text:
            # creating the random color to fill
            color = random.choice(self.color_list)
            # creating the container using the cor-ordinate
            self.containter_builder(x1, y1, x2, y2, r, color=color)
            
            # creating the center co-ordinate for the char
            x_center = (x1 + x2)/2
            y_center = (y1 + y2)/2    
            self.background_canvas.create_text(x_center, y_center, text=char, font=('Press Start 2P', 25, 'bold'), fill="black")
            
            # displacing the item by 40 units on x-axis
            x1 += 40
            x2 += 40
        
    def containter_builder(self, x1, y1, x2, y2, r, color=None):
        # calculate coordinates of polygon vertices
        points = [
            x1+r, y1,  # top left
            x2-r, y1,  # top right
            x2, y1+r,  # top right corner
            x2, y2-r,  # bottom right corner
            x2-r, y2,  # bottom right
            x1+r, y2,  # bottom left
            x1, y2-r,  # bottom left corner
            x1, y1+r,  # top left corner
        ]
        item = self.background_canvas.create_polygon(points, outline=color, fill=color, width=2) 
        return item
    
    def key_pressed(self, event): 
        color = random.choice(self.color_list)
        if event.char.isalnum():
            if len(self.name) >= 10:
                return
            self.pencil_location = self.co_ord['x2'] + 20
            # append the char in name:
            self.name.append(event.char)
            
            # build the container
            self.name_container.append(self.containter_builder(self.co_ord['x1'], self.co_ord['y1'], self.co_ord['x2'], self.co_ord['y2'], self.co_ord['r'], color=color))

            # creating the center co-ordinate for the char
            x_center = (self.co_ord['x1'] + self.co_ord['x2'])/2
            y_center = (self.co_ord['y1'] + self.co_ord['y2'])/2  
            
            #create text inside the container
            self.name_text.append(self.background_canvas.create_text(x_center, y_center, text=event.char.upper(), font=('Press Start 2P', 20,), fill="black"))

            # increase the co-ordinate
            self.co_ord['x1'] += 30
            self.co_ord['x2'] += 30
        
        # managing the delete
        if event.keysym == 'BackSpace':
            if len(self.name_container) >= 0 and (len(self.name_text)) >=0:
                self.background_canvas.delete(self.name_container.pop())
                self.background_canvas.delete(self.name_text.pop())
                self.pencil_location -= 30
                
                #decrease the co-ordinats value as well
                self.co_ord['x1'] -= 30
                self.co_ord['x2'] -= 30
                
                # pop out from name
                self.name.pop()
        
        #placing the pencil at the required phase
        self.background_canvas.coords(self.pencil_logo, (self.pencil_location, 150))

    def on_go_button_click(self, event):
        self.name = "".join(self.name)
        if self.name != "":
            self.db.add_account(self.name, self.logo_api.avatar_bytes.tobytes())
            print(self.logo_api.avatar_bytes)
            self.destroy()
            self.frame2 = AppPage(self.master)
        else:
            print("name is left empty")
        # get all the required item to insert
        # insert the item in the database
        # exits this frame and open next frame
        # provide the error pop up for the empty name
            
    

class AppPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry("1050x450")
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
