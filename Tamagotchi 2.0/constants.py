"""Constants used for Tamagotchi and GUI"""

EAT = 'Eat'
DRINK = 'Drink'
SLEEP = 'Sleep'
LOVE = 'Love'
PLAY = 'Play'
HEALTH = 'Health'
HAPPINESS = 'Happiness'
MINUTES = 60
HOURS = MINUTES * 60
DAYS = HOURS * 24
HH = 'health_happiness'
TIMES = 'times'
READY = 'Ready'
PET_WINDOW = 1
INT_WINDOW = 2

if __name__ == '__main__':
    print('\n%s:\n' %__doc__)
    C = globals().copy()
    for name in C:
        if name[0] != '_':
            print('%s = %s' % (name, C[name]))