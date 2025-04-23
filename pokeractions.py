import pygame as pg
from component import *
from handeval import HandEvaluator
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading

class PlayerActions:
    def __init__(self, game, screen, game_state):
        self.screen = screen
        self.game = game
        self.game_state = game_state

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            if self.game.leave_button.is_hovered(mouse_pos):
                pg.quit()

            if self.game_state.is_your_turn():
                if self.game.check_button.is_hovered(mouse_pos):
                    self.check_action()
                elif self.game.call_button.is_hovered(mouse_pos):
                    self.call_action()
                elif self.game.raise_button.is_hovered(mouse_pos):
                    self.raise_action()
                elif self.game.fold_button.is_hovered(mouse_pos):
                    self.fold_action()
                elif self.game.all_in_button.is_hovered(mouse_pos):
                    self.all_in_action()
                elif self.game.peek_button.is_hovered(mouse_pos):
                    self.peek_action()

    def check_action(self):
        print(f"{self.game_state.get_player_turn().name} checked.")
        self.game_state.check()

    def call_action(self):
        print(f"{self.game_state.get_player_turn().name} called.")
        self.game_state.call()
        
    def raise_action(self):
        root = tk.Tk()
        root.withdraw()

        player_chips = self.game_state.get_player_turn().chips

        amount = simpledialog.askinteger("Raise Amount", "Enter the amount to raise:", minvalue=1)

        if amount is not None:
            if amount > player_chips:
                self.show_popup("Invalid Action", "Not enough chips to raise.")
                print(f"Insufficient chips. You only have {player_chips} chips.")
            else:
                print(f"{self.game_state.get_player_turn().name} raised by {amount}.")
                self.game_state.raise_bet(amount)
        else:
            print("You didn't enter a valid raise amount.")
        
    def fold_action(self):
        print(f"{self.game_state.get_player_turn().name} folded.")
        self.game_state.fold()

    def all_in_action(self):
        all_in_amount = self.game_state.get_player_turn().chips
        print(f"{self.game_state.get_player_turn().name} went all-in with {all_in_amount} chips.")
        self.game_state.raise_bet(all_in_amount)
        
    def peek_action(self):
        print("PEEKING")

        for i, player in enumerate(self.game_state.get_all_players()):
            full_hand = self.game_state.get_community_cards() + player.hand
            e = HandEvaluator()
            evaluated_hand = e.evaluate_hand(full_hand)
            print(player)
            print("Full hand: ", full_hand)
            print("Evaluated_hand: ", evaluated_hand)
            print("----------------")
        
        winrate = HandEvaluator.calculate_winrate(self.game_state.get_all_players()[0].hand, self.game_state.get_community_cards())
        message = f"Estimated winrate: {winrate}%"
        self.show_popup_info("Winrate", message)

    def show_popup(self, title, message):
        popup_root = tk.Tk()
        popup_root.withdraw()
        popup_root.attributes("-topmost", True)

        messagebox.showerror(title, message, parent=popup_root)
        popup_root.destroy()

    def show_popup_info(self, title, message):
        popup_root = tk.Tk()
        popup_root.withdraw()
        popup_root.attributes("-topmost", True)

        messagebox.showinfo(title, message, parent=popup_root)
        popup_root.destroy()

class PlayerManager:
    def __init__(self, player, game):
        self.player = player
        self.game = game

    def take_action(self, action, amount=0):
        if action == 'check':
            self.game.check()
        elif action == 'call':
            self.game.call()
        elif action == 'fold':
            self.game.fold()
        elif action == 'raise':
            self.game.raise_bet(amount)

class BotManager:
    def __init__(self, bot, game):
        self.bot = bot
        self.game = game

    def decide_action(self):
        max_bet = max(self.game.bets.values())
        current_bet = self.game.bets[self.bot]
        chips = self.bot.chips

        actions = []
        weights = []

        if current_bet == max_bet:
            actions.append("check")
            weights.append(50)

            if chips >= 50:
                actions.append("raise")
                weights.append(20)
        else:
            call_amount = max_bet - current_bet

            if chips >= call_amount:
                actions.append("call")
                weights.append(30)

                if chips > call_amount + 50:
                    actions.append("raise")
                    weights.append(15)
            else:
                actions.append("fold")
                weights.append(40)

        # if chips > 0:
        #     actions.append("all in")
        #     weights.append(5)

        return random.choices(actions, weights=weights, k=1)[0]

    def take_action(self):

        # time.sleep(2)
        action = self.decide_action()
        print(f"Bot chooses to {action}")

        try:
            if action == 'call':
                self.game.call()
            elif action == 'fold':
                self.game.fold()
            elif action == 'check':
                self.game.check()
            elif action == 'all in':
                self.game.raise_bet(self.bot.chips)
            elif action == 'raise':
                raise_amount = min(50, self.bot.chips)
                self.game.raise_bet(raise_amount)
        except ValueError as e:
            print(f"Bot action failed: {e}")
            self.game.fold()

from data import Data

class PokerGame:
    def __init__(self, screen):
        self.screen = screen
        self.reset_in_progress = False
        self.start_game()

    def start_game(self):
        self.deck = Deck()
        self.turn = "Flop"
        self.players = [Player('Player', 975), Bot('Bot', 975)]
        self.player_turn = self.players[0]
        self.community_cards = []
        self.pot = 50
        self.bets = {player: 0 for player in self.players}
        self.bot_thinking = False
        self.showcard = False
        self.log = []

        self.player_manager = PlayerManager(self.players[0], self)
        self.bot_manager = BotManager(self.players[1], self)

        self.give_out_cards()

        self.add_log("Game Start")
        self.add_log("Game Turn: Preflop")

        self.data = Data()

    def reset_game(self):
        # Reset the deck for a new round
        self.deck = Deck()
        self.showcard = False
        self.log = []

        # Reset players
        for player in self.players:
            player.folded = False      # Marks folded = False
            player.checked = False     # Important for check logic
            player.hand = []           # Clear old hand

        active_players = [p for p in self.players if not p.folded]
        # print("players: ", [player.folded for player in self.players])

        # Reset game state
        self.turn = "Pre-Flop"
        self.player_turn = self.players[0]
        self.community_cards = []
        self.pot = 0
        self.bets = {player: 0 for player in self.players}
        self.bot_thinking = False

        # Deal new cards
        self.give_out_cards()

        self.add_log("Game Reset")
        self.add_log("Game Turn: Preflop")


    def give_out_cards(self):
        for player in self.players:
            hand = [self.deck.draw() for _ in range(2)]
            player.recieve_hand(hand)

    def draw(self):
        return self.deck.draw()

    def all_player_checked(self):
        return all(player.checked for player in self.players if not player.folded)

    def get_all_players(self):
        return self.players

    def get_log(self):
        return self.log

    def change_turn(self):
        print("change turn")
        active_players = [p for p in self.players if not p.folded]

        if len(active_players) == 1:
            # text = f"{active_players[0].name} wins the pot of {self.pot} chips!"
            # active_players[0].chips += self.pot
            # self.showcard = True
            # self.add_log(text)
            # self.ask_reset_game(text)
            self.win_pot(active_players[0])
            return

        current_index = active_players.index(self.player_turn) if self.player_turn in active_players else -1
        next_index = (current_index + 1) % len(active_players)
        self.player_turn = active_players[next_index]
        self.add_log(f"{self.player_turn.name}'s Turn")

        if self.player_turn == self.players[1]:
            self.bot_thinking = True
            self.bot_manager.take_action()
            self.bot_thinking = False


    def get_player_turn(self):
        return self.player_turn

    def get_community_cards(self):
        return self.community_cards

    def get_pot(self):
        return self.pot

    def is_your_turn(self):
        return self.player_turn == self.players[0]

    def raise_bet(self, amount):
        if amount > self.player_turn.chips:
            self.show_popup("Invalid Action", "Not enough chips to raise.")
            return
        self._place_bet(amount)
        self.change_turn()

    def check(self):
        if self.bets[self.player_turn] < max(self.bets.values()):
            self.show_popup("Invalid Action", "Cannot check, must call or raise.")
            return
        self.player_turn.checked = True
        self.change_turn()

        if self.all_player_checked():
            self.next_phase()

    def call(self):
        max_bet = max(self.bets.values())
        call_amount = max_bet - self.bets[self.player_turn]
        if call_amount > self.player_turn.chips:
            self.show_popup("Invalid Action", "Not enough chips to call.")
            return
        self._place_bet(call_amount)
        self.change_turn()

        if all(self.bets[player] == max_bet for player in self.players if not player.folded):
            self.next_phase()

    def win_pot(self, player):
        print("called")
        player.chips += self.pot
        self.showcard = True
        text = f"{player.name} wins the pot of {self.pot} chips!"
        self.add_log(text)
        self.ask_reset_game(text)
        return

    def fold(self):
        self.player_turn.fold()
        self.change_turn()

        active_players = [p for p in self.players if not p.folded]
        # if len(active_players) == 1:
        #     # text = f"{active_players[0].name} wins the pot of {self.pot} chips!"
        #     # active_players[0].chips += self.pot
        #     # self.showcard = True
        #     # self.add_log(text)
        #     # self.ask_reset_game(text)
        #     # return
        #     print("1")
        #     self.win_pot(active_players[0])
        #     return

        if all(self.bets[player] == max(self.bets.values()) for player in self.players if not player.folded):
            self.next_phase()

    def next_phase(self):
        print("next phase")
        active_players = [p for p in self.players if not p.folded]

        if len(active_players) == 1:
            # text = f"{active_players[0].name} wins the pot of {self.pot} chips!"
            # active_players[0].chips += self.pot
            # self.showcard = True
            # self.add_log(text)
            # self.ask_reset_game(text)
            # return
            self.win_pot(active_players[0])
            return

        if self._all_bets_equal() and all(player.checked or player.folded for player in active_players):
            self._reset_checked_status()

            if self.turn == "Pre-Flop":
                self.turn = "Flop"

                self.add_log("Game Turn: Preflop")

            elif self.turn == "Flop":
                self.community_cards.extend([self.deck.draw() for _ in range(3)])
                self.turn = "Turn"

                self.add_log("Game Turn: Flop")

            elif self.turn == "Turn":
                self.community_cards.append(self.deck.draw())
                self.turn = "River"

                self.add_log("Game Turn: Turn")

            elif self.turn == "River":
                self.community_cards.append(self.deck.draw())
                self.turn = "Showdown"

                self.add_log("Game Turn: River")

            elif self.turn == "Showdown":
                self.turn = "ShowCard"
                self.add_log("Game Turn: Showdown")
                hand1 = self.players[0].hand
                hand2 = self.players[1].hand
                result = HandEvaluator.compare_hands(hand1, hand2)
                text = ""
                if result[1] == "hand1":
                    self.players[1].fold()
                    self.win_pot(self.players[0])
                    
                elif result[1] == "hand2":
                    self.players[0].fold()
                    self.win_pot(self.players[1])

                elif result[1] == "tie":
                    players = self.get_all_players()
                    amount = self.pot // len(players)
                    for player in players:
                        player.add_chips(amount)
                    text = f"All player tied! The pot of {self.pot} chips is split!"

                self.showcard = True
                self.add_log(text)
                self.ask_reset_game(text)

    
    def ask_reset_game(self, text):
        if self.reset_in_progress:
            return

        self.reset_in_progress = True

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        result = messagebox.askyesno(f"{text}\nContinue Game", "Do you want to continue the game?", parent=root)
        root.destroy()

        if result:
            def reset_wrapper():
                self.reset_game()
                self.reset_in_progress = False
            threading.Timer(4.0, reset_wrapper).start() # from chatGPT it will wait for the reset_wrapper to finish first
        else:
            self.reset_in_progress = False


    def _all_bets_equal(self):
        max_bet = max(self.bets.values())
        return all(self.bets[player] == max_bet for player in self.players if not player.folded)

    def _reset_checked_status(self):
        for player in self.players:
            player.checked = False

    def _place_bet(self, amount):
        self.bets[self.player_turn] += amount
        self.player_turn.deduct_chips(amount)
        self.pot += amount

    def show_popup(self, title, message):
        popup_root = tk.Tk()
        popup_root.withdraw()
        popup_root.attributes("-topmost", True)

        messagebox.showerror(title, message, parent=popup_root)
        popup_root.destroy()

    def add_log(self, text):
        self.log.append(text)

    @staticmethod
    def convert_name(card: Card):
        rank_name = {
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '10': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'
        }
        suit_name = {
            '♠': 'spades', '♥': 'hearts', '♦': 'diamonds', '♣': 'clubs'
        }
        rank = rank_name[card.rank]
        suit = suit_name[card.suit]
        return f"{rank}_of_{suit}.png"
