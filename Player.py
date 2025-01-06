# Player

from Deck import Deck
import random

class Player:
    def __init__(self, name, is_bot = False):
        self.name = name
        self.is_bot = is_bot
        self.hand = []
        
        self.stack = []
        self.deck = Deck()
        self.hand = self.deck.cards.copy()

        self.bet_bool = False
        self.pass_bool = False
        self.betsize = 0

        self.score = 0

    def play_card(self, card):
        self.hand.remove(card)
        self.stack.append(card)

    def bet(self, betsize):
        self.bet_bool = True
        self.betsize = betsize

    def reset(self):
        self.hand = self.deck.cards.copy()
        for card in self.hand:  
            card.flipped = False
        self.stack = []
        self.bet_bool = False
        self.pass_bool = False
        self.betsize = 0

    def win_round(self):
        self.score += 1

    def lose_round(self):
        # remove a random card
        card = random.choice(self.deck.cards)
        self.deck.cards.remove(card)

    def pass_betting(self):
        self.bet_bool = False
        self.pass_bool = True
    
    def __repr__(self):
        hand_list = ', '.join([str(card.suit) for card in self.hand])
        stack_list = ', '.join([str(card.suit) for card in self.stack])

        return (f"Name: {self.name}\n"
                f"Deck: {self.deck}\n"
                f"Hand: {hand_list}\n"
                f"Stack: {stack_list}\n"
                f"Bet Bool: {self.bet_bool}\n"
                f"Pass Bool: {self.pass_bool}\n"
                f"Bet Size: {self.betsize}\n"
                f"Score: {self.score}")

    

if __name__ == "__main__":
    player = Player(1)
    print(player)
    player.lose_round()
    print("lost_card",player)
    player.reset()
    print("reset" ,player)
    player.play_card(player.hand[0])
    print("played_card ",player)
