import pickle as pkl

class Tamagotchi:
    def __init__(self):

        self.name = None
        self.animal = None
        self.folder = None

        self.times[
            ['Eat', None],
            ['Drink', None],
            ['Sleep', None],
            ['Love', None],
            ['Play', None]
        ]

    def update_times(self):
        folder = self.folder + 'times/'

        if not os.path.exists(folder):
            mkdir()

        for type, time in self.times:
            path = folder + type.lower() + '.pkl'
            if not time:
                time = int(time.time())
            pkl._dump(time, open(path))