from tkinter import *


def client_gui():
    window = Tk()
    window.title("Client")
    window.geometry('350x200')
    btn = Button(window, text="Click Me", command=clicked)
    window.mainloop()


def clicked():
    pass