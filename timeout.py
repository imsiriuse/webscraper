from random import randint


class Timeout:
    def __init__(self, max=0, min=0, step=0):
        self.max = max
        self.min = min
        self.step = step

    def getrandom(self):
        if max == 0:
            return 0
        return randint(self.min * 1000, self.max * 1000) / 1000
