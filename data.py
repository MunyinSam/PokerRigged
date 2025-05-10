import csv
import os

class Data:
    def __init__(self):
        # General round info
        self.rounds_played = 0
        self.total_chips_won = 0
        self.total_chips_lost = 0
        self.total_wins = 0
        self.total_losses = 0
        self.showdown_reached = 0
        self.showdown_wins = 0

        # Player action frequency
        self.total_folds = 0
        self.total_calls = 0
        self.total_raises = 0
        self.total_checks = 0

        # Winrate tracking
        self.estimated_winrate = 0.0  # Value shown to player at button press

        # Hand type summary
        self.winning_hand_type = ""  # e.g. "Pair", "Flush"
        self.losing_hand_type = ""   # Same as above

        # Stage-specific actions
        self.preflop_actions = {"fold": 0, "call": 0, "raise": 0, "check": 0}
        self.flop_actions = {"fold": 0, "call": 0, "raise": 0, "bet": 0, "check": 0}
        self.turn_actions = {"fold": 0, "call": 0, "raise": 0, "bet": 0, "check": 0}
        self.river_actions = {"fold": 0, "call": 0, "raise": 0, "bet": 0, "check": 0}

    def to_dict(self):
        data = self.__dict__.copy()
        # Flatten stage action dictionaries
        for stage in ["preflop", "flop", "turn", "river"]:
            for action, value in data[f"{stage}_actions"].items():
                data[f"{stage}_{action}"] = value
            del data[f"{stage}_actions"]
        return data

    def save_to_csv(self, filename='data/poker_data.csv'):
        print("Saving data to CSV...")
        data_dict = self.to_dict()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
