"""Main loop for Tamagotchi gui"""

from tkinter import Tk
from gui import TamaTk
import os


if __name__ == '__main__':
    root = Tk()
    gui = TamaTk(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()
