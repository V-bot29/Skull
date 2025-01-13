# Game
from Player import Player
import numpy as np
import matplotlib.pyplot as plt
import pprint
import copy
import pprint as pp

class Game:
    def __init__(self, player_amount = 0, game_bots = []):
        self.player_amount = player_amount
        self.bot_amount = len(game_bots)

        self.gamestate = {
            "winner": None,
            "round": 0,
            "players": [],
            "player_to_act": None,
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

        self.game_bots = game_bots

        # Setup Players and Bots
        for i in range(1, self.player_amount + 1):
            self.gamestate["players"].append(Player(i))
        for j in range(self.player_amount+1, self.player_amount + self.bot_amount + 1):
            new_player = Player(j, is_bot = True)
            self.gamestate["players"].append(new_player)

            # Bot takes control of player
            self.game_bots[j - self.player_amount - 1].player = new_player
           

        self.gamestate["player_to_act"] = self.gamestate["players"][0]  # Who goes first

        print("Game initialized")
        
    def start_new_game(self):

        for player in self.gamestate["players"]:
            player.total_reset()

        self.gamestate["player_to_act"] = np.random.choice(self.gamestate["players"])  # Who goes first
        print (f"Starting new game with {len(self.gamestate["players"])} players")
        self.game_loop()

        return self.gamestate["winner"]

    def game_loop(self):
        self.gamestate["game_over"] = False
        while not self.gamestate["game_over"]:
            self.gamestate["round"] += 1
            print(f"Round {self.gamestate["round"]}")

            self.round_loop()
            # reset players
            for player in self.gamestate["players"]:
                player.reset()

            if self.gamestate["player_to_act"].deck.cards == []:
                    self.gamestate["players"].remove(self.gamestate["player_to_act"])


            self.gamestate["game_over"] = self.check_game_over()

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

        self.gamestate["round_over"] = False
        while not self.gamestate["round_over"]:
            for i in range(first, last):
                name = i % len(self.gamestate["players"])
                self.gamestate["player_to_act"] = self.gamestate["players"][name]

                pass_count = 0
                for player in self.gamestate["players"]:
                    if player.pass_bool:
                        pass_count += 1
            
                if pass_count == len(self.gamestate["players"]) - 1:             
                    self.gamestate["flip_win"] = self.flip_loop()
                    
                    if self.gamestate["flip_win"]:
                        self.gamestate["player_to_act"].win_round()
                        print(f'{self.gamestate["player_to_act"].name} won the round')
                    else:
                        self.gamestate["player_to_act"].lose_round()
                        print(f'{self.gamestate["player_to_act"].name} lost the round')

                    self.gamestate["round_over"] = True
                    break
                else: 
                    self.turn_loop()
    
    def flip_loop(self):
        print('Flipping cards')
        
        # Determine player who has not passed
        for player in self.gamestate["players"]:
            if not player.pass_bool:
                self.gamestate["player_to_act"] = player

        
        self.gamestate["flowers_flipped"] = 0
        self.gamestate["skulls_flipped"] = 0
        self.gamestate["flipping_phase"] = True
        self.gamestate["carding_phase"] = False
        self.gamestate["betting_phase"] = False
        self.gamestate["cards_flipped"] = 0
        
        # flip own cards
        #self.gamestate["player_to_act"].stack.reverse() # take the topmost card
        for card in self.gamestate["player_to_act"].stack:
            print(f'{self.gamestate["player_to_act"].name} own card flipped')
            if card.suit == 'flower':
                self.gamestate["flowers_flipped"] += 1
                print(f'{self.gamestate["player_to_act"].name} flipped a flower')
            elif card.suit == 'skull':
                self.gamestate["skulls_flipped"] += 1
                print(f'{self.gamestate["player_to_act"].name} flipped a skull')
                return False

            self.gamestate["cards_flipped"] += 1

            if self.gamestate["flowers_flipped"] == self.gamestate["player_to_act"].betsize:
                return True

        # flip other players cards
        while self.gamestate["cards_flipped"] < self.gamestate["player_to_act"].betsize:

            if self.gamestate["player_to_act"].is_bot:
                action_type, action_value = self.bot_action()
                action_type, player_id = action_type.split()
            else:
                action = input("Enter action for {}: ".format(self.gamestate["player_to_act"].name))
                if action == "gamestate":
                    pprint.pprint(self.gamestate)
                    continue
                if action == "status":
                    print(self.gamestate["player_to_act"])
                    continue
                if action == "moves":
                    pprint.pprint(self.get_moves())
                    continue

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
                                    self.gamestate["flowers_flipped"] += 1
                                    print(f'{self.gamestate["player_to_act"].name} flipped a flower')
                                elif card.suit == 'skull':
                                    self.gamestate["skulls_flipped"] += 1
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
     
      
        if action == "status":
            print(player)
            return False
        
        if action == "gamestate":
            pprint.pprint(self.gamestate)
            return False
        
        if action == "moves":
            pprint.pprint(self.get_moves(self.gamestate))
            return False

        if action == "pass" or action == "pass None":
            if self.gamestate["betting_phase"]:
                player.pass_betting()
                print(f'{player.name} passed')
                return True
            
        if action != "pass":
            action_type, action_value = action.split()

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
                self.gamestate["winner"] = player
                print (f"Player {player.name} wins the game")
                return True
            if player.hand == []:
                out_of_cards_count += 1

        if out_of_cards_count == len(self.gamestate["players"]) - 1:
            for player in self.gamestate["players"]:
                if player.hand != []:
                    self.gamestate["winner"] = player
                    print(f"Player {player.name} wins the game")
            return True

        if self.gamestate["players"] == []:
            print("Draw")
            self.gamestate["winner"] = None
            return True   
            
        return False
    
    def bot_action(self):  
        # decide on bot to call
        for bot in self.game_bots:
            if bot.player == self.gamestate["player_to_act"]:
                moves = self.get_moves(self.gamestate)
                action_type, action_value = bot.random_move(moves)
                                            # TODO change this to actual move
        return action_type, action_value

    def get_moves(self, gamestate = None):
        moves = []

        if gamestate is None:
            gamestate = self.gamestate

        player = gamestate["player_to_act"]

        if gamestate["flipping_phase"]:
            for p in gamestate["players"]:
                if len(p.deck.cards) == 0:
                    continue
                if p.name == player.name:
                    continue

                flip_values = np.arange(1, len(p.stack) + 1)  # check here for flip issues
                for value in flip_values:
                    moves.append((f'flip {p.name}', value))

        else:
            if len(player.hand) == 0 and gamestate["carding_phase"]:
                bet_values = np.arange(gamestate['highest_bet'] + 1, gamestate["cards_played"] + 1)
                for value in bet_values:
                    moves.append(("bet", value))

            elif gamestate["cards_played"] < len(gamestate["players"]):
                play_values = [player.hand[i].suit for i in range(len(player.hand))]
                for value in play_values:
                    moves.append(("play", value))

            elif gamestate["betting_phase"] and (gamestate['highest_bet'] < gamestate["cards_played"]):
                bet_values = np.arange(gamestate["highest_bet"] + 1, gamestate["cards_played"] + 1)
                for value in bet_values:
                    moves.append(("bet", value))
                moves.append(("pass", None))

            elif gamestate["betting_phase"] and (gamestate['highest_bet'] == gamestate["cards_played"]):
                moves.append(("pass", None))

            else:
                play_values = [player.hand[i].suit for i in range(len(player.hand))]
                for value in play_values:
                    moves.append(("play", value))
                bet_values = np.arange(1, gamestate["cards_played"])
                for value in bet_values:
                    moves.append(("bet", value))


        #print(f"Available moves: {moves} for player {player.name}")
        return moves

class SimGame(Game):
    def __init__(self, input_gamestate):
        self.original_gamestate = input_gamestate.copy()
        self.gamestate = input_gamestate.copy()
        self.gamestate_history = [self.original_gamestate.copy()]
        self.player_to_act = self.gamestate["player_to_act"]
        self.next_player_name = self.gamestate["player_to_act"].name

    def do_move(self, move):
        action_type, action_value = move
        # Change Gamestate
        #print(f'Player {self.gamestate["player_to_act"].name} Action: {action_type} {action_value}')
        # GAME LOOP
        if not self.gamestate["game_over"]:

            # ROUND LOOP
            if not self.gamestate["round_over"]:
                self.next_player_name = (self.gamestate["player_to_act"].name) % (len(self.gamestate["players"])) + 1

                pass_count = 0
                for player in self.gamestate["players"]:
                    if player.pass_bool:
                        pass_count += 1
            
                if pass_count == len(self.gamestate["players"]) - 1:             
                    # FLIP LOOP
                    self.next_player_name = self.gamestate["player_to_act"].name

                    for card in self.gamestate["player_to_act"].stack:
                        if card.suit == 'flower' and not card.flipped:
                            self.gamestate["flowers_flipped"] += 1
                            self.gamestate["cards_flipped"] += 1
                            card.flipped = True
                        elif card.suit == 'skull' and not card.flipped:
                            self.gamestate["skulls_flipped"] += 1
                            self.gamestate["cards_flipped"] += 1
                            card.flipped = True
                            self.gamestate["flip_win"] = False
                            break
                    
                            


                    # flip other players cards
                    if self.gamestate["cards_flipped"] < self.gamestate["player_to_act"].betsize:
                        action_type, player_id = action_type.split()

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
                                                self.gamestate["flowers_flipped"] += 1
                                            elif card.suit == 'skull':
                                                self.gamestate["skulls_flipped"] += 1
                                                self.gamestate["flip_win"] = False
                                                break
                                            
                                            card.flipped = True
                                            self.gamestate["cards_flipped"] += 1

                    if self.gamestate["flowers_flipped"] == self.gamestate["player_to_act"].betsize:
                            self.gamestate["flip_win"] = True

                    if self.gamestate["flip_win"] == True:
                        self.gamestate["player_to_act"].win_round()
                        print(f'{self.gamestate["player_to_act"].name} won the round')
                        self.gamestate["round_over"] = True
                    elif self.gamestate["flip_win"] == False:
                        self.gamestate["player_to_act"].lose_round()
                        print(f'{self.gamestate["player_to_act"].name} lost the round')
                        self.gamestate["round_over"] = True
                    
                else: 
                    # TURN LOOP
                    if action_type == "pass":
                        if self.gamestate["betting_phase"]:
                            self.gamestate["player_to_act"].pass_betting()
                        
                    if (action_type == "play") and self.gamestate["carding_phase"]:
                        suit = action_value

                        for card in self.gamestate["player_to_act"].hand:
                            if card.suit == suit:
                                self.gamestate["player_to_act"].play_card(card)
                                self.gamestate["cards_played"] += 1
                                break
                               

                    if action_type == "bet":
                        if self.gamestate["cards_played"] >= len(self.gamestate["players"]):    
                            betsize = int(action_value)
                            if self.gamestate["highest_bet"] < betsize <= self.gamestate["cards_played"]:
                                self.gamestate["player_to_act"].bet(betsize)
                                self.gamestate["carding_phase"] = False
                                self.gamestate["betting_phase"] = True
                                self.gamestate["highest_bet"] = betsize
                              



            if self.gamestate["round_over"]:
                
                self.gamestate["flip_win"] = None
                self.gamestate["flowers_flipped"] = 0
                self.gamestate["skulls_flipped"] = 0
                self.gamestate["flipping_phase"] = True
                self.gamestate["carding_phase"] = False
                self.gamestate["betting_phase"] = False
                self.gamestate["cards_flipped"] = 0

                self.gamestate["round_over"] = False
                self.gamestate["carding_phase"] = True
                self.gamestate["betting_phase"] = False
                self.gamestate["flipping_phase"] = False
                self.gamestate["highest_bet"] = 0
                self.gamestate["cards_played"] = 0



                for player in self.gamestate["players"]:
                    player.reset()

                if self.gamestate["player_to_act"].deck.cards == []:
                        self.gamestate["players"].remove(self.gamestate["player_to_act"])

                # CHECK GAME OVER
                out_of_cards_count = 0
        
                for player in self.gamestate["players"]:
                    if player.score == 2:
                        self.gamestate["winner"] = player
                        
                    if player.hand == []:
                        out_of_cards_count += 1

                if out_of_cards_count == len(self.gamestate["players"]) - 1:
                    for player in self.gamestate["players"]:
                        if player.hand != []:
                            self.gamestate["winner"] = player
                            print(f"Player {player.name} wins the game")
                   

                if self.gamestate["players"] == []:
                    self.gamestate["winner"] = False # DRAW
            

        #print(f'next player: {next_player_name}')
        for player in self.gamestate["players"]:
            if player.name == self.next_player_name:
                self.gamestate["player_to_act"] = player

        self.gamestate_history.append(copy.deepcopy(self.gamestate))
        return self.gamestate

    def undo_move(self):
        self.gamestate_history.pop()
        self.gamestate = self.gamestate_history[-1].copy()
        return self.gamestate

    def reset(self):
        self.gamestate = self.original_gamestate.copy()
        self.gamestate_history = [self.gamestate.copy()]
        return self.gamestate
    
    def is_terminal(self):
        return self.gamestate["game_over"]


if __name__ == "__main__":
    game = Game(player_amount=2)

    winner = game.start_new_game()
    print(winner)