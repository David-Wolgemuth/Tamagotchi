import time
import os
import pickle as pkl
import pdb

MINUTES = 60
HOURS = MINUTES * 60
DAYS = HOURS * 24

class Tamagotchi:
    def __init__(self):

        self.name = None
        self.animal = None
        self.folder = None

        now = int(time.time())

        self.eat = {'last_time':now, 'type':'Eat', 'timestring':None}
        self.sleep = {'last_time':now, 'type':'Sleep', 'timestring':None}
        self.play = {'last_time':now, 'type':'Play', 'timestring':None}
        self.love = {'last_time':now, 'type':'Love', 'timestring':None}
        self.drink = {'last_time':now, 'type':'Drink', 'timestring': None}

        self.interactions = {
            # Action, Wait Time, Health, Happiness, Action Time
            'Eat':[['Cheeseburger', 3 * HOURS, -1, 1, 45],
                    ['Salad', 90 * MINUTES, 1, -1, 20],
                    ['Pizza', 4 * HOURS, -2, 2, 30],
                    ['Celery', 30 * MINUTES, 2, -2, 10]
                    ],
            'Drink':[['Water', 2 * HOURS, 0, 0, 10],
                      ['Soda', 2 * HOURS, -1, 1, 10],
                      ['Coffee', 90 * MINUTES, 0, 1, 10],
                      ['Beer', 30 * MINUTES, -1, 2, 10]
                    ],
            'Love':[['Hug', 2 * HOURS, 0, 3, 30],
                       ['Pet', 30 * MINUTES, 0, 1, 10],
                       ],
            'Play':[['Basketball', 4 * HOURS, 3, 3, 120],
                    ['Frisbee', 3 * HOURS, 2, 4, 60],
                    ['Watch TV', 1 * HOURS, -1, 3, 60]
                    ],
            'Sleep':[['Sleep', 12 * HOURS, 6, 6, 2 * HOURS],
                     ['Nap', 4 * HOURS, 0, 3, 30 * MINUTES]]
        }

        # Wellness
        self.health = None
        self.happiness = None
        self.conditions = [self.eat, self.sleep, self.drink,
                                        self.play, self.love]

    def alter_hh(self, health=False, happiness=False, amount=0):
        if health:
            self.health += amount
        if happiness:
            self.happiness += amount
        self.health_happiness(save=True)

    def interact(self, interaction, option, test_ready=False):
        '''Called when Player interacts with Pet --  Returns False if
        Pet is not ready to interact
        '''
        for cond in self.conditions:
            if cond['type'] == interaction:
                condition = cond
        folder = self.folder + 'wait_times/'
        file = condition['type'] + '.pkl'
        now = int(time.time())
        old = pkl.load(open(folder + file, 'rb'))

        if now - old > 0:
            if test_ready:
                for action in self.interactions[condition['type']]:
                    if action[0] == option:
                        return action[4] #Duration
            else:
                pkl.dump(now, open(folder + file, 'wb'))
                for action in self.interactions[condition['type']]:
                    if action[0] == option:
                        pkl.dump(now + action[1], open(folder + file, 'wb'))
                        self.health += action[2]
                        self.happiness += action[3]
                        return
        else:
            return False

    def wait_times(self):
        '''Pickle saves and loads wait_times for interactions
         '''
        folder = self.folder + 'wait_times/'
        if os.path.exists(folder[:-1]):
            for con in self.conditions:
                path = folder + con['type'] + '.pkl'
                con['last_time'] = pkl.load(open(path, 'rb'))
        else:
            os.mkdir(folder[:-1])
            for con in self.conditions:
                path = folder + con['type'] + '.pkl'
                pkl.dump(con['last_time'], open(path, 'wb'))

    def health_happiness(self, load=False, save=False):
        '''Pickle saves and loads health and happiness values
        '''
        folder = self.folder + 'hhbars'
        health = '/health.pkl'
        happy = '/happiness.pkl'

        if load:
            if os.path.exists(folder):
                self.health = pkl.load(open(folder + health, 'rb'))
                self.happiness = pkl.load(open(folder + happy, 'rb'))
            else:
                os.mkdir(folder)
                pkl.dump(self.health, open(folder + health, 'wb'))
                pkl.dump(self.happiness, open(folder + happy, 'wb'))

        if save:
            if self.health > 100:
                self.health = 100
            if self.happiness > 100:
                self.happiness = 100

            pkl.dump(self.health, open(folder + health, 'wb'))
            pkl.dump(self.happiness, open(folder + happy, 'wb'))

    def interaction_text(self, interaction, option):
        if option == 'Sleep':
            return 'sleeping'
        elif option == 'Nap':
            return 'taking a nap'
        elif interaction == 'Play':
            if option == 'Watch TV':
                return 'watching TV'
            else:
                return 'playing ' + option.lower()
        elif interaction == 'Eat':
            if option == 'Hamburger':
                return 'eating a hamburger'
            return 'eating ' + option.lower()
        elif interaction == 'Drink':
            return 'drinking ' + option.lower()
        elif option == 'Hug':
            'receiving a hug'
        elif option == 'Pet':
            'being petted'

if __name__ == '__main__':
    pet = Tamagotchi()
    pet.update()
    i = 0
    a = input('Allievate?')
    for at in pet.conditions:
        if a == at['file']:
            pet.allieviate(at)
    pet.update()
    for att in pet.conditions:
        print(att['file'][:-2], ': ', att['att'])