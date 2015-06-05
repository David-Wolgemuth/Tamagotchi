from tkinter import *
from threading import Thread
from tama import Tamagotchi
import pickle as pk
import os
from PIL import Image, ImageTk
import time
import pdb

class TamaWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Tamagotchi')
        self.active_widgets = []
        self.pet = None

        if os.path.exists('saves.pkl'):
            self.pet_saves = pk.load(open('saves.pkl', 'rb'))
            self.welcome_screen()
        else:
            self.pet_saves = []
            pk.dump(self.pet_saves, open('saves.pkl', 'wb'))
            self.new_pet_window()

    def update_pet(self):
        if self.pet.health:
            self.pet.update()
            self.display_seconds()
        self.master.after(1000, self.update_pet)

    def destroy_widgets(self):
        for widget in self.active_widgets:
            widget.destroy()

    def welcome_screen(self):
        new = Button(self.master, text='Make New Pet',
                                command=self.new_pet_window)
        old = Listbox(self.master)
        load = Button(self.master, text='Load Pet', command=lambda:
                        self.select_pet(old.get(old.curselection()[0])))

        self.destroy_widgets()
        new.grid(row=0, column=0)
        load.grid(row=0, column=1)
        old.grid(row=1, column=0, columnspan=2)
        self.active_widgets = [new, old, load]

        for name in pk.load(open('saves.pkl', 'rb')):
            old.insert(END, name)

    def select_pet(self, name, animal=None):
        self.pet = Tamagotchi()
        self.pet.name = name
        self.pet.folder = folder = name + '_saves/'

        if  not os.path.exists(folder):
            os.mkdir(folder)
            pk.dump(animal, open(folder + 'animal_type.pkl', 'wb'))
            pk.dump(50, open(folder + 'happiness.pkl', 'wb'))
            pk.dump(50, open(folder + 'health.pkl', 'wb'))

        self.pet.animal = pk.load(open(folder + 'animal_type.pkl', 'rb'))
        self.pet.happiness = pk.load(open(folder + 'happiness.pkl', 'rb'))
        self.pet.health = pk.load(open(folder + 'health.pkl', 'rb'))
        self.pet.update()
        self.display_pet()

    def interaction(self, interaction, option):

        ready = self.pet.interact(interaction, option)

        if not ready:
            message = '%s is not ready to %s.' % (self.pet.name, interaction)
            x = Button(text=message, command=lambda: x.destroy())
            x.grid(columnspan=6)
            self.active_widgets.append(x)

    def new_pet_window(self):
        lanimal = Label(self.master, text='Choose an Animal')
        lname = Label(self.master, text='Choose a Name')
        listanimal = Listbox(self.master)
        onlyA = self.master.register(lambda x: x.isalpha())
        ename = Entry(self.master, validate='key',
                      validatecommand=(onlyA, '%S'))

        submit = Button(self.master, text='Submit', command=lambda:
                    self.make_pet(ename.get(), listanimal.curselection()[0]))

        for widget in self.active_widgets:
            widget.destroy()

        self.active_widgets = [lname, ename, lanimal, listanimal, submit]
        for widget in self.active_widgets:
            widget.pack()

        for animal in os.listdir('animals'):
            listanimal.insert(END, animal[:-4])

    def bar_color(self, bar):
        if bar == 'health':
            x = self.pet.health
        elif bar == 'happiness':
            x = self.pet.health

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


    def display_pet(self):
        self.destroy_widgets()
        self.master.title(self.pet.name)
        self.show_image()
        self.health_happiness()
        self.display_seconds(initial=True)
        self.interaction_menu()
        self.thread = Thread(target=self.update_pet)
        self.thread.start()

    def show_image(self):
        img = Image.open('animals/' + self.pet.animal)
        png = ImageTk.PhotoImage(img)
        img_label = Label(self.master, image=png)
        img_label.image=png
        img_label.grid(row=0, columnspan=6)
        self.active_widgets.append(img_label)

    def health_happiness(self):
        health_label = Label(self.master, text='Health: ')
        health_canvas = Canvas(self.master, width=100, height=10)
        health_canvas.create_rectangle(0, 0, self.pet.health, 10,
                                       fill=self.bar_color('health'))
        health_canvas.create_rectangle(0, 0, 100, 10, outline='LightBlue4')

        happiness_label = Label(self.master, text='Happiness: ')
        happiness_canvas = Canvas(self.master, width=100, height=10)
        happiness_canvas.create_rectangle(0, 0, self.pet.happiness, 10,
                                          fill=self.bar_color('happiness'))
        happiness_canvas.create_rectangle(0, 0, 100, 10, outline='LightBlue4')

        health_label.grid(row=1, column=0)
        health_canvas.grid(row=1, column=1)
        happiness_label.grid(row=1, column=3)
        happiness_canvas.grid(row=1, column=4)
        
        for widget in health_label, health_canvas, \
                            happiness_label, happiness_canvas:
            self.active_widgets.append(widget)

    def seconds_left(self, condition):
        waittime = condition['wait']
        now = int(time.time())
        last = pk.load(open(self.pet.folder + condition['file'], 'rb'))
        wait = waittime - (now - last)
        if wait > 0:
            return str(wait)
        else:
            return 'Ready'

    def display_seconds(self, initial=False):
        for i, condition in enumerate(self.pet.conditions):
            if initial:
                condition['timestring'] = StringVar()
                condition['timestring'].set(self.seconds_left(condition))
                tlabel = Label(self.master, text=condition['type'])
                label = Label(self.master, textvariable=condition['timestring'])
                tlabel.grid(row=2, column=i)
                label.grid(row=3, column=i)
                self.active_widgets.append(label)
            else:
                condition['timestring'].set(self.seconds_left(condition))

    def interaction_menu(self):
        for i, condition in enumerate(self.pet.conditions):
            interaction = condition['type']
            m_button = Menubutton(self.master, text=interaction)
            m_button.grid()
            m_button.menu = Menu(m_button)
            m_button['menu'] = m_button.menu
            for option in self.pet.interactions[interaction]:
                m_button.menu.add_checkbutton(label=option[0],
                        command=lambda int=interaction, opt=option[0]:
                                            self.interaction(int, opt))
            self.active_widgets.append(m_button.grid)
            m_button.grid(row=4, column=i)

    def make_pet(self, name, animal):
        if name in pk.load(open('saves.pkl', 'rb')):
            self.error_page('Name Already Exists')
        else:
            out_animal = os.listdir('animals')[animal]
            self.pet_saves = pk.load(open('saves.pkl', 'rb'))
            self.pet_saves.append(name)
            pk.dump(self.pet_saves, open('saves.pkl', 'wb'))
            self.select_pet(name, out_animal)

if __name__ == '__main__':
    root = Tk()
    gui = TamaWindow(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()
