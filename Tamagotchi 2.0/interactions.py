"""The interactions and interaction types used with Tamagotchi pet"""

from constants import *


class Interaction:
    """Class for each interaction user can initiate with pet
    """
    def __init__(self, interaction, wait_time, health,
                 happiness, action_time, text):
        self.interaction = interaction
        self.wait_time = wait_time
        self.health = health
        self.happiness = happiness
        self.action_time = action_time
        self.text = text


class InteractionType:
    """Class used to hold lists of interactions and properties for
    each interaction type
    """
    def __init__(self, i_type, interactions, neglect):
        self.i_type = i_type
        self.interactions = interactions
        self.neglect_days = neglect[0]
        self.neglect_health = neglect[1]
        self.neglect_happiness = neglect[2]


def get_interaction_type(interaction):
    """Returns interaction type of input interaction
    """
    for I in INTERACTION_TYPES:
        if interaction in INTERACTION_TYPES[I].interactions:
            return I

INTERACTIONS = {
    'Cheeseburger': Interaction('Cheeseburger',
                                3 * HOURS, -1, 1, 45,
                                'eating a juicy cheeseburger'),
    'Salad': Interaction('Salad',
                         90 * MINUTES, 1, -1, 20,
                         'eating a healthy salad'),
    'Pizza': Interaction('Pizza',
                         4 * HOURS, -2, 2, 30,
                         'eating delicious pizza'),
    'Celery': Interaction('Celery',
                          30 * MINUTES, 2, -2, 10,
                          'eating calory-burning celery'),
    'Water': Interaction('Water',
                         2 * HOURS, 0, 0, 10,
                         'drinking a pure glass of water'),
    'Soda': Interaction('Soda',
                        2 * HOURS, -1, 1, 10,
                        'drinking Barq\'s Root Beer'),
    'Coffee': Interaction('Coffee',
                          90 * MINUTES, 0, 1, 10,
                          'drinking a cup o\' Joe'),
    'Beer': Interaction('Beer',
                        30 * MINUTES, -1, 2, 10,
                        'chugging a beer'),
    'Hug': Interaction('Hug',
                       2 * HOURS, 0, 3, 30, 'softly hugging you'),
    'Pet': Interaction('Pet',
                       30 * MINUTES, 0, 1, 10,
                       'feeling much better'),
    'Basketball': Interaction('Basketball',
                              4 * HOURS, 3, 3, 120,
                              'playing a game of basketball'),
    'Frisbee': Interaction('Frisbee',
                           3 * HOURS, 2, 4, 60,
                           'throwing frisbee'),
    'Watch TV': Interaction('Watch TV',
                            1 * HOURS, -1, 3, 60,
                            'watching Adventure Time'),
    'Long Sleep': Interaction('Long Sleep',
                              12 * HOURS, 6, 6, 2 * HOURS,
                              'snoring... zzz..'),
    'Nap': Interaction('Nap',
                       4 * HOURS, 0, 3, 30 * MINUTES,
                       'taking a short nap'),
    'Stop': Interaction('Stop', 0, 0, -2, 0, None)
}

INTERACTION_TYPES = {
    EAT: InteractionType(EAT,
                         ['Cheeseburger', 'Salad', 'Pizza', 'Celery'],
                         [5, 2, 1]),
    DRINK: InteractionType(DRINK, ['Water', 'Soda', 'Coffee', 'Beer'],
                           [3, 3, 0]),
    LOVE: InteractionType(LOVE, ['Hug', 'Pet'],
                          [7, 0, 10]),
    PLAY: InteractionType(PLAY, ['Basketball', 'Frisbee', 'Watch TV'],
                          [7, 2, 2]),
    SLEEP: InteractionType(SLEEP, ['Long Sleep', 'Nap'],
                           [3, 3, 0])
}

if __name__ == '__main__':
    print('\n%s:\n' % __doc__)
    print('Interaction Types:\n')
    for I in INTERACTION_TYPES:
        print(I, end='  ')
    print('\n\nInteractions:\n')
    for I in INTERACTIONS:
        print(INTERACTIONS[I].interaction, end=' ')
    print()
