import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PokerDataDashboard:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = self.load_data()
        self.root = tk.Tk()
        self.root.title("Poker Data Dashboard")
        self.notebook = ttk.Notebook(self.root)

    def load_data(self):
        column_names = [
            "rounds_played", "total_chips_won", "total_chips_lost", "total_wins", "total_losses",
            "showdown_reached", "showdown_wins", "total_folds", "total_calls", "total_raises", "total_checks",
            "estimated_winrate", "winning_hand_type", "losing_hand_type",
            "preflop_fold", "preflop_call", "preflop_raise", "preflop_check",
            "flop_fold", "flop_call", "flop_raise", "flop_bet", "flop_check",
            "turn_fold", "turn_call", "turn_raise", "turn_bet", "turn_check",
            "river_fold", "river_call", "river_raise", "river_bet", "river_check"
        ]
        return pd.read_csv(self.csv_path, header=0, names=column_names)

    def plot_action_distribution(self, frame):
        stages = ['Preflop', 'Flop', 'Turn', 'River']
        actions = ['fold', 'call', 'raise', 'check']
        stage_columns = {
            'Preflop': ['preflop_fold', 'preflop_call', 'preflop_raise', 'preflop_check'],
            'Flop': ['flop_fold', 'flop_call', 'flop_raise', 'flop_bet', 'flop_check'],
            'Turn': ['turn_fold', 'turn_call', 'turn_raise', 'turn_bet', 'turn_check'],
            'River': ['river_fold', 'river_call', 'river_raise', 'river_bet', 'river_check']
        }

        action_data = {stage: self.df[columns].sum().values for stage, columns in stage_columns.items()}

        fig, ax = plt.subplots(figsize=(10, 6))
        bottom = [0] * len(stages)
        for i, action in enumerate(actions):
            values = [action_data[stage][i] for stage in stages]
            ax.bar(stages, values, bottom=bottom, label=action)
            bottom = [bottom[j] + values[j] for j in range(len(values))]

        ax.set_title('Action Distribution per Stage')
        ax.set_xlabel('Game Stage')
        ax.set_ylabel('Frequency')
        ax.legend(title='Actions')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def plot_winrate_vs_showdown(self, frame):
        # Calculate winrate, showdown frequency, and showdown winrate
        self.df['winrate'] = self.df['total_wins'] / self.df['rounds_played']
        self.df['showdown_frequency'] = self.df['showdown_reached'] / self.df['rounds_played']
        self.df['showdown_winrate'] = self.df['showdown_wins'] / self.df['showdown_reached']

        # Handle missing or invalid values
        self.df['winrate'] = self.df['winrate'].fillna(0).replace([float('inf'), -float('inf')], 0)
        self.df['showdown_frequency'] = self.df['showdown_frequency'].fillna(0).replace([float('inf'), -float('inf')], 0)
        self.df['showdown_winrate'] = self.df['showdown_winrate'].fillna(0).replace([float('inf'), -float('inf')], 0)

        # Ensure the index is numeric
        self.df = self.df.reset_index(drop=True)  # Reset index to ensure it's numeric

        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.df.index, self.df['winrate'], label='Winrate', marker='o')
        ax.plot(self.df.index, self.df['showdown_frequency'], label='Showdown Frequency', marker='o')
        ax.plot(self.df.index, self.df['showdown_winrate'], label='Showdown Winrate', marker='o')

        ax.set_title('Winrate vs Showdown Frequency')
        ax.set_xlabel('Game Rounds')
        ax.set_ylabel('Rate')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def plot_hand_strength(self, frame):
        # Calculate the frequency of each winning hand type
        winning_hands = self.df['winning_hand_type'].value_counts()

        # Calculate the total number of wins
        total_wins = self.df['total_wins'].sum()

        # Calculate the win rate for each hand type
        win_rates = (winning_hands / total_wins) * 100  # Convert to percentage

        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 6))
        win_rates.sort_values(ascending=True).plot(kind='barh', ax=ax, color='skyblue', alpha=0.8)

        # Set plot title and labels
        ax.set_title('Winning Hands with Win Rates')
        ax.set_xlabel('Win Rate (%)')
        ax.set_ylabel('Hand Type')

        # Add the canvas to the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_tabs(self):
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        tab1 = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)
        tab3 = ttk.Frame(self.notebook)

        self.notebook.add(tab1, text="Action Distribution")
        self.notebook.add(tab2, text="Winrate vs Showdown")
        self.notebook.add(tab3, text="Hand Strength Frequency")

        # Plot graphs in tabs
        self.plot_action_distribution(tab1)
        self.plot_winrate_vs_showdown(tab2)
        self.plot_hand_strength(tab3)

    def run(self):
        self.create_tabs()
        self.root.mainloop()


# Run the dashboard
if __name__ == "__main__":
    dashboard = PokerDataDashboard(csv_path='data/poker_data.csv')
    dashboard.run()