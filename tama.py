import time
import os
import pickle

MINUTES = 60
HOURS = MINUTES * 60
DAYS = HOURS * 24

class Tamagotchi:
    def __init__(self):

        self.name = None
        self.animal = None
        self.folder = None

        self.hungry = {'att':False, 'wait':3 * HOURS, 'file':'hungry.pkl', 'type':'food'}
        self.tired = {'att':False, 'wait':6 * HOURS, 'file':'tired.pkl', 'type':'sleep'}
        self.bored = {'att':False, 'wait':3 * MINUTES, 'file':'bored.pkl', 'type':'play'}
        self.lonely = {'att':False, 'wait':1 * HOURS, 'file':'lonely.pkl', 'type':'comfort'}
        self.thirsty = {'att':False, 'wait':45 * MINUTES, 'file':'thirsty.pkl', 'type':'drink'}

        self.interactions = {
            # Action, Time, Health, Happiness
            'food':[['Cheeseburger', 3 * HOURS, -1, 1],
                    ['Salad', 90 * MINUTES, 1, -1],
                    ['Pizza', int(3.5 * HOURS), -2, 2],
                    ['Celery', 1 * HOURS, 2, -2]
                    ],
            'drink':[['Water', 2 * HOURS, 0, 0],
                      ['Soda', 1 * HOURS, -1, 1],
                      ['Coffee', 90 * MINUTES, 0, 1],
                      ['Beer', 30 * MINUTES, -1, 2]
                    ],
            'comfort':[['Hug', 2 * HOURS, 0, 3],
                       ['Pet', 30 * MINUTES, 0, 1],
                       ],
            'play':[['Basketball', 4 * HOURS, 3, 3],
                    ['Frisbee', 3 * HOURS, 2, 4],
                    ['Watch TV', 1 * HOURS, -1, 3]
                    ],
            'sleep':[['Sleep', 12 * HOURS, 2, 2],
                     ['Nap', 4 * HOURS, 0, 3]]

        }

        # Wellness
        self.health = 50
        self.happiness = 50

        self.conditions = [self.hungry, self.tired,
                           self.bored, self.lonely,
                           self.thirsty]

    def interact(self, condition, interaction):

        now = int(time.time())
        old = pickle.load(now, open(self.folder + condition['file'], 'rb'))

        if now - old > condition['wait']:

            for action in self.interactions[condition['type']]:
                if action == interaction:
                    condition['wait'] = action[1]
                    self.health += action[2]
                    self.happiness += action[3]

            pickle.dump(now, open(self.folder + condition['file'], 'wb'))

    def save_wait_times(self):
        pass

    def update(self):
        for con in self.conditions:
            now = int(time.time())
            if os.path.exists(self.folder + con['file']):
                old_time = pickle.load(open(self.folder + con['file'], 'rb'))
                if now - old_time > con['wait']:
                    con['att'] = True
                else:
                    con['att'] = False
            else:
                con['att'] = False
                pickle.dump(now, open(self.folder + con['file'], 'wb'))

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