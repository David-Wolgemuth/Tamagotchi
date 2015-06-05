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

        self.hungry = {'att':False, 'wait':3 * HOURS, 'file':'hungry.pkl', 'type':'Eat', 'timestring':None}
        self.tired = {'att':False, 'wait':6 * HOURS, 'file':'tired.pkl', 'type':'Sleep', 'timestring':None}
        self.bored = {'att':False, 'wait':3 * HOURS, 'file':'bored.pkl', 'type':'Play', 'timestring':None}
        self.lonely = {'att':False, 'wait':1 * HOURS, 'file':'lonely.pkl', 'type':'Love', 'timestring':None}
        self.thirsty = {'att':False, 'wait':45 * MINUTES, 'file':'thirsty.pkl', 'type':'Drink', 'timestring': None}

        self.interactions = {
            # Action, Time, Health, Happiness
            'Eat':[['Cheeseburger', 3 * HOURS, -1, 1],
                    ['Salad', 90 * MINUTES, 1, -1],
                    ['Pizza', int(3.5 * HOURS), -2, 2],
                    ['Celery', 1 * HOURS, 2, -2]
                    ],
            'Drink':[['Water', 2 * HOURS, 0, 0],
                      ['Soda', 1 * HOURS, -1, 1],
                      ['Coffee', 90 * MINUTES, 0, 1],
                      ['Beer', 30 * MINUTES, -1, 2]
                    ],
            'Love':[['Hug', 2 * HOURS, 0, 3],
                       ['Pet', 30 * MINUTES, 0, 1],
                       ],
            'Play':[['Basketball', 4 * HOURS, 3, 3],
                    ['Frisbee', 3 * HOURS, 2, 4],
                    ['Watch TV', 1 * HOURS, -1, 3]
                    ],
            'Sleep':[['Sleep', 12 * HOURS, 2, 2],
                     ['Nap', 4 * HOURS, 0, 3]]

        }

        # Wellness
        self.health = None
        self.happiness = None

        self.conditions = [self.hungry, self.tired,
                           self.bored, self.lonely,
                           self.thirsty]

    def interact(self, in_condition, interaction):

        for cond in self.conditions:
            if cond['type'] == in_condition:
                condition = cond

        now = int(time.time())
        old = pickle.load(open(self.folder + condition['file'], 'rb'))

        if now - old > condition['wait']:
            for action in condition['type']:
                if action == interaction:
                    condition['wait'] = action[1]
                    self.health += action[2]
                    self.happiness += action[3]
            pickle.dump(now, open(self.folder + condition['file'], 'wb'))
            return True
        else:
            return False

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
                pickle.dump(0, open(self.folder + con['file'], 'wb'))

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