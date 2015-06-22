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
        self.health_string = StringVar()
        self.happiness_string = StringVar()
        self.health_bar = None
        self.happiness_bar = None

        if os.path.exists('saves/saves.pkl'):
            self.pet_saves = pk.load(open('saves/saves.pkl', 'rb'))
            self.welcome_screen()
        else:
            os.mkdir('saves')
            self.pet_saves = []
            pk.dump(self.pet_saves, open('saves/saves.pkl', 'wb'))
            self.new_pet_window()

    def destroy_widgets(self):
        for widget in self.active_widgets:
            widget.destroy()

    def welcome_screen(self):
        '''Player has option between loading a pet or making a new one
        '''
        new = Button(self.master, text='Make New Pet',
                                command=self.new_pet_window)
        old = Listbox(self.master)
        load = Button(self.master, text='Load', command=lambda:
                        self.select_pet(old.get(old.curselection()[0])))

        self.destroy_widgets()
        new.grid(row=0, column=0)
        load.grid(row=0, column=1)
        old.grid(row=1, column=0, columnspan=2)
        self.active_widgets = [new, old, load]

        for name in pk.load(open('saves/saves.pkl', 'rb')):
            old.insert(END, name)

    def select_pet(self, name, animal=None):
        '''If pet exists, load the pet information, otherwise creates
        new directory
        '''
        self.pet = Tamagotchi()
        self.pet.name = name
        self.pet.folder = 'saves/' + name + '_saves/'

        folder = self.pet.folder
        hhfolder = folder + 'hhbars/'

        if  not os.path.exists(folder):
            os.mkdir(folder)
            pk.dump(animal, open(folder + 'animal_type.pkl', 'wb'))
            os.mkdir(hhfolder)
            pk.dump(50, open(hhfolder + 'happiness.pkl', 'wb'))
            pk.dump(50, open(hhfolder + 'health.pkl', 'wb'))

        self.pet.animal = pk.load(open(folder + 'animal_type.pkl', 'rb'))
        self.pet.happiness = pk.load(open(hhfolder + 'happiness.pkl', 'rb'))
        self.pet.health = pk.load(open(hhfolder + 'health.pkl', 'rb'))
        self.display_pet()

    def interaction(self, interaction, option):
        '''Processes Menubutton -- if pet is not ready, will return a message
        to player
        '''
        ready = self.pet.interact(interaction, option)

        if ready:
            self.health_happiness(update=True)
            self.pet.health_happiness(save=True)
        else:
            message = '%s is not ready to %s.' % (self.pet.name, interaction)
            x = Button(text=message, command=lambda: x.destroy())
            x.grid(columnspan=6)
            self.active_widgets.append(x)

    def interacting_screen(self, interaction):
        '''Make a Loading Bar? (maybe a cancel button)? to signify that you are
        interacting with the pet and cannot do anything at the moment... Possibly
        even a new window demonstrating what's happening?...
        '''
        self.destroy_widgets()


    def new_pet_window(self):
        '''Player creates a new pet, window has an Entry box and List
        of Animal types
        '''
        lload = Button(self.master, text='Load Existing',
                                    command = self.welcome_screen)
        lanimal = Label(self.master, text='Choose an Animal')
        lname = Label(self.master, text='Choose a Name')
        listanimal = Listbox(self.master)
        onlyA = self.master.register(lambda x: x.isalpha())
        ename = Entry(self.master, validate='key',
                      validatecommand=(onlyA, '%S'))

        submit = Button(self.master, text='Create New Pet', command=lambda:
                    self.make_pet(ename.get(), listanimal.curselection()[0]))

        self.destroy_widgets()

        self.active_widgets = [lload, lname, ename, lanimal, listanimal, submit]
        for widget in self.active_widgets:
            widget.pack()

        for animal in os.listdir('animals'):
            listanimal.insert(END, animal[:-4])

    def make_pet(self, name, animal):
        '''Creates a directory for animal and puts animal name in
        save directory
        '''
        save_file = 'saves/saves.pkl'
        if name in pk.load(open(save_file, 'rb')):
            self.error_page('Name Already Exists')
        else:
            out_animal = os.listdir('animals')[animal]
            self.pet_saves = pk.load(open(save_file, 'rb'))
            self.pet_saves.append(name)
            pk.dump(self.pet_saves, open(save_file, 'wb'))
            self.select_pet(name, out_animal)

    def bar_color(self, bar):
        '''Bar will change color on scale from red to green
        '''
        if bar == 'health':
            x = self.pet.health
        elif bar == 'happiness':
            x = self.pet.happiness

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
        '''The main window for interacting with pet
        '''
        self.destroy_widgets()
        self.master.title(self.pet.name)
        self.show_image()
        self.pet.health_happiness(load=True)
        self.health_happiness()
        self.pet.wait_times()
        self.display_seconds(initial=True)
        self.interaction_menu()
        self.thread = Thread(target=self.update_pet)
        self.thread.start()

    def show_image(self):
        '''Adds a label containing PNG of animal
        '''
        img = Image.open('animals/' + self.pet.animal)
        png = ImageTk.PhotoImage(img)
        img_label = Label(self.master, image=png)
        img_label.image=png
        img_label.grid(row=0, columnspan=6)
        self.active_widgets.append(img_label)

    def health_happiness(self, update=False):
        '''Creates labels containing health and happiness values
        and canvases containing horizontal bars for visual representation
        '''
        if update:
            self.health_string.set('Health: ' + str(self.pet.health))
            self.happiness_string.set('Happiness: ' + str(self.pet.happiness))
            self.health_bar.delete('bar')
            self.happiness_bar.delete('bar')
            self.health_bar.create_rectangle(0, 0, self.pet.health, 10,
                                       fill=self.bar_color('health'), tags='bar')
            self.happiness_bar.create_rectangle(0, 0, self.pet.happiness, 10,
                                          fill=self.bar_color('happiness'), tags='bar')
            return

        self.health_string.set('Health: ' + str(self.pet.health))
        health_label = Label(self.master,
                             textvariable=self.health_string)
        self.health_bar = Canvas(self.master, width=100, height=10)
        self.health_bar.create_rectangle(0, 0, self.pet.health, 10,
                                       fill=self.bar_color('health'), tags='bar')
        self.health_bar.create_rectangle(0, 0, 100, 10, outline='LightBlue4')

        self.happiness_string.set('Happiness: ' + str(self.pet.happiness))
        happiness_label = Label(self.master,
                                textvariable=self.happiness_string)
        self.happiness_bar = Canvas(self.master, width=100, height=10)
        self.happiness_bar.create_rectangle(0, 0, self.pet.happiness, 10,
                                          fill=self.bar_color('happiness'), tags='bar')
        self.happiness_bar.create_rectangle(0, 0, 100, 10, outline='LightBlue4')

        health_label.grid(row=1, column=0)
        self.health_bar.grid(row=1, column=1)
        happiness_label.grid(row=1, column=3)
        self.happiness_bar.grid(row=1, column=4)
        
        for widget in health_label, self.health_bar, \
                            happiness_label, self.happiness_bar:
            self.active_widgets.append(widget)

    def update_pet(self):
        '''Every second, updates the times related to pet interactions
         '''
        if self.pet.health:
            self.display_seconds()
        self.master.after(1000, self.update_pet)

    def display_seconds(self, initial=False):
        '''Shows how long until pet is ready to interact
        '''
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

    def seconds_left(self, condition):
        '''Called during update to returns how many seconds are left before
        pet is ready to interact
        '''
        waittime = condition['last_time']
        now = int(time.time())
        folder = self.pet.folder + '/wait_times/'
        file = condition['type'] + '.pkl'
        last = pk.load(open(folder + file, 'rb'))
        wait = last - now
        print('%s: %s = %s - %s' % (condition['type'], wait, last, now))
        if 0 < wait <1000000:
            return str(wait)
        else:
            return 'Ready'

    def interaction_menu(self):
        '''Menubars corrisponding to types of interactions
        '''
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


if __name__ == '__main__':
    root = Tk()
    gui = TamaWindow(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()
