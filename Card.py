# Card

class Card:
    def __init__(self, suit, id):
        self.suit = suit
        self.id = id
        self.flipped = False

    def __repr__(self):
        return self.suit + " " + self.id