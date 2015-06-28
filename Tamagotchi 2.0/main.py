from tkinter import Tk
from gui import TamaTk
import os

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('+%s+%s' % (x, y))

if __name__ == '__main__':
    root = Tk()
    gui = TamaTk(root)
    center_window(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()