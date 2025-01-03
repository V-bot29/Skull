# Game

import Player

class Game:
    def __init__(self, player_amount = 3, settings = None):
        # TODO implement settings

        self.player_amount = player_amount

        
        self.winner = None


    def start_new_game(self):
        
        self.round = 0
        self.players = []

        for i in range(1, self.player_amount+1):
            self.players.append(Player.Player("Player " + str(i)))

        self.player_to_act = self.players[0] # Who goes first

    
            
    
    
    
