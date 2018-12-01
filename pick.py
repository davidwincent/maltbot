from random import randint


class Pick:
    """
    class Pick picks a pseudo random value without repeating itself more than
    `max_repeat`
    """

    def __init__(self, values, max_repeat=3):
        if max_repeat > len(values):
            raise ValueError("max_repeat > len(values)")
        self.values = values
        self.max_repeat = max_repeat
        self.repeat = []

    def one(self):
        """pick one of self.values"""
        while True:
            value = self.values[randint(0, len(self.values) - 1)]
            if value in self.repeat:
                continue
            self.repeat = self.repeat[- self.max_repeat + 1 or None:] + [value]
            return value
