import pygame as pg
from component import *
from handeval import HandEvaluator
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
from data import Data
from component import Player, Bot, Deck, Card, PlayerManager, BotManager

class PokerGame:
    def __init__(self, screen):
        self.screen = screen
        self.reset_in_progress = False
        self.start_game()

    def start_game(self):
        self.deck = Deck()
        self.turn = "Pre-Flop"
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
        self.rounds_played = 1
        self.data.rounds_played += 1

        self.isloading = False
        self.bot_actions = None
        self.game_ended = False

    def reset_game(self):
        self.isloading = True
        self.bot_actions = None
        self.game_ended = False

        winrate = HandEvaluator.calculate_winrate(self.get_all_players()[0].hand, self.get_community_cards())
        print("winrate ", winrate)
        print("winrate function called")
        self.data.estimated_winrate = winrate
        self.data.save_to_csv()

        self.data = Data()
        self.data.rounds_played = self.rounds_played
        self.rounds_played += 1

        self.deck = Deck()
        self.showcard = False
        self.log = []

        for player in self.players:
            player.folded = False
            player.checked = False
            player.hand = []

        active_players = [p for p in self.players if not p.folded]

        self.turn = "Pre-Flop"
        self.player_turn = self.players[0]
        self.community_cards = []
        self.pot = 0
        self.bets = {player: 0 for player in self.players}
        self.bot_thinking = False

        def loading_action():
            self.isloading = False
        threading.Timer(2, loading_action).start()

        self.give_out_cards()

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
            self.win_pot([active_players[0]])
            if active_players[0] == self.players[0]:
                print("Player 1 wins")
                self.data.winning_hand_type = HandEvaluator.evaluate_hand(self.get_all_players()[0].hand + self.community_cards)[0]
                self.data.losing_hand_type = HandEvaluator.evaluate_hand(self.get_all_players()[1].hand + self.community_cards)[0]
            else:
                print("Player 2 wins")
                self.data.winning_hand_type = HandEvaluator.evaluate_hand(self.get_all_players()[1].hand + self.community_cards)[0]
                self.data.losing_hand_type = HandEvaluator.evaluate_hand(self.get_all_players()[0].hand + self.community_cards)[0]
            return

        current_index = active_players.index(self.player_turn) if self.player_turn in active_players else -1
        next_index = (current_index + 1) % len(active_players)
        self.player_turn = active_players[next_index]
        self.add_log(f"{self.player_turn.name}'s Turn")

        if self.player_turn == self.players[1]:
            self.bot_thinking = True
            print("Bot thinking")

            def bot_action():
                self.bot_manager.take_action()
                self.bot_actions = self.bot_manager.bot_actions
                self.bot_thinking = False

            threading.Timer(1.5, bot_action).start()

    def get_bot_actions(self):
        return self.bot_actions

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
        
        if self.turn == "Pre-Flop":
            self.data.preflop_actions["raise"] += 1
        elif self.turn == "Flop":
            self.data.flop_actions["raise"] += 1
        elif self.turn == "Turn":
            self.data.turn_actions["raise"] += 1
        elif self.turn == "River":
            self.data.river_actions["raise"] += 1

        self.data.total_raises += 1
        self.change_turn()

    def check(self):
        if self.bets[self.player_turn] < max(self.bets.values()):
            self.show_popup("Invalid Action", "Cannot check, must call or raise.")
            return
        self.player_turn.checked = True

        if self.turn == "Pre-Flop":
            self.data.preflop_actions["check"] += 1
        elif self.turn == "Flop":
            self.data.flop_actions["check"] += 1
        elif self.turn == "Turn":
            self.data.turn_actions["check"] += 1
        elif self.turn == "River":
            self.data.river_actions["check"] += 1

        self.data.total_checks += 1
        self.change_turn()

        if self.all_player_checked():
            self.next_phase()

    def call(self):
        max_bet = max(self.bets.values())
        call_amount = max_bet - self.bets[self.player_turn]

        if call_amount == 0:
            self.show_popup("Invalid Action", "There is no bet to call.")
            return

        if call_amount > self.player_turn.chips:
            self.show_popup("Invalid Action", "Not enough chips to call.")
            return

        self.bets[self.player_turn] += call_amount
        self.player_turn.deduct_chips(call_amount)
        self.pot += call_amount

        if self.turn == "Pre-Flop":
            self.data.preflop_actions["call"] += 1
        elif self.turn == "Flop":
            self.data.flop_actions["call"] += 1
        elif self.turn == "Turn":
            self.data.turn_actions["call"] += 1
        elif self.turn == "River":
            self.data.river_actions["call"] += 1

        self.data.total_calls += 1
        self.change_turn()

        if all(self.bets[player] == max_bet for player in self.players if not player.folded):
            self.next_phase()

    def fold(self):
        if self.reset_in_progress:
            return

        self.player_turn.fold()

        if self.turn == "Pre-Flop":
            self.data.preflop_actions["fold"] += 1
        elif self.turn == "Flop":
            self.data.flop_actions["fold"] += 1
        elif self.turn == "Turn":
            self.data.turn_actions["fold"] += 1
        elif self.turn == "River":
            self.data.river_actions["fold"] += 1

        self.data.total_folds += 1
        self.change_turn()

        active_players = [p for p in self.players if not p.folded]
        if all(self.bets[player] == max(self.bets.values()) for player in self.players if not player.folded):
            self.next_phase()

    def win_pot(self, players, text=None, condition=None):
        if self.reset_in_progress or self.game_ended:
            return

        print("win pot")
        self.game_ended = True
        if condition == "tie":
            for player in players:
                player.chips += self.pot // len(players)
        else:
            for player in players:
                player.chips += self.pot
        self.showcard = True

        if len(players) == 1:
            if players[0] == self.players[0]:
                self.data.total_wins += 1
                self.data.total_chips_won += self.pot
            else:
                self.data.total_losses += 1
                self.data.total_chips_lost += self.pot

            if text:
                self.ask_reset_game(text)
            else:
                self.ask_reset_game(f"{player.name} wins the pot of {self.pot} chips!")

        else:
            if text:
                self.ask_reset_game(text)
            else:
                self.ask_reset_game(f"Both players wins the pot of {self.pot} chips!")

    def next_phase(self):
        print("next phase")
        active_players = [p for p in self.players if not p.folded]

        if len(active_players) == 1:
            if not self.reset_in_progress:
                self.win_pot([active_players[0]])
            return

        if self._all_bets_equal() and all(player.checked or player.folded for player in active_players):
            self._reset_checked_status()

            if self.turn == "Pre-Flop":
                self.turn = "Flop"
                print("Game Turn: Preflop")

            elif self.turn == "Flop":
                self.community_cards.extend([self.deck.draw() for _ in range(3)])
                self.turn = "Turn"
                print("Game Turn: Flop")

            elif self.turn == "Turn":
                self.community_cards.append(self.deck.draw())
                self.turn = "River"
                print("Game Turn: Turn")

            elif self.turn == "River":
                self.community_cards.append(self.deck.draw())
                self.turn = "Showdown"
                print("Game Turn: River")

            elif self.turn == "Showdown":
                print("Game Turn: Showdown")
                self.data.showdown_reached += 1
                hand1 = self.players[0].hand + self.community_cards
                hand2 = self.players[1].hand + self.community_cards
                result = HandEvaluator.compare_hands(hand1, hand2)
                text = result[0]

                print("results", result)

                if result[1] == "hand1":
                    print("Player 1 wins")
                    self.data.showdown_wins += 1
                    self.players[1].fold()
                    self.win_pot([self.players[0]], text)
                    self.data.winning_hand_type = HandEvaluator.evaluate_hand(hand1)[0]
                    self.data.losing_hand_type = HandEvaluator.evaluate_hand(hand2)[0]

                elif result[1] == "hand2":
                    print("Player 2 wins")
                    self.players[0].fold()
                    self.win_pot([self.players[1]], text)
                    self.data.losing_hand_type = HandEvaluator.evaluate_hand(hand1)[0]
                    self.data.winning_hand_type = HandEvaluator.evaluate_hand(hand2)[0]

                elif result[1] == "tie":
                    players = self.get_all_players()
                    amount = self.pot // len(players)
                    text = f"All players tied! The pot of {self.pot} chips is split!"
                    self.win_pot(players, text, "tie")

                self.showcard = True
                # self.add_log(text)

    def ask_reset_game(self, text):
        if self.reset_in_progress:
            return

        self.reset_in_progress = True

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        result = messagebox.askyesno(f"Continue Game", f"{text}\nDo you want to continue the game?", parent=root)
        root.destroy()

        if result:
            def reset_wrapper():
                self.reset_game()
                self.reset_in_progress = False
                self.game_ended = False
            threading.Timer(2.0, reset_wrapper).start()
        else:
            self.reset_in_progress = False

    def _all_bets_equal(self):
        max_bet = max(self.bets.values())
        return all(self.bets[player] == max_bet for player in self.players if not player.folded)

    def _reset_checked_status(self):
        for player in self.players:
            player.checked = False

    def _place_bet(self, amount):
        if amount > self.players[0].chips or amount > self.players[1].chips:
            return
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
