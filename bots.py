import numpy as np
from Player import Player


class Bot:
    def __init__(self, player = None, name = "Bot"):
        self.player = player
        self.wins = 0
        self.name = name

    def get_moves(self, gamestate):
        moves = {}

        player = gamestate["player_to_act"]

        if gamestate["flipping_phase"]:

            for p in gamestate["players"]:
                if len(p.deck.cards) == 0:
                    continue
                if p.name == player.name:
                    continue

                flip_values = np.arange(1, len(p.stack) + 1) # check here for flip issues
                action_type = (f'flip {p.name}')
                moves[action_type] = flip_values
            
        else:
            if len(player.hand) == 0 and gamestate["carding_phase"]:
                action_type = "bet"
                bet_values = np.arange(gamestate['highest_bet']+1, gamestate["cards_played"] + 1)
                moves[action_type] = bet_values

            elif gamestate["cards_played"] < len(gamestate["players"]):
                action_type = "play"
                play_values = [player.hand[i].suit for i in range(len(player.hand))]  
                moves[action_type] = play_values


            elif gamestate["betting_phase"] and (gamestate['highest_bet'] < gamestate["cards_played"]):
                action_type1 = "bet"
                action_type2 = "pass"
                bet_values = np.arange(gamestate["highest_bet"]+1, gamestate["cards_played"] + 1)
                moves[action_type1] = bet_values
                moves[action_type2] = [None]
            
            elif gamestate["betting_phase"] and (gamestate['highest_bet'] == gamestate["cards_played"]):
                action_type = "pass"
                moves[action_type] = [None]

            else:
                action_type1 = "play"
                action_type2 = "bet"

                play_values = [player.hand[i].suit for i in range(len(player.hand))]               
                bet_values = np.arange(1, gamestate["cards_played"])
                moves[action_type1] = play_values
                moves[action_type2] = bet_values
     
        return moves

    def random_move(self, gamestate):
        # Decide on a move based on bot thinking

        moves = self.get_moves(gamestate)
        #print(moves)
        action_type = np.random.choice(list(moves.keys())) # chose random type
        action_value = np.random.choice(moves[action_type]) # chose random value
        #print(f'Bot chose {action_type} {action_value}')
        return action_type, action_value

if __name__ == "__main__":
    bot = Bot(1)
    player = Player(1)
    gamestate = {
        "flipping_phase": False,
        "carding_phase": True,
        "betting_phase": False,
        "cards_played": 0,
        "cards_flipped": 0,
        "player_to_act": player,
        "players": [player],
        "highest_bet": 0
    }
    print(bot.random_move(gamestate))