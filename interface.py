
import tkinter as tk


class AppInterface(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Typing Test")
        self.geometry('900x400')
        self.frame = AppPage(self)
        self.bind("<Key>", self.frame.key_pressed)

    # def key_pressed(self, event):
    #     print(event.char)


class AppPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.data = "crazy fox jump over the lazy dog and get drunked with the bottle of wine Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus"

        # setuping the box for the characters
        self.char_var = None
        self.char_frame = tk.Frame(self)
        self.char_frame.grid(padx=10)
        self.gen_char()
        # self.char_frame.bind("<KeyPress>", self.key_pressed)
     # generating the characters
        self.bind("<Key>", self.key_pressed)

    def gen_char(self):
        # self.data = self.data.split(' ')
        row = 0
        col = 0
        self.box_list = []
        # myVars = ''
        for num, char in enumerate(self.data):

            # creating the variable from string
            my_box = f'self.char_boxes_{num}'
            myVars = vars()
            if char == "":
                char = "......."
            myVars[my_box] = tk.Label(
                self.char_frame, text=char, font=('Arial', 20), highlightthickness=0, borderwidth=0, padx=0,
                width=1)
            if col % 50 == 0:
                row = row + 1
                col = 0
            myVars[my_box].grid(column=col, pady=10,
                                padx=0, row=row, ipadx=0, sticky='EW')
            col = col + 1
            self.box_list.append(myVars[my_box])
        print(self.box_list[0].cget('text'))

    def key_pressed(self, event):
        print(event.char)

        # when user press the key , it should check the key with the corresponding key in list
        # it should be sequential

        # check_char(event.char)
