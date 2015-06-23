from constants import *

class Interaction:
    def __init__(self, interaction, wait_time, health,
                 happiness, action_time, text):
        self.interaction = interaction
        self.wait_time = wait_time
        self.health = health
        self.happiness = happiness
        self.action_time = action_time
        self.text = text

def get_type(interaction):
    for type in INTERACTION_TYPES:
        if interaction in INTERACTION_TYPES[type]:
            return type

INTERACTIONS = {
    'Cheeseburger': Interaction('Cheeseburger',
                3 * HOURS, -1, 1, 45, 'eating a juicy cheeseburger'),
    'Salad': Interaction('Salad',
                90 * MINUTES, 1, -1, 20, 'eating a healthy salad'),
    'Pizza': Interaction('Pizza',
                4 * HOURS, -2, 2, 30, 'eating delicious pizza'),
    'Celery': Interaction('Celery',
                30 * MINUTES, 2, -2, 10, 'eating calory-burning celery'),
    'Water': Interaction('Water',
                2 * HOURS, 0, 0, 10, 'drinking a pure glass of water'),
    'Soda': Interaction('Soda',
                2 * HOURS, -1, 1, 10, 'drinking Barq\'s Root Beer'),
    'Coffee': Interaction('Coffee',
                90 * MINUTES, 0, 1, 10, 'drinking a cup o\' Joe'),
    'Beer': Interaction('Beer',
                30 * MINUTES, -1, 2, 10, 'chugging a beer'),
    'Hug': Interaction('Hug',
                2 * HOURS, 0, 3, 30, 'softly hugging you'),
    'Pet': Interaction('Pet',
                30 * MINUTES, 0, 1, 10, 'feeling much better'),
    'Basketball': Interaction('Basketball',
                4 * HOURS, 3, 3, 120, 'playing a game of basketball'),
    'Frisbee': Interaction('Frisbee',
                3 * HOURS, 2, 4, 60, 'throwing frisbee'),
    'Watch TV': Interaction('Watch TV',
                1 * HOURS, -1, 3, 60, 'watching Adventure Time'),
    'Long Sleep': Interaction('Long Sleep',
                12 * HOURS, 6, 6, 2 * HOURS, 'snoring... zzz..'),
    'Nap': Interaction('Nap',
                4 * HOURS, 0, 3, 30 * MINUTES, 'taking a short nap'),
}

INTERACTION_TYPES = {
    EAT:['Cheeseburger', 'Salad', 'Pizza', 'Celery'],
    DRINK:['Water', 'Soda', 'Coffee', 'Beer'],
    LOVE:['Hug', 'Pet'],
    PLAY:['Basketball', 'Frisbee','Watch TV'],
    SLEEP:['Long Sleep', 'Nap']
}

if __name__=='__main__':
    for i in INTERACTION_TYPES['Love']:
        print(INTERACTIONS[i].text)
    print(int_type('Nap'))