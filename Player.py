# Player

from Deck import Deck

class Player:
    def __init__(self, name, symbol = None):
        self.name = name
        self.symbol = symbol
        self.hand = []
        
        self.stack = []
        self.deck = Deck()
        self.hand = self.deck.cards

        self.bet_bool = False
        self.betsize = 0

        self.score = 0

    def play_card(self, card):
        self.hand.remove(card)
        self.stack.append(card)

    def bet(self, betsize):
        self.bet_bool = True
        self.betsize = betsize

    def reset(self):
        self.hand += self.stack
        self.stack = []
        self.bet_bool = False
        self.betsize = 0

    def win_round(self):
        self.score += 1

    def pass_turn(self):
        pass
    
    def __repr__(self):
        hand_list = ', '.join([str(card.suit) for card in self.hand])
        stack_list = ', '.join([str(card.suit) for card in self.stack])

        return (f"Name: {self.name}\n"
                f"Hand: {hand_list}\n"
                f"Stack: {stack_list}\n"
                f"Bet Bool: {self.bet_bool}\n"
                f"Bet Size: {self.betsize}\n"
                f"Score: {self.score}")

    

if __name__ == "__main__":
    player = Player("Player 1")
    print(player)
    player.bet(2)
    card = player.hand[0]
    player.win_round()
    player.play_card(card)
    print(player)
