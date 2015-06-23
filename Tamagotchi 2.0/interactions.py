from constants import *

class Interaction:
    def __init__(self, interaction, wait_time, health, happiness, action_time):
        self.interaction = interaction
        self.wait_time = wait_time
        self.health = health
        self.happiness = happiness
        self.action_time = action_time



INTERACTIONS = {
    'Cheeseburger': Interaction('Cheeseburger', 3 * HOURS, -1, 1, 45),
    'Salad': Interaction('Salad', 90 * MINUTES, 1, -1, 20),
    'Pizza': Interaction('Pizza', 4 * HOURS, -2, 2, 30),
    'Celery': Interaction('Celery', 30 * MINUTES, 2, -2, 10),
    'Water': Interaction('Water', 2 * HOURS, 0, 0, 10),
    'Soda': Interaction('Soda', 2 * HOURS, -1, 1, 10),
    'Coffee': Interaction('Coffee', 90 * MINUTES, 0, 1, 10),
    'Beer': Interaction('Beer', 30 * MINUTES, -1, 2, 10),
    'Hug': Interaction('Hug', 2 * HOURS, 0, 3, 30),
    'Pet': Interaction('Pet', 30 * MINUTES, 0, 1, 10),
    'Basketball': Interaction('Basketball', 4 * HOURS, 3, 3, 120),
    'Frisbee': Interaction('Frisbee', 3 * HOURS, 2, 4, 60),
    'Watch TV': Interaction('Watch TV', 1 * HOURS, -1, 3, 60),
    'Long Sleep': Interaction('Long Sleep', 12 * HOURS, 6, 6, 2 * HOURS),
    'Nap': Interaction('Nap', 4 * HOURS, 0, 3, 30 * MINUTES),
}

INTERACTION_TYPES = {
    'Eat':['Cheeseburger', 'Salad', 'Pizza', 'Celery'],
    'Drink':['Water', 'Soda', 'Coffee', 'Beer'],
    'Love':['Hug', 'Pet'],
    'Play':['Basketball', 'Frisbee','Watch TV'],
    'Sleep':['Long Sleep', 'Nap']
}

if __name__=='__main__':
    print(INTERACTIONS['Drink'].interactions)