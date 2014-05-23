#!/usr/bin/python3

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.title=tk.Label(self)
        self.title["text"] = "Centry"
        self.title["font"] = ('',26,'bold')
        self.title.pack(side='top')
        self.hi_there = tk.Button(self)
#        self.hi_there["text"] = "Hello World\n(click me)"
#        self.hi_there["command"] = self.say_hi
#        self.hi_there.pack(side="right")

        self.QUIT = tk.Button(self, text="PANIC",font=('',32,''), bg="red", fg="black",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.master.title("Centry Panic Systems")
app.master.geometry("400x300")
app.mainloop()
