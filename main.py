import bots
import Game
import matplotlib.pyplot as plt

if __name__ == "__main__":

    
    # Initialize bots
    bot1 = bots.RandomBot(name = "RandomBot1")
    bot2 = bots.RandomBot(name = "RandomBot2")
    bot3 = bots.TreeSearchBot(name = "TreeSearchBot", search_depth=1)
    #bot2 = bots.RandomBot(name = "RandomBot")
    game_bots = [bot1, bot2, bot3]

    game = Game.Game(player_amount=0, game_bots = game_bots)


    n = 100


    for i in range(n):
        winner = game.start_new_game()
        for bot in game_bots:
            if bot.player.name == winner.name:
                bot.wins += 1

    # Plot results
    names = [bot.name for bot in game_bots]
    wins = [bot.wins for bot in game_bots]

    plt.bar(names, wins)
    plt.show()