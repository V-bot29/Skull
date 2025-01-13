import random
import numpy as np
from Player import Player
import numpy as np
from Game import SimGame

class Bot:
    def __init__(self, player = None, name = "Bot", search_depth = 2):
        self.player = player
        self.wins = 0
        self.name = name
        self.search_depth = search_depth

   

    def random_move(self, moves):  
        move = random.choice(list(moves))
        return move

    def get_default_weights(self, gamestate):
        weights = {
            "num_cards_played": 1,
            "highest_bet_ratio": 1,
            "distance": 1,
            "own_hand": 1,
            "own_stack": 1,
            # TODO skull in hand/stack
            "own_bet_ratio": 1,
            "own_wins": 100,
            "others": {}
        }

        for player in gamestate["players"]:
            name = player.name
            weights_other = {
                "other_stack": -1,
                "other_hand": -1,
                "other_bet_ratio": 1,
                "other_wins": -10
            }
            weights["others"][name] = weights_other
        
        return weights

    def evaluate_gamestate(self, gamestate, weights = None):
   
        if weights is None:  # TODO move to init
            weights = self.get_default_weights(gamestate)

        # Now evaluate/weigh variables
        evaluation = 0
        # general gamestate variables
        evaluation += gamestate["cards_played"] * weights["num_cards_played"]

        highest_bet_ratio = gamestate["highest_bet"] / gamestate["cards_played"]
        evaluation += highest_bet_ratio * weights["highest_bet_ratio"]

        distance = (int(self.player.name) - int(gamestate["player_to_act"].name)) % len(gamestate["players"])
        evaluation += distance * weights["distance"]

        # own variables
        evaluation += len(self.player.hand) * weights["own_hand"]
        evaluation += len(self.player.stack) * weights["own_stack"]
        evaluation += self.player.score * weights["own_wins"]
        own_bet_ratio = self.player.betsize / gamestate["cards_played"]
        evaluation += own_bet_ratio * weights["own_bet_ratio"]

        if self.player.score == 2:
            evaluation = np.inf

        # other players
        for player in gamestate["players"]:
            if player.name == self.player.name:
                continue
            name = player.name
            evaluation += len(player.stack) * weights["others"][name]["other_stack"]
            evaluation += len(player.hand) * weights["others"][name]["other_hand"]
            evaluation += player.score * weights["others"][name]["other_wins"]
            other_bet_ratio = player.betsize / gamestate["cards_played"]
            evaluation += other_bet_ratio * weights["others"][name]["other_bet_ratio"]

            if player.score == 2:
                evaluation = -np.inf

        return evaluation 

    def get_move(self, gamestate):
        simgame = SimGame(gamestate) 
        best_move, eval = self.minmax(simgame, self.search_depth)
        print(f"final eval: {eval}")
        return best_move 

    def minmax(self, simgame, max_depth, depth = 0):
        if depth == max_depth or simgame.is_terminal():
            eval = self.evaluate_gamestate(simgame.gamestate)
            return eval

        if simgame.gamestate["player_to_act"].name == self.player.name:
            maximizing_player = True
        else:
            maximizing_player = False

        if maximizing_player:
            max_eval = -np.inf
            best_move = None
            moves = simgame.get_moves()
            for move in moves:
                simgame.do_move(move)
                eval = self.minmax(simgame, max_depth, depth + 1)
                simgame.undo_move()
                if eval > max_eval:
                    print(f"new max eval: {eval} for move: {move}")
                    max_eval = eval
                    best_move = move
            if depth == 0:
                print(f"best move: {best_move}")
                print(f"max eval: {max_eval}")
                return best_move, max_eval
            return max_eval
        else:
            min_eval = np.inf
            moves = simgame.get_moves()
            for move in moves:
                simgame.do_move(move)
                eval = self.minmax(simgame, max_depth, depth + 1)
                simgame.undo_move()
                if eval < min_eval:
                    min_eval = eval
            return min_eval

class RandomBot(Bot):
    def __init__(self, player=None, name="RandomBot"):
        super().__init__(player, name)

    def get_move(self, gamestate):
        simgame = SimGame(gamestate)
        moves = simgame.get_moves()
        
        return self.random_move(moves)

class GeneticBot(Bot):
    def __init__(self, player=None, name="ManualBot"):
        super().__init__(player, name)

if __name__ == "__main__":
    player1 = Player(1)
    player2 = Player(2)
    gamestate = {
        "winner": None,
        "round": 0,
        "players": [player1, player2],
        "player_to_act": player1,
        "cards_played": 0,
        "cards_flipped": 0,
        "flowers_flipped": 0,
        "skulls_flipped": 0,
        "highest_bet": 0,
        "carding_phase": True,
        "betting_phase": False,
        "flipping_phase": False,
        "round_over": False,
        "game_over": False,
        "flip_win" : None,
    }

    """
    random_bot = RandomBot(player1)
    move = random_bot.get_move(gamestate)
    print(f"Random Bot move: {move}")
    """

    minmax_bot = Bot(player2)
    move = minmax_bot.get_move(gamestate)
    print(f"Minmax Bot move: {move}")

    '''
    # EXAMPLES
    moves_play = [('play', 'skull'), ('play', 'flower'), ('play', 'flower'), ('play', 'flower')]
    moves_bet = [('bet', 2), ('bet', 3), ('bet', 4), ('pass', None)]
    moves_flip = [('flip 2', 1), ('flip 2', 2)]
    print(bot.random_move(moves_play))
    '''
