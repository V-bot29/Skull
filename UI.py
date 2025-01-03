# UI
from tkinter import *
from tkinter import ttk
from Game import Game

class UI:
    def __init__(self):
        self.game = None

        self.create_menu(root)
        self.create_game_panedwindow(root)

        self.show_menu()

    
    def create_log(self, parent):
        self.log = LabelFrame(parent, text="Log", name = "log")

        self.log_text = Text(self.log)
        self.log_text.pack(fill="both", expand="yes")
    def log_message(self, message):
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)

    def create_game_panedwindow(self, parent):
        self.game_panedwindow = PanedWindow(parent, orient=VERTICAL)
        self.game_panedwindow.pack(fill="both", expand="yes")

        self.create_game_frame(self.game_panedwindow)
        self.create_log(self.game_panedwindow)

        self.game_frame.pack(fill="both", expand="yes")

        self.game_panedwindow.add(self.game_frame)
        self.game_panedwindow.add(self.log)
    def create_menu(self, parent):
        self.menu = LabelFrame(parent, text="Menu", name = "menu")
        self.menu.pack(fill="both", expand="yes")

        self.player_amount = IntVar()
        self.player_amount.set(3)
        self.player_amount_label = Label(self.menu, text="Player amount")
        self.player_amount_label.pack()
        self.player_amount_entry = Entry(self.menu, textvariable=self.player_amount)
        self.player_amount_entry.pack()

        self.start_button = Button(self.menu, text="Start", command=self.create_game)
        self.start_button.pack()
    def create_game_frame(self, parent):
        self.game_frame = LabelFrame(parent, text="Game", name = "game")

        self.back_button = Button(self.game_frame, text="Back", command=self.show_menu)
        self.back_button.pack()

    def create_player_frame(self, parent, player):
        player_frame = LabelFrame(parent, text=player.name, name = "player_frame"+ player.name)

        hand_frame = self.create_hand_frame(player_frame, player.hand)
        hand_frame.pack(side="top")

        stack_frame = self.create_stack_frame(player_frame, player.stack)
        stack_frame.pack(side="top")

        play_card_frame = self.create_play_card_frame(player_frame, player)
        play_card_frame.pack(side="top")

        bet_frame = self.create_bet_frame(player_frame, player)
        bet_frame.pack(side="top")
        
        self.log_message(player.name + " joined the game")
        
        return player_frame

    def create_card_frame(self, parent, card):
        card_frame = LabelFrame(parent, text=card.suit, name = "card_frame"+ card.id)
        card_label = Label(card_frame, text=card.id)
        card_label.pack()
        return card_frame
    
    def create_hand_frame(self, parent, hand):
        hand_frame = LabelFrame(parent, text="Hand", name = "hand_frame")
        for card in hand:
            card_frame = self.create_card_frame(hand_frame, card)
            card_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5)
            root.after(100)
        return hand_frame

    def create_stack_frame(self, parent, stack):
        stack_frame = LabelFrame(parent, text="Stack", name = "stack_frame")
        for card in stack:
            card_frame = self.create_card_frame(stack_frame, card)
            card_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5)
            root.after(100)
        return stack_frame

    def create_play_card_frame(self, parent, player):
        play_card_frame = LabelFrame(parent, text="Play Card", name="play_card_frame")
        play_card_label = Label(play_card_frame, text="Play Card: ")
        play_card_label.pack()

        # Create a dictionary to map card types to card objects
        card_map = {card.suit: card for card in player.hand}

        # Populate the dropdown with card types
        play_card_dropdown = ttk.Combobox(play_card_frame, values=list(card_map.keys()))
        play_card_dropdown.pack()

        def play_card():
            selected_suit = play_card_dropdown.get()
            selected_card = card_map.get(selected_suit)
            if selected_card:
                self.log_message(player.name + " played " + str(selected_card))
                player.play_card(selected_card)
                self.refresh_game()


        play_card_button = Button(play_card_frame, text="Play Card", command=play_card)
        play_card_button.pack()

        

        return play_card_frame

    def create_bet_frame(self, parent, player):
        bet_frame = LabelFrame(parent, text="Bet", name = "bet_frame")
        bet_label = Label(bet_frame, text="Bet: ")
        bet_label.pack()

        bet_entry = Entry(bet_frame)
        bet_entry.pack()
        bet_entry.insert(0, str(player.betsize))

        def pass_turn():
            player.pass_turn()
            self.log_message(player.name + " passed")

            self.refresh_game()

        def bet():
            betsize = bet_entry.get()
            player.bet(betsize)

            self.log_message(player.name + " bet " + betsize)
            self.refresh_game()


        bet_button = Button(bet_frame, text="Bet", command=bet)
        bet_button.pack()

        pass_button = Button(bet_frame, text="Pass", command=pass_turn)
        pass_button.pack()

        return bet_frame


    def clear_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def update_player_frame(self, player_frame, player):
        self.clear_panel(player_frame)

        hand_frame = self.create_hand_frame(player_frame, player.hand)
        hand_frame.pack(side="top")

        stack_frame = self.create_stack_frame(player_frame, player.stack)
        stack_frame.pack(side="top")

        play_card_frame = self.create_play_card_frame(player_frame, player)
        play_card_frame.pack(side="top")

        bet_frame = self.create_bet_frame(player_frame, player)
        bet_frame.pack(side="top")

        self.log_message(player.name + " updated")

    # Example usage
    def refresh_game(self):
        for player in self.game.players:
            player_frame = self.find_player_frame(player.name)
            self.update_player_frame(player_frame, player)

    def find_player_frame(self, player_name):
        for child in self.game_frame.winfo_children():
            if child.winfo_name() == "player_frame" + player_name:
                return child
        return None




    def show_game_panedwindow(self):
        self.hide_all()
        self.game_panedwindow.pack(fill="both", expand="yes")
    def show_menu(self):
        self.hide_all()
        self.menu.pack(fill="both", expand="yes")
    def hide_all(self):
        for child in root.winfo_children():
            child.pack_forget()

    def create_game(self):
        player_amount = self.player_amount.get()
        self.show_game_panedwindow()

        self.game = Game(player_amount)
        self.game.start_new_game()

        for player in self.game.players:
            player_frame = self.create_player_frame(self.game_frame, player)
            player_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5)
            #print(player)
            

        self.log_message("Game started with " + str(player_amount) + " players")




if __name__ == "__main__":
    root = Tk()
    root.title("Skull")
    root.geometry("800x600")

    ui = UI()

    root.mainloop()
