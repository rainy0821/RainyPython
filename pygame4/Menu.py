from tkinter import Tk, Button
from threading import Thread
from pygame4 import Game1


def start():
    game = Game1
    game.main()


def middle():
    Thread(target=start).start()


def menu():
    win = Tk()
    win.title('選項')

    button = Button(win, text='start', command=start)
    button.pack()

    win.mainloop()


menu()
