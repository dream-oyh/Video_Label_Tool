import tkinter as tk
from Components.MyFrame import MyFrame


class APP(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = MyFrame(master=self, width=1080, height=720)
        self.frame.grid(row=1, column=1)


app = APP()
app.title("Video Label Tool")
app.geometry("1080x720")
app.mainloop()
