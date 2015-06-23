from constants import *
from threading import Thread
import tkinter as tk
from PIL import Image, ImageTk
from pet import Tamagotchi
import os

class TamaTk:
    def __init__(self, master):
        self.master = master
        self.master.title('Tamagotchi')
        self.active_widgets = []
        self.saves = []
        self.find_saves()
        self.pet = None
        self.bars = []
        self.welcome_screen()

    def find_saves(self):
        if os.path.isdir('saves'):
            for folder in os.listdir('saves'):
                if os.path.isdir('saves/' + folder):
                    self.saves.append(folder)

    def destroy_widgets(self):
        for widget in self.active_widgets:
            widget.destroy()

    def welcome_screen(self):
        '''Player has option between loading a pet or making a new one
        '''
        self.destroy_widgets()

        new = tk.Button(self.master, text='Make New Pet',
                        command=self.new_pet_window)
        old = tk.Listbox(self.master)
        load = tk.Button(self.master, text='Load Pet', command=lambda:
                            self.select_pet(old.get(old.curselection()[0])))

        new.grid(row=0, column=0)
        load.grid(row=0, column=1)
        old.grid(columnspan=2)
        for name in self.saves:
            old.insert(tk.END, name)

        self.active_widgets = [new, load, old]

    def new_pet_window(self):
        '''Player creates a new pet, window has an Entry box and List
        of Animal types
        '''
        self.destroy_widgets()

        lload = tk.Button(self.master, text='Load Existing',
                                    command = self.welcome_screen)
        lanimal = tk.Label(self.master, text='Choose an Animal')
        lname = tk.Label(self.master, text='Choose a Name')
        listanimal = tk.Listbox(self.master)
        onlyA = self.master.register(lambda x: x.isalpha())
        ename = tk.Entry(self.master, validate='key',
                                            validatecommand=(onlyA, '%S'))

        submit = tk.Button(self.master, text='Create New Pet', command=lambda:
                    self.make_pet(ename.get(), listanimal.curselection()[0]))

        self.active_widgets = [lload, lname, ename,
                               lanimal, listanimal, submit]
        for widget in self.active_widgets:
            widget.pack()

        for animal in os.listdir('animals'):
            listanimal.insert(tk.END, animal[:-4])

    def make_pet(self, name, animal):
        if name in os.listdir('saves'):
            x = tk.Button(text='Name Already Exists',
                          command=lambda: x.destroy())
            x.pack()
            self.active_widgets.append(x)
        else:
            animal = os.listdir('animals')[animal]
            print(animal)
            self.select_pet(name, animal)

    def select_pet(self, name, animal=None):
        '''Makes class of for new pet, loads old information if
        it exists
        '''
        self.pet = Tamagotchi()
        self.pet.name = name

        self.pet.assign_folder()
        self.pet.pkl_stats(load=True)
        self.pet.animal_type(animal)
        self.display_pet()

    def bar_color(self, bar):
        '''Bar will change color on scale from red to green
        '''
        print(bar)
        x = self.pet.hh[bar]

        if x < 20:
            return 'red4'
        elif 20 <= x < 40:
            return 'orange red'
        elif 40 <= x < 60:
            return 'medium purple'
        elif 60 <= x < 80:
            return 'cyan3'
        elif 80 <= x:
            return 'green3'

    def hh_bars(self, set_up=False):
        '''Creates labels containing health and happiness values
        and canvases containing horizontal bars for visual representation
        '''
        if set_up:
            for stat in HEALTH, HAPPINESS:
                val = self.pet.hh[stat]
                color = self.bar_color(stat)

                label = tk.Label(self.master, text=stat + ': ')
                bar = tk.Canvas(self.master, width=100, height=10)
                bar.create_rectangle(0, 0, val, 10, fill=color, tags='bar')
                bar.create_rectangle(0, 0, 100, 10, outline='LightBlue4')

                if stat == HEALTH:
                    COL = 0
                    self.health_bar = bar
                else:
                    COL = 3
                    self.happiness_bar = bar

                label.grid(row=1, column=COL)
                bar.grid(row=1, column=COL+1)
                self.active_widgets.append(label)
                self.active_widgets.append(bar)

        elif not set_up:
            for bar, stat in [self.health_bar, HEALTH], \
                                    [self.happiness_bar, HAPPINESS]:
                val = self.pet.hh[stat]
                color = self.bar_color(stat)
                bar.delete('bar')
                bar.create_rectangle(0, 0, val, 10, fill=color, tags='bar')

    def show_image(self, ROW=0, COLUMN=0, cSpan=6):
        '''Adds a label containing PNG of animal
        '''
        img = Image.open('animals/' + self.pet.animal)
        png = ImageTk.PhotoImage(img)
        img_label = tk.Label(self.master, image=png)
        img_label.image=png
        img_label.grid(row=ROW, column=COLUMN, columnspan=cSpan)
        self.active_widgets.append(img_label)

    def display_pet(self):
        self.destroy_widgets()
        self.master.title(self.pet.name)
        self.show_image()
        self.hh_bars(set_up=True)
        self.display_seconds(set_up=True)
        self.active_window = PET_WINDOW
        self.thread = Thread(target=lambda: self.update_GUI)
        self.thread.start()

    def display_seconds(self, set_up=False):
        '''Shows how long until pet is ready to interact
        '''
        for i, string in enumerate(sorted(self.pet.time_strings.items())):
            string = string[0]
            time_string = self.pet.time_strings[string]
            if set_up:
                time_string = tk.StringVar()
                time_string.set(self.pet.seconds_left(string))
                label = tk.Label(self.master, textvariable=time_string)
                label.grid(row=3, column=i)
                self.active_widgets.append(label)
            else:
                time_string.set(self.pet.seconds_left(string))

    def update_GUI(self):
        if self.active_window == PET_WINDOW:
            self.pet.update_seconds()
            self.display_seconds()
            self.master.after(1000, self.update_GUI)