import bots
import Game

if __name__ == "__main__":

    
    # Initialize bots
    bot_amount = 3
    game_bots = []
    for i in range(bot_amount):
        bot = bots.Bot(name = f"Bot {i+1}")
        game_bots.append(bot)

    game = Game.Game(player_amount=0, game_bots = game_bots)
