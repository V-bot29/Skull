from Game import Game
import pprint as pp
from Game import SimGame

if __name__ == "__main__":

    game = Game(bot_amount=3, player_amount=0)
    sim_game = SimGame(game.gamestate)
    
    moves = [
        ("play", "flower"),
        ("play", "flower"),
        ("play", "flower"),
        ("bet", "3"),
        ("pass", None),
        ("pass", None),
        ("flip 2", "1"),
        ("flip 3", "1"),
        ("play", "flower"),
        ("play", "flower"),
        ("play", "skull"),
        ("bet", "2"),
        ("pass", None),
        ("pass", None),
        ("flip 2", "1")
    ]

    for move in moves:
        sim_game.do_move(move)

    print(len(sim_game.gamestate["player_to_act"].deck.cards))
    pp.pprint(sim_game.gamestate["player_to_act"].score)
    sim_game.undo_move()
    #print("UNDO" + "\n" + "\n" + "\n")  
    pp.pprint(sim_game.gamestate["player_to_act"].score)
    #pp.pprint(sim_game.gamestate_history[-1])