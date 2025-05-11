import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
            "flop_fold", "flop_call", "flop_raise", "flop_check",
            "turn_fold", "turn_call", "turn_raise", "turn_check",
            "river_fold", "river_call", "river_raise", "river_check"
        ]
        try:
            return pd.read_csv(self.csv_path, header=0, names=column_names)
        except pd.errors.ParserError as e:
            print(f"Error reading CSV file: {e}")
            return pd.DataFrame(columns=column_names)

    def plot_action_distribution(self, frame):
        stages = ['Preflop', 'Flop', 'Turn', 'River']
        actions = ['fold', 'call', 'raise', 'check']
        stage_columns = {
            'Preflop': ['preflop_fold', 'preflop_call', 'preflop_raise', 'preflop_check'],
            'Flop': ['flop_fold', 'flop_call', 'flop_raise', 'flop_check'],
            'Turn': ['turn_fold', 'turn_call', 'turn_raise', 'turn_check'],
            'River': ['river_fold', 'river_call', 'river_raise', 'river_check']
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

    # def plot_winrate_vs_showdown(self, frame):
    #     self.df['winrate'] = self.df['total_wins'] / self.df['rounds_played']
    #     self.df['showdown_frequency'] = self.df['showdown_reached'] / self.df['rounds_played']
    #     self.df['showdown_winrate'] = self.df['showdown_wins'] / self.df['showdown_reached']

    #     self.df['winrate'] = self.df['winrate'].fillna(0).replace([float('inf'), -float('inf')], 0)
    #     self.df['showdown_frequency'] = self.df['showdown_frequency'].fillna(0).replace([float('inf'), -float('inf')], 0)
    #     self.df['showdown_winrate'] = self.df['showdown_winrate'].fillna(0).replace([float('inf'), -float('inf')], 0)

    #     self.df = self.df.reset_index(drop=True)

    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     ax.plot(self.df.index, self.df['winrate'], label='Winrate', marker='o')
    #     ax.plot(self.df.index, self.df['showdown_frequency'], label='Showdown Frequency', marker='o')
    #     ax.plot(self.df.index, self.df['showdown_winrate'], label='Showdown Winrate', marker='o')

    #     ax.set_title('Winrate vs Showdown Frequency')
    #     ax.set_xlabel('Game Rounds')
    #     ax.set_ylabel('Rate')
    #     ax.legend()

    #     canvas = FigureCanvasTkAgg(fig, master=frame)
    #     canvas.draw()
    #     canvas.get_tk_widget().pack()
        
    def plot_hand_strength(self, frame):
        winning_hands = self.df['winning_hand_type'].value_counts()
        losing_hands = self.df['losing_hand_type'].value_counts()

        all_hand_types = set(winning_hands.index).union(set(losing_hands.index))
        hand_win_rates = {}

        for hand in all_hand_types:
            wins = winning_hands.get(hand, 0)
            losses = losing_hands.get(hand, 0)
            total = wins + losses
            if total > 0:
                hand_win_rates[hand] = (wins / total) * 100

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        pd.Series(hand_win_rates).sort_values(ascending=True).plot(
            kind='barh', ax=ax, color='lightgreen', alpha=0.8
        )

        ax.set_title('Win Rate by Hand Type (When Drawn)')
        ax.set_xlabel('Win Rate (%)')
        ax.set_ylabel('Hand Type')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    def plot_estimated_vs_chips_won(self, frame):
        x = self.df['estimated_winrate']
        y = self.df['total_chips_won']

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, color='teal', alpha=0.6)

        if len(x) > 1 and x.nunique() > 1:
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color='red', linestyle='--', label='Trend Line')

        ax.set_title('Estimated Winrate vs Total Chips Won')
        ax.set_xlabel('Estimated Winrate (%)')
        ax.set_ylabel('Total Chips Won')
        ax.set_xlim(0, 100)
        ax.set_ylim(min(0, y.min()), y.max() * 1.1)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    
    def plot_winrate_vs_foldrate(self, frame):
        actions = ['total_folds', 'total_calls', 'total_raises', 'total_checks']
        self.df['action_total'] = self.df[actions].sum(axis=1)
        self.df['fold_rate'] = self.df['total_folds'] / self.df['action_total'].replace(0, 1)

        x = self.df['estimated_winrate']
        y = self.df['fold_rate']

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x, y, color='orange', alpha=0.6)

        # Add a trendline if data varies
        if len(x) > 1 and x.nunique() > 1:
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color='red', linestyle='--', label='Trend Line')

        ax.set_title('Fold Rate vs Estimated Winrate')
        ax.set_xlabel('Estimated Winrate (%)')
        ax.set_ylabel('Fold Rate')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 1)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    def plot_action_boxplot(self, frame):
        data = [
            self.df['total_folds'],
            self.df['total_calls'],
            self.df['total_raises'],
            self.df['total_checks']
        ]
        labels = ['Folds', 'Calls', 'Raises', 'Checks']

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(data, vert=True, patch_artist=True, labels=labels, notch=True, widths=0.5)

        ax.set_title('Distribution of Actions (Folds, Calls, Raises, Checks)')
        ax.set_ylabel('Action Count')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def plot_winrate_distribution(self, frame):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.df['estimated_winrate'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)

        ax.set_title('Distribution of Estimated Winrates')
        ax.set_xlabel('Estimated Winrate (%)')
        ax.set_ylabel('Frequency')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    def add_summary_table_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="All Data Table")

        columns = ("pattern", "rounds", "fold_bet_call_raise", "winrates", "hands_summary")
        tree = ttk.Treeview(tab, columns=columns, show='headings', height=10)

        tree.heading("pattern", text="Player Betting Pattern")
        tree.heading("rounds", text="Rounds Played")
        tree.heading("fold_bet_call_raise", text="Folds/Bets/Calls/Raises")
        tree.heading("winrates", text="Cheat vs Actual Winrate")
        tree.heading("hands_summary", text="Hands Played/Won/Lost")

        tree.column("pattern", width=160)
        tree.column("rounds", width=100)
        tree.column("fold_bet_call_raise", width=180)
        tree.column("winrates", width=180)
        tree.column("hands_summary", width=180)

        for _, row in self.df.iterrows():
            folds = row['total_folds']
            bets = row[['preflop_raise', 'flop_raise', 'turn_raise', 'river_raise']].sum()
            calls = row['total_calls']
            raises = row['total_raises']

            pattern = "Aggressive" if (raises + bets) > (folds + calls) else "Passive"

            cheat_winrate = round(row['estimated_winrate'], 2)
            actual_winrate = round((row['total_wins'] / row['rounds_played']) * 100 if row['rounds_played'] else 0, 2)

            winrate_str = f"{cheat_winrate}% vs {actual_winrate}%"
            actions_str = f"{int(folds)}/{int(bets)}/{int(calls)}/{int(raises)}"
            hands_str = f"{int(row['rounds_played'])}/{int(row['total_wins'])}/{int(row['total_losses'])}"

            tree.insert("", "end", values=(pattern, int(row['rounds_played']), actions_str, winrate_str, hands_str))

        tree.pack(fill='both', expand=True)

    def add_analysis_summary_tab(self):
        import pandas as pd
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Summary Analysis")

        tree = ttk.Treeview(tab, columns=("Metric", "Value"), show="headings", height=8)
        tree.heading("Metric", text="Metric")
        tree.heading("Value", text="Value")

        tree.column("Metric", width=200)
        tree.column("Value", width=150)

        df = self.df

        total_rounds = int(df['rounds_played'].sum())
        avg_estimated_winrate = round(df['estimated_winrate'].mean(), 2)
        total_wins = int(df['total_wins'].sum())
        total_losses = int(df['total_losses'].sum())
        win_loss_ratio = round(total_wins / total_losses, 2) if total_losses != 0 else "N/A"
        net_chips = int(df['total_chips_won'].sum() - df['total_chips_lost'].sum())
        total_showdowns = df['showdown_reached'].sum()
        total_showdown_wins = df['showdown_wins'].sum()
        showdown_winrate = round((total_showdown_wins / total_showdowns) * 100, 2) if total_showdowns != 0 else 0

        metrics = {
            "Total Rounds Played": total_rounds,
            "Avg Estimated Winrate (%)": avg_estimated_winrate,
            "Win/Loss Ratio": win_loss_ratio,
            "Net Chips Gained": net_chips,
            "Showdown Winrate (%)": showdown_winrate
        }

        for key, value in metrics.items():
            tree.insert("", "end", values=(key, value))

        tree.pack(fill='both', expand=True)



    def create_tabs(self):
        self.notebook.pack(fill='both', expand=True)

        tab1 = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)
        tab3 = ttk.Frame(self.notebook)
        tab4 = ttk.Frame(self.notebook)
        tab5 = ttk.Frame(self.notebook)
        
        
        self.notebook.add(tab1, text="Action Distribution")
        self.notebook.add(tab2, text="Winrate Distribution")
        self.notebook.add(tab3, text="Hand Strength Frequency")
        self.notebook.add(tab4, text="Estimated Winrate vs Chips Won")
        self.notebook.add(tab5, text="Winrate vs Fold Rate")

        self.plot_action_distribution(tab1)
        self.plot_winrate_distribution(tab2)
        self.plot_hand_strength(tab3)
        self.plot_estimated_vs_chips_won(tab4)
        self.plot_winrate_vs_foldrate(tab5)
        self.add_analysis_summary_tab()
        self.add_summary_table_tab()
        
    def run(self):
        self.create_tabs()
        self.root.mainloop()

if __name__ == "__main__":
    dashboard = PokerDataDashboard(csv_path='data/poker_data.csv')
    dashboard.run()