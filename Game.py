# Game

from Player import Player

class Game:
    def __init__(self):
        # TODO implement settings
        print("Game initialized")
        
    def start_new_game(self, player_amount = 3):
        self.player_amount = player_amount
        self.winner = None
        self.round = 0
        self.players = []

        for i in range(1, self.player_amount + 1):
            self.players.append(Player(i))

        self.player_to_act = self.players[-1]  # Who goes first
        print (f"Starting new game with {self.player_amount} players")
        self.game_loop()

    def game_loop(self):
        game_over = False

        while not game_over:
            self.round += 1
            print(f"Round {self.round}")

            self.round_loop()

            if self.check_game_over():
                game_over = True

        print("Game Over")

    def round_loop(self):
        # start with player to act and then loop through the rest
        carding_phase = True
        betting_phase = False
        cards_played = 0
        round_over = False

        first = self.player_to_act.name
        last = self.player_to_act.name + self.player_amount

        while not round_over:
            for i in range(first, last):
                name = i % self.player_amount
                self.player_to_act = self.players[name]
                if (self.player_to_act.hand != []) or self.player_to_act.pass_bool:
                    self.turn_loop()

    def turn_loop(self):
        player = self.player_to_act
        print(f"{player.name}'s turn")

        valid_action = False

        while not valid_action: 
            action = input("Enter action for {}: ".format(player.name))
            valid_action = self.process_action(player, action)

    def process_action(self, player, action):
        # Implement the logic to process the player's action
        print(f"Processing action '{action}' for {player.name}")
        action_type, action_value = action.split()

        if action_type == "status":
            print(player)
            return False

        if action_type == "play":
            suit = action_value

            for card in player.hand:
                if card.suit == suit:
                    player.play_card(card)
                    print(f'{player.name} played {card}')
                    return True

        if action_type == "bet":
            global cards_played
            global betting_phase
            global carding_phase

            if cards_played >= self.player_amount:    
                betsize = int(action_value)
                if betsize <= cards_played:
                    player.bet(betsize)
                    print(f'{player.name} bet {betsize}')
                    return True

        if action_type == "pass":
            global betting_phase
            if betting_phase:
                player.pass_betting()
                print(f'{player.name} passed')
                return True

        return False
        
        
        

    def check_game_over(self):
        # Implement the logic to check if the game is over
        # Return True if the game is over, otherwise False
        return False


if __name__ == "__main__":
    game = Game()
    game.start_new_game(2)