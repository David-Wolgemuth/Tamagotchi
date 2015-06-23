import time
import os
import pickle
import pdb

MINUTES = 10
HOURS = MINUTES * 10
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
            'Eat':[['Cheeseburger', 3 * HOURS, -1, 1, 20],
                    ['Salad', 90 * MINUTES, 1, -1, 20],
                    ['Pizza', int(3.5 * HOURS), -2, 2, 30],
                    ['Celery', 30 * MINUTES, 2, -2, 10]
                    ],
            'Drink':[['Water', 2 * HOURS, 0, 0, 10],
                      ['Soda', 1 * HOURS, -1, 1, 10],
                      ['Coffee', 90 * MINUTES, 0, 1, 10],
                      ['Beer', 30 * MINUTES, -1, 2, 10]
                    ],
            'Love':[['Hug', 2 * HOURS, 0, 3, 20],
                       ['Pet', 30 * MINUTES, 0, 1, 5],
                       ],
            'Play':[['Basketball', 4 * HOURS, 3, 3, 45],
                    ['Frisbee', 3 * HOURS, 2, 4, 45],
                    ['Watch TV', 1 * HOURS, -1, 3, 45]
                    ],
            'Sleep':[['Sleep', 12 * HOURS, 2, 2, 3 * HOURS],
                     ['Nap', 4 * HOURS, 0, 3, 30 * MINUTES]]
        }

        # Wellness
        self.health = None
        self.happiness = None
        self.conditions = [self.eat, self.sleep, self.drink,
                                        self.play, self.love]

    def interact(self, interaction, option):
        '''Called when Player interacts with Pet --  Returns False if
        Pet is not ready to interact
        '''
        for cond in self.conditions:
            if cond['type'] == interaction:
                condition = cond
        folder = self.folder + 'wait_times/'
        file = condition['type'] + '.pkl'
        now = int(time.time())
        old = pickle.load(open(folder + file, 'rb'))

        if now - old > 0:
            pickle.dump(now, open(folder + file, 'wb'))
            for action in self.interactions[condition['type']]:
                if action[0] == option:
                    pickle.dump(now + action[1], open(folder + file, 'wb'))
                    self.health += action[2]
                    self.happiness += action[3]
                    return True
        else:
            return False

    def wait_times(self):
        '''Pickle saves and loads wait_times for interactions
         '''
        folder = self.folder + 'wait_times/'
        if os.path.exists(folder[:-1]):
            for con in self.conditions:
                path = folder + con['type'] + '.pkl'
                con['last_time'] = pickle.load(open(path, 'rb'))
        else:
            os.mkdir(folder[:-1])
            for con in self.conditions:
                path = folder + con['type'] + '.pkl'
                pickle.dump(con['last_time'], open(path, 'wb'))

    def health_happiness(self, load=False, save=False):
        '''Pickle saves and loads health and happiness values
        '''
        folder = self.folder + 'hhbars'
        health = '/health.pkl'
        happy = '/happiness.pkl'

        if load:
            if os.path.exists(folder):
                self.health = pickle.load(open(folder + health, 'rb'))
                self.happiness = pickle.load(open(folder + happy, 'rb'))
            else:
                os.mkdir(folder)
                pickle.dump(self.health, open(folder + health, 'wb'))
                pickle.dump(self.happiness, open(folder + happy, 'wb'))

        if save:
            if self.health > 100:
                self.health = 100
            if self.happiness > 100:
                self.happiness = 100

            pickle.dump(self.health, open(folder + health, 'wb'))
            pickle.dump(self.happiness, open(folder + happy, 'wb'))


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