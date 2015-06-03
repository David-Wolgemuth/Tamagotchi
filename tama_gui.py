from tkinter import *
from tama import Tamagotchi
import pickle
import os

class TamaWindow:
    def __init__(self, master):
        self.master = master
        self.active_labels = []
        self.pet = None

        if os.path.exists('saves.pkl'):
            self.pet_saves = pickle.load(open('saves.pkl', 'rb'))
            self.welcome_screen()
        else:
            self.pet_saves = []
            pickle.dump(self.pet_saves, open('saves.pkl', 'wb'))
            self.new_pet_window()

    def welcome_screen(self):
        new = Button(self.master, text='Make New Pet', command=self.new_pet_window)
        old = Listbox(self.master)
        load = Button(self.master, text='Load Pet', command=lambda:
                        self.select_pet(old.curselection()))

        for label in self.active_labels:
            label.destroy()

        new.grid(row=0, column=0)
        load.grid(row=0, column=1)
        old.grid(row=1, column=0, columnspan=2)
        self.active_labels = [new, old, load]

        for name in pickle.load(open('saves.pkl', 'rb')):
            old.insert(END, name)

    def select_pet(self, name, kind=None):
        self.pet = Tamagotchi()
        self.pet.name = name
        self.pet.folder = name + '_saves'
        if not self.pet.animal:
            self.pet.animal = kind

        if os.path.exists(self.pet.folder):
            self.pet.kind = pickle.load(open(self.pet.folder + '/animal_type.pkl', 'rb'))
            self.pet.happiness = pickle.load(open(self.pet.folder + '/happiness.pkl', 'rb'))
            self.pet.health = pickle.load(open(self.pet.folder + '/health.pkl', 'rb'))
        else:
            os.mkdir(self.pet.folder)
            pickle.dump(kind, open(self.pet.folder + '/animal_type.pkl', 'wb'))
            pickle.dump(50, open(self.pet.folder + '/happiness.pkl', 'wb'))
            pickle.dump(50, open(self.pet.folder + '/health.pkl', 'wb'))

    def error_page(self, text_in):
        if text_in == 'Name Already Exists':
            for label in self.active_labels:
                label.destroy()
            message = Label(self.master, text=text_in)
            button = Button(self.master, text='Continue',
                            command=self.new_pet_window)
            for x in message, button:
                self.active_labels.append(x)
                x.pack()

    def new_pet_window(self):

        lkind = Label(self.master, text='Choose an Animal')
        lname = Label(self.master, text='Choose a Name')
        listkind = Listbox(self.master)
        onlyA = self.master.register(lambda x: x.isalpha())
        ename = Entry(self.master, validate='key',
                      validatecommand=(onlyA, '%S'))

        submit = Button(self.master, text='Submit', command=lambda:
                        self.make_pet(ename.get(), listkind.curselection()[0]))

        for label in self.active_labels:
            label.destroy()

        self.active_labels = [lname, ename, lkind, listkind, submit]
        for label in self.active_labels:
            label.pack()

        for animal in os.listdir('animals'):
            listkind.insert(END, animal[:-4])

    def make_pet(self, name, kind):
        if name in pickle.load(open('saves.pkl', 'rb')):
            self.error_page('Name Already Exists')
        else:
            out_kind = os.listdir('animals')[kind]
            self.pet_saves = pickle.load(open('saves.pkl', 'rb'))
            self.pet_saves.append(name)
            pickle.dump(self.pet_saves, open('saves.pkl', 'wb'))
            self.select_pet(name, out_kind)

if __name__ == '__main__':
    root = Tk()
    gui = TamaWindow(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to
                set frontmost of process "Python" to true' ''')
    root.mainloop()