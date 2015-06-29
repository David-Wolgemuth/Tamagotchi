"""TamaTk class : Main class for displaying tkinter gui of pet"""

from constants import *
from interactions import *
from threading import Thread, current_thread
import tkinter as tk
from PIL import Image, ImageTk
from pet import Tamagotchi
import os
import shutil


class TamaTk:
    """Main tkinter gui for displaying enabling user interaction with the
    Tamagotchi pet
    """
    def __init__(self, master):
        self.master = master
        self.center_window()
        self.master.title('Animal Master')
        self.active_widgets = []
        self.saves = []
        self.pet = None
        self.thread = None
        self.current_interaction = None
        self.health_bar = None
        self.happiness_bar = None
        self.interaction_bar = None
        self.bars = []
        self.welcome_screen()

    def center_window(self):
        """Places window in the center of the computer's display"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('+%s+%s' % (x, y))

    def find_saves(self):
        """Loads all folders in the 'saves' directory"""
        self.saves = []
        if os.path.isdir('saves'):
            for folder in os.listdir('saves'):
                if os.path.isdir('saves/' + folder):
                    self.saves.append(folder)

    def destroy_widgets(self):
        """Destroys all active widgets"""
        for widget in self.active_widgets:
            widget.destroy()

    def welcome_screen(self):
        """Player has option between loading a pet or making a new one
        """
        self.destroy_widgets()
        self.find_saves()
        if not self.saves:
            self.new_pet_window()
            return

        new = tk.Button(self.master, text='Make New Pet',
                        command=self.new_pet_window)
        scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        old = tk.Listbox(self.master, yscrollcommand=scroll.set)
        scroll.config(command=old.yview)
        load = tk.Button(self.master, text='Load Pet', command=lambda:
                         self.select_pet(old.get(old.curselection()[0])))
        dlt = tk.Button(self.master, text='Delete Pet', command=lambda:
                        self.delete_pet(old.get(old.curselection()[0])))
        new.grid(row=0, column=0)
        load.grid(row=1, column=0)
        dlt.grid(row=2, column=0)
        scroll.grid(row=0, column=2, sticky=tk.N+tk.S, rowspan=3)
        old.grid(row=0, column=1, rowspan=3)
        for name in self.saves:
            old.insert(tk.END, name)
        self.center_window()
        self.active_widgets = [new, load, old, dlt, scroll]

    def new_pet_window(self):
        """Player creates a new pet, window has an Entry box and List
        of Animal types
        """
        self.destroy_widgets()
        load = tk.Button(self.master, text='Load Existing',
                         command=self.welcome_screen)
        choice = tk.Label(self.master, text='Choose an Animal')
        name = tk.Label(self.master, text='Choose a Name')
        scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        l_box = tk.Listbox(self.master, yscrollcommand=scroll.set)
        scroll.config(command=l_box.yview)
        alpha = self.master.register(lambda x: x.isalpha())
        entry = tk.Entry(self.master, validate='key',
                         validatecommand=(alpha, '%S'))
        submit = tk.Button(self.master, text='Create New Pet', command=lambda:
                           self.make_pet(entry.get(), l_box.curselection()[0]))
        self.active_widgets = [load, name, entry,
                               choice, l_box, submit]
        for widget in self.active_widgets:
            widget.grid()
        for animal in os.listdir('animals'):
            if animal[-4:] == '.png':
                l_box.insert(tk.END, animal[:-4])
        scroll.grid(row=4, column=1,sticky=tk.N+tk.S)
        self.center_window()

    def make_pet(self, name, animal):
        """Determines if pet name already exists, continues to
        'select_pet' function
        """
        if not os.path.exists('saves'):
            os.mkdir('saves')
        if name in os.listdir('saves'):
            x = tk.Button(text='Name Already Exists',
                          command=lambda: x.destroy())
            x.pack()
            self.active_widgets.append(x)
        else:
            animal = os.listdir('animals')[animal]
            self.select_pet(name, animal)

    def select_pet(self, name, animal=None):
        """Makes class of for new pet, loads old information if
        it exists
        """
        self.pet = Tamagotchi()
        self.pet.name = name
        self.pet.assign_folder()
        self.pet.pkl_stats(load=True)
        self.pet.calculate_neglect()
        self.pet.animal_type(animal)
        self.display_pet()

    def delete_pet(self, name, sure=False):
        """Deletes directory with pet name if sure, else creates button
        asking if sure
        """
        if sure:
            folder = 'saves/' + name
            shutil.rmtree(folder)
            self.saves.remove(name)
            self.welcome_screen()
            return

        # First time function is called, creates button
        self.destroy_widgets()
        message = 'Are you sure you want to PERMANENTLY delete %s?' % name
        lab = tk.Label(self.master, text=message)
        y = tk.Button(self.master, text='Yes, I\'m sure.',
                      command=lambda: self.delete_pet(name, sure=True))
        n = tk.Button(self.master, text='Cancel', command=self.welcome_screen)
        lab.grid(row=0, columnspan=2)
        n.grid(row=1, column=0)
        y.grid(row=1, column=1)
        self.active_widgets = [lab, y, n]

    def display_pet(self):
        """Main function that displays the pet
        """
        self.destroy_widgets()
        self.master.title(self.pet.name)
        self.return_to_welcome(setup=True)
        # self.print_stats()  # Uncomment when debugging
        self.show_image()
        if not self.pet.neglect:
            self.hh_bars(set_up=True)
            self.display_seconds(set_up=True)
            self.display_menu_buttons()
            if not self.thread:
                self.thread = Thread(target=self.update)
                self.thread.start()
        else:
            self.display_neglect()
        self.center_window()

    def return_to_welcome(self, setup=False):
        """Creates button or returns to main menu"""
        if setup:
            but = tk.Button(self.master, text='Main Menu',
                            command=self.return_to_welcome)
            but.grid(columnspan=6)
            self.active_widgets.append(but)
        else:
            self.pet = self.thread = None
            self.welcome_screen()

    def print_stats(self):
        """Creates a button to be used during debugging
        """
        but = tk.Button(self.master, text='show stats',
                        command=self.pet.print_stats)
        but.grid(row=0, column=5)
        self.active_widgets.append(but)

    def show_image(self, row=1, column=0, c_span=6):
        """Adds a label containing PNG of animal
        """
        img = Image.open('animals/' + self.pet.animal)
        png = ImageTk.PhotoImage(img)
        img_label = tk.Label(self.master, image=png)
        img_label.image = png
        img_label.grid(row=row, column=column, columnspan=c_span)
        self.active_widgets.append(img_label)

    def bar_color(self, bar):
        """Returns color on scale from red to green"""
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
        """Creates labels containing health and happiness values
        and canvases containing horizontal bars for visual representation
        """
        if set_up:
            for stat in HEALTH, HAPPINESS:
                val = self.pet.hh[stat]
                color = self.bar_color(stat)

                label = tk.Label(self.master, text=stat + ': ')
                bar = tk.Canvas(self.master, width=100, height=10)
                bar.create_rectangle(0, 0, val, 10, fill=color, tags='bar')
                bar.create_rectangle(0, 0, 100, 10, outline='LightBlue4')

                if stat == HEALTH:
                    column = 0
                    self.health_bar = bar
                else:
                    column = 3
                    self.happiness_bar = bar

                label.grid(row=2, column=column)
                bar.grid(row=2, column=column+1)
                self.active_widgets.append(label)
                self.active_widgets.append(bar)

        elif not set_up:
            for bar, stat in [self.health_bar, HEALTH], \
                             [self.happiness_bar, HAPPINESS]:
                val = self.pet.hh[stat]
                color = self.bar_color(stat)
                bar.delete('bar')
                bar.create_rectangle(0, 0, val, 10, fill=color, tags='bar')

    def display_seconds(self, set_up=False):
        """Shows how long until pet is ready to interact"""
        for i, string in enumerate(sorted(self.pet.time_strings.items())):
            string = string[0]
            time_strings = self.pet.time_strings
            if set_up:
                time_strings[string] = tk.StringVar()
                time_strings[string].set(self.pet.seconds_left(string))
                label = tk.Label(self.master,
                                 textvariable=time_strings[string])
                label.grid(row=3, column=i)
                self.active_widgets.append(label)
            else:
                time_strings[string].set(self.pet.seconds_left(string))

    def display_menu_buttons(self):
        """Menu-bars corresponding to types of interactions
        """
        for i, i_type in enumerate(sorted(INTERACTION_TYPES)):
            m_button = tk.Menubutton(self.master, text=i_type)
            m_button.grid(row=4, column=i)
            m_button.menu = tk.Menu(m_button)
            m_button['menu'] = m_button.menu
            for I in INTERACTION_TYPES[i_type].interactions:
                m_button.menu.add_checkbutton(label=I, command=lambda I=I:
                                              self.interact_with_pet(I))
            self.active_widgets.append(m_button)

    def display_neglect(self):
        """Informs user if pet has died or run away
        """
        pet = self.pet
        message = self.pet.neglect
        if pet.neglect == HEALTH:
            message = '%s has died because of your neglect.' % pet.name
        elif pet.neglect == HAPPINESS:
            message = '%s has become too unhappy and has run away.' % pet.name
        lab = tk.Label(self.master, text=message)
        lab.grid(columnspan=5)
        self.active_widgets.append(lab)

    def interact_with_pet(self, interaction):
        """Activated by menubutton.  If ready, continues to
        'display_interaction' function, else button informs user
        """
        i_type = get_interaction_type(interaction)
        is_ready = self.pet.seconds_left(i_type)
        if is_ready == READY:
            self.display_interaction(interaction)
        else:
            message = '%s is not ready to %s' % (self.pet.name, i_type)
            but = tk.Button(self.master, text=message,
                            command=lambda: but.destroy())
            but.grid(columnspan=6)
            self.active_widgets.append(but)

    def display_interaction(self, interaction):
        """Displays a bar to indicate the progress of the interaction
        includes a button to cancel the interaction
        """
        self.destroy_widgets()
        self.show_image()

        message = 'Stop %s from %s.' % (self.pet.name,
                                        INTERACTIONS[interaction].text)
        stop = tk.Button(self.master, text=message,
                         command=self.stop_interaction)
        stop.grid()
        self.active_widgets.append(stop)

        self.interaction_bar = tk.Canvas(self.master, width=500, height=40)
        self.interaction_bar.grid()
        self.interaction_bar.create_rectangle(0, 0, 0, 40,
                                              fill='medium purple',
                                              tags='bar')
        self.active_widgets.append(self.interaction_bar)
        self.current_interaction = [interaction, 0]
        self.center_window()

    def stop_interaction(self):
        """Activated if user presses 'Stop' button during interaction"""
        self.pet.change_stats('Stop')  # Removes 2 points from pet's happiness
        self.current_interaction = None
        self.display_pet()

    def update_interaction(self):
        """Loading Bar and cancel button to signify that you are
        interacting with the pet and cannot do anything at the moment
        """
        interaction = INTERACTIONS[self.current_interaction[0]]
        current = self.current_interaction[1]
        duration = interaction.action_time
        percent = (current / duration) * 100
        if percent > 100:
            self.current_interaction = None
            self.pet.change_stats(interaction.interaction)
            self.display_pet()
            return
        else:
            self.interaction_bar.delete('bar')
            self.interaction_bar.create_rectangle(0, 0, 5*percent, 40,
                                                  fill='medium purple',
                                                  tags='bar')
        self.current_interaction[1] += 1

    def update(self):
        """Second thread will either update the interaction screen,
        the seconds on the main display, or finish if no pet
        """
        if self.current_interaction:
            self.update_interaction()
            self.master.after(1000, self.update)
            # print(self.current_interaction)#, current_thread())
        elif self.pet:
            self.pet.update_seconds()
            self.display_seconds()
            self.master.after(1000, self.update)

if __name__ == '__main__':
    print('\n%s' % __doc__)
    print('class TamaTk:')
    functions = dir(TamaTk)
    for function in functions:
        if function[0] != '_':
            print('\t> ' + function)
