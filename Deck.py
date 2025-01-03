# Deck
from Card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self, skull_cards = 1, flower_cards = 3):
        for i in range(1,skull_cards+1):
            id = "s" + str(i)
            skull = Card("skull", id)
            self.cards.append(skull)

        for i in range(1,flower_cards+1):
            id = "f" + str(i)
            flower = Card("flower", id)
            self.cards.append(flower)

    def __repr__(self):
        return str(self.cards)
            
