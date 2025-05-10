import csv
import os

class Data:
    def __init__(self):
        self.rounds_played = 0
        self.number_of_folds = 0
        self.number_of_raises = 0
        self.number_of_calls = 0
        self.number_of_bets = 0
        self.number_of_checks = 0

        self.preflop_folds = 0
        self.preflop_raises = 0
        self.preflop_calls = 0
        self.preflop_bets = 0
        self.preflop_checks = 0

        self.flop_folds = 0
        self.flop_raises = 0
        self.flop_calls = 0
        self.flop_bets = 0
        self.flop_checks = 0

        self.turn_folds = 0
        self.turn_raises = 0
        self.turn_calls = 0
        self.turn_bets = 0
        self.turn_checks = 0

        self.river_folds = 0
        self.river_raises = 0
        self.river_calls = 0
        self.river_bets = 0
        self.river_checks = 0

        self.total_wins = 0
        self.total_losses = 0
        self.total_chips_won = 0
        self.total_chips_lost = 0
        self.went_to_showdown = 0
        self.won_at_showdown = 0

        self.calculated_winrate_before_game_end = 0
        self.hand = ""

    def to_dict(self):
        return self.__dict__

    def save_to_csv(self, filename='data/poker_data.csv'):
        data_dict = self.to_dict()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
