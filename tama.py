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

        self.hungry = {'att':False, 'wait':3, 'file':'hungry.pkl',
                       'type':'Eat', 'timestring':None}
        self.tired = {'att':False, 'wait':6 , 'file':'tired.pkl',
                      'type':'Sleep', 'timestring':None}
        self.bored = {'att':False, 'wait':30, 'file':'bored.pkl',
                      'type':'Play', 'timestring':None}
        self.lonely = {'att':False, 'wait':1, 'file':'lonely.pkl',
                       'type':'Love', 'timestring':None}
        self.thirsty = {'att':False, 'wait':45, 'file':'thirsty.pkl',
                        'type':'Drink', 'timestring': None}

        self.interactions = {
            # Action, Wait_Time, Health, Happiness, Action_Time
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

        self.conditions = [self.hungry, self.tired,
                           self.bored, self.lonely,
                           self.thirsty]

    def interact(self, in_condition, interaction):
        '''Called when Player interacts with Pet --  Returns False if
        Pet is not ready to interact
        '''
        for cond in self.conditions:
            if cond['type'] == in_condition:
                condition = cond

        now = int(time.time())
        old = pickle.load(open(self.folder + condition['file'], 'rb'))

        if now - old > condition['wait']:
            pickle.dump(now, open(self.folder + condition['file'], 'wb'))
            for action in self.interactions[condition['type']]:
                if action[0] == interaction:
                    condition['wait'] = action[1]
                    self.health += action[2]
                    self.happiness += action[3]
                    self.wait_times(save=True)
                    return True
        else:
            return False

    def wait_times(self, load=False, save=False):
        '''Pickle saves and loads wait_times for interactions
         '''
        folder = self.folder + 'wait_times/'
        if os.path.exists(folder[:-1]):
            for con in self.conditions:
                path = folder + con['type'] + '.pkl'
                if load:
                    con['wait'] = pickle.load(open(path, 'rb'))
                if save:
                    pickle.dump(con['wait'], open(path, 'wb'))
        else:
            os.mkdir(folder[:-1])
            for con in self.conditions:
                path = folder + con['type'] + '.pkl'
                pickle.dump(con['wait'], open(path, 'wb'))

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