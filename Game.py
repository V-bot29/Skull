# Game
import numpy as np
from Player import Player


class Game:
    def __init__(self):
        # TODO implement settings
        print("Game initialized")
        
    def start_new_game(self, player_amount = 3, bot_amount = 0):
        self.player_amount = player_amount
        self.bot_amount = bot_amount
        self.winner = None
        self.round = 0
        self.players = []

        for i in range(1, self.player_amount + 1):
            self.players.append(Player(i))

        '''
        for i in range(1, self.bot_amount + 1):
            self.players.append(Player(i + self.player_amount, is_bot = True))
        '''

        self.player_to_act = self.players[0]  # Who goes first
        print (f"Starting new game with {len(self.players)} players")
        self.game_loop()

    def game_loop(self):
        game_over = False

        while not game_over:
            self.round += 1
            print(f"Round {self.round}")

            self.round_loop()

            game_over = self.check_game_over()

        print("Game Over")

    def round_loop(self):
        # start with player to act and then loop through the rest
        global carding_phase
        global betting_phase
        global cards_played
        global round_over
        global highest_bet
        
        carding_phase = True
        betting_phase = False
        highest_bet = 0
        cards_played = 0
        round_over = False

        first = self.player_to_act.name - 1
        last = self.player_to_act.name + self.player_amount - 1

        while not round_over:
            for i in range(first, last):
                name = i % self.player_amount
                self.player_to_act = self.players[name]
                 
                pass_count = 0
                for player in self.players:
                    if player.pass_bool:
                        pass_count += 1

                if (self.player_to_act.hand != []) or self.player_to_act.pass_bool:
                    if pass_count == self.player_amount - 1:    
                        print('Entering flipping phase')          
                        winner = self.flip_loop()
                        
                        # reset players
                        for player in self.players:
                            player.reset()

                        if winner:
                            self.player_to_act.win_round()
                            print(f'{self.player_to_act.name} won the round')
                        else:
                            self.player_to_act.lose_round()
                            print(f'{self.player_to_act.name} lost the round')

                        round_over = True
                        break
                    else: 
                        self.turn_loop()
    
    def flip_loop(self):
        print('Flipping cards')
        global round_over
        global cards_flipped
        # flip own cards
        flowers = 0
        skulls = 0
        cards_flipped = 0

        for card in self.player_to_act.stack:

            if card.suit == 'flower':
                flowers += 1
                print(f'{self.player_to_act.name} flipped a flower')
            elif card.suit == 'skull':
                skulls += 1
                print(f'{self.player_to_act.name} flipped a skull')
                return False

            self.player_to_act.hand.append(card)
            self.player_to_act.stack.remove(card)
            cards_flipped += 1

            if cards_flipped == self.player_to_act.betsize:
                return True

        while cards_flipped < self.player_to_act.betsize:

            if self.player_to_act.is_bot:
                action = self.bot_action(self.player_to_act, flip_flag = True)
            else:
                action = input("Enter action for {}: ".format(self.player_to_act.name))

            try:
                action_type, player_id, action_value = action.split()

                if action_type == "flip":
                    player_id = int(player_id)

                    for player in self.players:
                        if (player.name == player_id) and (player != self.player_to_act):

                            for i in range(0, int(action_value)):
                                card = player.stack[i]
                                
                                if card.suit == 'flower':
                                    flowers += 1
                                    print(f'{self.player_to_act.name} flipped a flower')
                                elif card.suit == 'skull':
                                    skulls += 1
                                    print(f'{self.player_to_act.name} flipped a skull')
                                    return False

                                player.hand.append(card)
                                player.stack.remove(card)
                                cards_flipped += 1
            except:
                print('Invalid Input')

        return True

    def turn_loop(self):
        player = self.player_to_act
        print(f"{player.name}'s turn")

        valid_action = False

        while not valid_action: 
            if player.is_bot:
                action_type, action_value = self.bot_action(player)
                valid_action = self.process_action(player, f"{action_type} {action_value}")
            else:
                action = input("Enter action for {}: ".format(player.name))
                valid_action = self.process_action(player, action)

    def process_action(self, player, action):
        global cards_played
        global betting_phase
        global carding_phase
        global highest_bet

        if (action != "status") and (action != "pass"):
            action_type, action_value = action.split()

        if action == "status":
            print(player)
            return False
        
        if action == "pass":
            if betting_phase:
                player.pass_betting()
                print(f'{player.name} passed')
                return True

        if (action_type == "play") and carding_phase:
            suit = action_value

            for card in player.hand:
                if card.suit == suit:
                    player.play_card(card)
                    cards_played += 1
                    print(f'{player.name} played {card}')
                    return True

        if action_type == "bet":
            if cards_played >= self.player_amount:    
                betsize = int(action_value)
                if highest_bet < betsize <= cards_played:
                    player.bet(betsize)
                    carding_phase = False
                    betting_phase = True
                    highest_bet = betsize
                    print(f'{player.name} bet {betsize}')
                    return True

        print("Invalid action")
        return False
        
    def check_game_over(self):
        out_of_cards_count = 0
        
        for player in self.players:
            if player.score == 2:
                self.winner = player
                print (f"Player {player.name} wins the game")
                return True
            if player.hand == []:
                out_of_cards_count += 1

        if out_of_cards_count == self.player_amount - 1:
            for player in self.players:
                if player.hand != []:
                    self.winner = player
                    print (f"Player {player.name} wins the game")
            return True
        


        
        return False

    def bot_action(self, player, flip_flag = False):
        if flip_flag:
            action_types = {
                0: "flip"
            }
            player_ids = np.arange(1, len(self.players) + 1)
            player_ids = np.delete(player_ids, player.name - 1)
            player_id = np.random.choice(player_ids)

            global cards_flipped
            flip_amount = np.arange(1, self.betsize - cards_flipped)
            action_value = np.random.choice(flip_amount)

            return action_types[0], player_id, action_value
        
        else:
            action_types = {
                0: "play",
                1: "bet",
                2: "pass"
            }
            play_values = {player.hand[i].suit for i in range(len(player.hand))}               
            bet_values = np.arange(1, len(self.players)*4)

            action_type = np.random.choice(list(action_types.values()))
            if action_type == "play":
                action_value = np.random.choice(list(play_values))
            elif action_type == "bet":
                action_value = np.random.choice(bet_values)
            
            return action_type, action_value

if __name__ == "__main__":
    game = Game()
    game.start_new_game(player_amount=0, bot_amount=2)