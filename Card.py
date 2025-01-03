# Card

class Card:
    def __init__(self, suit, id):
        self.suit = suit
        self.id = id

    def __repr__(self):
        return self.suit + " " + self.id