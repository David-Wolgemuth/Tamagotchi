"""Tamagotchi Class : Main class that defines the pet"""

from interactions import *
from constants import *
import pickle as pkl
import os
import time


class Tamagotchi:
    """Main class that defines the Tamagotchi pet.  Handles all
     stats and saving stats.
    """
    def __init__(self):
        self.name = ''
        self.animal = ''
        self.folder = ''
        self.neglect = False
        self.hh = {
            HEALTH: 0,
            HAPPINESS: 0,
        }
        self.times = {
            EAT: 0,
            DRINK: 0,
            SLEEP: 0,
            LOVE: 0,
            PLAY: 0,
        }
        self.time_strings = self.times.copy()

    def assign_folder(self):
        """Sets folder to be 'saves/____' """
        self.folder = 'saves/' + self.name

    def animal_type(self, animal=None):
        """Assigns animal type to pet.  Loads if pickle exists, else saves
        pickle file
        """
        file = self.folder + '/animal_type.pkl'
        if os.path.isfile(file):
            self.animal = pkl.load(open(file, 'rb'))
        elif animal:
            pkl.dump(animal, open(file, 'wb'))
            self.animal = animal

    def pkl_stats(self, save=False, load=False):
        """Pickles stats for Health, Happiness, and last time for each
        interaction with pet.  Will create new stats if .pkl files do
        not exist.
        """
        for stat_type in HH, TIMES:
            if stat_type == HH:
                stat_group = self.hh
            elif stat_type == TIMES:
                stat_group = self.times

            folder = '%s/%s' % (self.folder, stat_type)
            if not os.path.exists('saves'):
                os.mkdir('saves')
            if not os.path.exists(self.folder):
                os.mkdir(self.folder)
            if not os.path.exists(folder):
                os.mkdir(folder)
                self.pkl_stats(save=True)
                return

            for stat in stat_group:
                value = stat_group[stat]
                file = '%s/%s.pkl' % (folder, stat.lower())
                if load:
                    stat_group[stat] = pkl.load(open(file, 'rb'))
                if save:
                    if not value:
                        if stat_type == HH:
                            stat_group[stat] = 50
                        elif stat_type == TIMES:
                            stat_group[stat] = int(time.time())
                    pkl.dump(value, open(file, 'wb'))

    def update_seconds(self):
        """Updates all seconds in self.times"""
        for int_type in self.times:
            self.seconds_left(int_type)

    def seconds_left(self, int_type):
        """Called with 'update_seconds' function and returns string
        to be used in 'TamaTk.display_seconds' function
        """
        now = int(time.time())
        last = self.times[int_type]
        left = last - now

        if not 0 < left < 1000000:
            left = READY
        return str(left)

    def change_stats(self, interaction):
        """Reads interaction and alters pet's stats"""
        int_object = INTERACTIONS[interaction]
        self.hh[HAPPINESS] += int_object.happiness
        self.hh[HEALTH] += int_object.health

        int_type = get_interaction_type(interaction)
        if int_type:
            now = int(time.time())
            wait = int_object.wait_time
            self.times[int_type] = now + wait

        self.pkl_stats(save=True)

    def print_stats(self):
        """Prints pet Stats. Used for debugging only"""
        now = int(time.time())
        print('Now: %s' % now)
        print('Health: %s' % (self.hh[HEALTH]))
        print('Happiness: %s' % (self.hh[HAPPINESS]))
        print('Eat: %s' % (now-self.times[EAT]))
        print('Drink: %s' % (now-self.times[DRINK]))
        print('Sleep: %s' % (now-self.times[SLEEP]))
        print('Love: %s' % (now-self.times[LOVE]))
        print('Play: %s' % (now-self.times[PLAY]))
        print('<-------------->')

    def calculate_neglect(self):
        """Alters pet health/happiness based on length of time since
        last interaction
        """
        file = self.folder + '/neglect.pkl'
        now = int(time.time())
        if os.path.exists(file):
            last = pkl.load(open(file, 'rb'))
            if now - last > 1 * DAYS:  # Gives user 1 day to care for pet
                for its in INTERACTION_TYPES:
                    i_type = INTERACTION_TYPES[its]
                    t = now - self.times[its]
                    while t > DAYS * i_type.neglect_days:
                        self.hh[HEALTH] -= i_type.neglect_health
                        self.hh[HAPPINESS] -= i_type.neglect_happiness
                        t -= 1 * DAYS
                        pkl.dump(now, open(file, 'wb'))
        else:
            pkl.dump(now, open(file, 'wb'))
        self.is_neglected()

    def is_neglected(self):
        """Sets self.neglect to 'health' or 'happiness' if neglected"""
        if self.hh[HEALTH] < 0:
            self.neglect = HEALTH
            return
        if self.hh[HAPPINESS] < 0:
            self.neglect = HAPPINESS


if __name__ == '__main__':
    frank = Tamagotchi()
    frank.name = "Frank/"
    frank.assign_folder()
    frank.pkl_stats(save=True)
    path = frank.folder + '/hh/' + 'happiness.pkl'
    print(pkl.load(open(path, 'rb')))
    path = frank.folder + '/times/' + 'sleep.pkl'
    print(pkl.load(open(path, 'rb')))
