# Game
from Player import Player
import bots
import numpy as np
import matplotlib.pyplot as plt


class Game:
    def __init__(self, player_amount = 0, bot_amount = 3):
        self.player_amount = player_amount
        self.bot_amount = bot_amount

        self.gamestate = {
            "winner": None,
            "round": 0,
            "players": [],
            "player_to_act": None,
            "cards_played": 0,
            "cards_flipped": 0,
            "highest_bet": 0,
            "carding_phase": True,
            "betting_phase": False,
            "flipping_phase": False
        }

        # Initialize bots
        self.game_bots = []
        for i in range(bot_amount):
            bot = bots.Bot(name = f"Bot {i+1}")
            self.game_bots.append(bot)

        

        print("Game initialized")
        
    def start_new_game(self):

        self.winner = None
        self.round = 0
        self.gamestate["players"] = []

        for i in range(1, self.player_amount + 1):
            self.gamestate["players"].append(Player(i))
        for j in range(self.player_amount+1, self.player_amount + self.bot_amount + 1):
            new_player = Player(j, is_bot = True)
            self.gamestate["players"].append(new_player)

            # Bot takes control of player
            self.game_bots[j - self.player_amount - 1].player = new_player
           


        self.gamestate["player_to_act"] = self.gamestate["players"][0]  # Who goes first
        print (f"Starting new game with {len(self.gamestate["players"])} players")
        self.game_loop()

        return self.winner

    def game_loop(self):
        game_over = False

        while not game_over:
            self.round += 1
            print(f"Round {self.round}")

            self.round_loop()
            # reset players
            for player in self.gamestate["players"]:
                player.reset()

            if self.gamestate["player_to_act"].deck.cards == []:
                    self.gamestate["players"].remove(self.gamestate["player_to_act"])


            game_over = self.check_game_over()

        print("Game Over")

    def round_loop(self):
        # start with player to act and then loop through the rest
    
       
        self.gamestate["carding_phase"] = True
        self.gamestate["betting_phase"] = False
        self.gamestate["flipping_phase"] = False
        self.gamestate["highest_bet"] = 0
        self.gamestate["cards_played"] = 0
        

        first = self.gamestate["player_to_act"].name - 1
        last = self.gamestate["player_to_act"].name + len(self.gamestate["players"]) - 1

        round_over = False
        while not round_over:
            for i in range(first, last):
                name = i % len(self.gamestate["players"])
                self.gamestate["player_to_act"] = self.gamestate["players"][name]

                pass_count = 0
                for player in self.gamestate["players"]:
                    if player.pass_bool:
                        pass_count += 1
            
                if pass_count == len(self.gamestate["players"]) - 1:             
                    winner = self.flip_loop()
                    
                    if winner:
                        self.gamestate["player_to_act"].win_round()
                        print(f'{self.gamestate["player_to_act"].name} won the round')
                    else:
                        self.gamestate["player_to_act"].lose_round()
                        print(f'{self.gamestate["player_to_act"].name} lost the round')

                    round_over = True
                    break
                else: 
                    self.turn_loop()
    
    def flip_loop(self):
        print('Flipping cards')
        
        # Determine player who has not passed
        for player in self.gamestate["players"]:
            if not player.pass_bool:
                self.gamestate["player_to_act"] = player

        
        flowers = 0
        skulls = 0
        self.gamestate["flipping_phase"] = True
        self.gamestate["carding_phase"] = False
        self.gamestate["betting_phase"] = False
        self.gamestate["cards_flipped"] = 0
        
        # flip own cards
        #self.gamestate["player_to_act"].stack.reverse() # take the topmost card
        for card in self.gamestate["player_to_act"].stack:
            print(f'{self.gamestate["player_to_act"].name} own card flipped')
            if card.suit == 'flower':
                flowers += 1
                print(f'{self.gamestate["player_to_act"].name} flipped a flower')
            elif card.suit == 'skull':
                skulls += 1
                print(f'{self.gamestate["player_to_act"].name} flipped a skull')
                return False

            self.gamestate["cards_flipped"] += 1

            if flowers == self.gamestate["player_to_act"].betsize:
                return True

        # flip other players cards
        while self.gamestate["cards_flipped"] < self.gamestate["player_to_act"].betsize:

            if self.gamestate["player_to_act"].is_bot:
                action_type, action_value = self.bot_action()
                action_type, player_id = action_type.split()
            else:
                action = input("Enter action for {}: ".format(self.gamestate["player_to_act"].name))            
                action_type, player_id, action_value = action.split()

            #  TODO move to process action
            if action_type == "flip":
                player_id = int(player_id)

                for player in self.gamestate["players"]:
                    if (player.name == player_id) and (player != self.gamestate["player_to_act"]):
                        #player.stack.reverse() # take the topmost card
                        cards_this_flip = 0
                        for card in player.stack:
                            if not card.flipped and (cards_this_flip < int(action_value)):
                                cards_this_flip += 1
                                if card.suit == 'flower':
                                    flowers += 1
                                    print(f'{self.gamestate["player_to_act"].name} flipped a flower')
                                elif card.suit == 'skull':
                                    skulls += 1
                                    print(f'{self.gamestate["player_to_act"].name} flipped a skull')
                                    return False
                                
                                card.flipped = True
                                self.gamestate["cards_flipped"] += 1

        return True

    def turn_loop(self):
        player = self.gamestate["player_to_act"]
        #print(f"{player.name}'s turn")

        valid_action = False

        while not valid_action: 
            if player.is_bot:
                action_type, action_value = self.bot_action()
                valid_action = self.process_action(player, f"{action_type} {action_value}")
            else:
                action = input("Enter action for {}: ".format(player.name))
                valid_action = self.process_action(player, action)

    def process_action(self, player, action):
     
        if (action != "status") and (action != "pass"):
            action_type, action_value = action.split()

        if action == "status":
            print(player)
            return False
        
        if action == "pass" or action == "pass None":
            if self.gamestate["betting_phase"]:
                player.pass_betting()
                print(f'{player.name} passed')
                return True

        if (action_type == "play") and self.gamestate["carding_phase"]:
            suit = action_value

            for card in player.hand:
                if card.suit == suit:
                    player.play_card(card)
                    self.gamestate["cards_played"] += 1
                    print(f'{player.name} played {card}')
                    return True

        if action_type == "bet":
            if self.gamestate["cards_played"] >= len(self.gamestate["players"]):    
                betsize = int(action_value)
                if self.gamestate["highest_bet"] < betsize <= self.gamestate["cards_played"]:
                    player.bet(betsize)
                    self.gamestate["carding_phase"] = False
                    self.gamestate["betting_phase"] = True
                    self.gamestate["highest_bet"] = betsize
                    print(f'{player.name} bet {betsize}')
                    return True

        #print("Invalid action")
        return False
        
    def check_game_over(self):
        out_of_cards_count = 0
        
        for player in self.gamestate["players"]:
            if player.score == 2:
                self.winner = player
                print (f"Player {player.name} wins the game")
                return True
            if player.hand == []:
                out_of_cards_count += 1

        if out_of_cards_count == len(self.gamestate["players"]) - 1:
            for player in self.gamestate["players"]:
                if player.hand != []:
                    self.winner = player
                    print(f"Player {player.name} wins the game")
            return True

        if self.gamestate["players"] == []:
            print("Draw")
            self.winner = None
            return True   
            
        return False
    
    def bot_action(self):  
        # decide on bot to call
        for bot in self.game_bots:
            if bot.player == self.gamestate["player_to_act"]:
                action_type, action_value = bot.random_move(self.gamestate)
                                            # TODO change this to actual move
        return action_type, action_value


if __name__ == "__main__":
    game = Game(player_amount=1, bot_amount=3)
    
    #game.start_new_game()

    n_games = 1000 

    for i in range(n_games):
        winner = game.start_new_game()
        for bot in game.game_bots:
            if bot.player == winner:
                bot.wins += 1
                break

    plt.bar([bot.name for bot in game.game_bots], [bot.wins/n_games for bot in game.game_bots])
    plt.show()