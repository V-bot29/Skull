import bots
import Game
import matplotlib.pyplot as plt

if __name__ == "__main__":

    
    # Initialize bots
    bot1 = bots.RandomBot(name = "RandomBot")
    bot2 = bots.TreeSearchBot(name = "TreeSearchBot")
    #bot2 = bots.RandomBot(name = "RandomBot")
    game_bots = [bot1, bot2]

    game = Game.Game(player_amount=0, game_bots = game_bots)


    n = 10


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