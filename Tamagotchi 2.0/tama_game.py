
class Tama_Game:
    def __init__(self):
        self.saves = []
        self.find_saves()
        self.pet = None

    def find_saves(self):
        if os.path.isdir('saves'):
            for folder in os.listdir('saves'):
                if os.isdir('saves/' + folder):
                    self.saves.append(folder)
