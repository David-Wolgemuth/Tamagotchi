from interactions import *
from constants import *
import pickle as pkl
import os
import time
import pdb

class Tamagotchi:
    def __init__(self):

        self.name = None
        self.animal = None
        self.folder = None

        self.hh = {
            HEALTH:None,
            HAPPINESS:None,
        }

        self.times = {
            EAT:None,
            DRINK:None,
            SLEEP:None,
            LOVE:None,
            PLAY:None,
        }
        self.time_strings = self.times.copy()

    def assign_folder(self):
        self.folder = 'saves/' + self.name

    def animal_type(self, animal=None):
        file_path = self.folder + '/animal_type.pkl'
        if os.path.isfile(file_path):
            self.animal = pkl.load(open(file_path, 'rb'))
        elif animal:
            pkl.dump(animal, open(file_path, 'wb'))
            self.animal = animal

    def pkl_stats(self, save=False, load=False):

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
                path = '%s/%s.pkl' % (folder, stat.lower())
                if load:
                    stat_group[stat] = pkl.load(open(path, 'rb'))
                if save:
                    if not value:
                        if stat_type == HH:
                            value = 50
                        elif stat_type == TIMES:
                            value = int(time.time())
                    pkl.dump(value, open(path, 'wb'))

    def update_seconds(self):
        for int_type in self.times:
            self.seconds_left(int_type)

    def seconds_left(self, int_type):
        now = int(time.time())
        last = self.times[int_type]
        left = last - now

        if not 0 < left < 1000000:
            left = READY
        return str(left)

    def change_stats(self, interaction):
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
        now = int(time.time())
        print('Now: %s' % now)
        print('Health: %s' % (self.hh[HEALTH]))
        print('Happiness: %s' % (self.hh[HAPPINESS]))
        print('Eat: %s' % (now-self.times[EAT]))
        print('Drink: %s' % (now-self.times[DRINK]))
        print('Sleep: %s' % (now-self.times[SLEEP]))
        print('Love: %s' % (now-self.times[LOVE]))
        print('Play: %s' % (now-self.times[PLAY]))

    def calculate_neglect(self):
        path = self.folder + 'neglect.pkl'
        now = int(time.time())
        if os.path.exists(path):
            last = pkl.load(open(path, 'rb'))
            if now - last > 1 * DAYS:
                for its in INTERACTION_TYPES:
                    i_type = INTERACTION_TYPES[its]
                    t = now - self.times[its]
                    while t > DAYS * i_type.neglect_days:
                        self.hh[HEALTH] -= i_type.neglect_health
                        self.hh[HAPPINESS] -= i_type.neglect_happiness
                        t -= 1 * DAYS
        pkl.dump(now, open(path, 'wb'))


if __name__=='__main__':
    frank = Tamagotchi()
    frank.name = "Frank/"
    frank.assign_folder()
    frank.pkl_stats(save=True)
    path = frank.folder + '/hh/' + 'happiness.pkl'
    print(pkl.load(open(path, 'rb')))
    path = frank.folder + '/times/' + 'sleep.pkl'
    print(pkl.load(open(path, 'rb')))