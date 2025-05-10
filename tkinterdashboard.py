import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Read CSV data
def load_data():

    column_names = [
    "rounds_played", "number_of_folds", "number_of_raises", "number_of_calls", "number_of_bets", "number_of_checks",
    "preflop_folds", "preflop_raises", "preflop_calls", "preflop_bets", "preflop_checks",
    "flop_folds", "flop_raises", "flop_calls", "flop_bets", "flop_checks",
    "turn_folds", "turn_raises", "turn_calls", "turn_bets", "turn_checks",
    "river_folds", "river_raises", "river_calls", "river_bets", "river_checks",
    "total_wins", "total_losses", "total_chips_won", "total_chips_lost",
    "went_to_showdown", "won_at_showdown", "calculated_winrate_before_game_end", "hand"
    ]
    return pd.read_csv('data/poker_data.csv', header=None, names=column_names)

# Plot 1: Player Betting Patterns
def plot_betting_patterns(frame, df):

    actions = ['number_of_folds', 'number_of_raises', 'number_of_calls', 'number_of_bets', 'number_of_checks']
    frequencies = df[actions].sum()
    
    fig, ax = plt.subplots(figsize=(12, 8))  # Increase figure size
    ax.bar(actions, frequencies)
    ax.set_title('Betting Action Frequency')
    ax.set_xlabel('Betting Action Type')
    ax.set_ylabel('Frequency')
    ax.tick_params(axis='x', labelrotation=30)  # Rotate x-axis labels

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Plot 2: Cheat Engine vs Actual Win Rate
def plot_winrate_correlation(frame, df):
    if 'calculated_winrate_before_game_end' not in df or 'total_wins' not in df:
        return
    df = df[df['rounds_played'] > 0]
    df['actual_win_rate'] = df['total_wins'] / (df['total_wins'] + df['total_losses'])

    fig, ax = plt.subplots()
    ax.scatter(df['calculated_winrate_before_game_end'], df['actual_win_rate'])
    ax.set_title('Cheat Engine vs Actual Win Rate')
    ax.set_xlabel('Predicted Win Rate')
    ax.set_ylabel('Actual Win Rate')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Plot 3: Number of Hands Played, Won, Lost
def plot_hand_stats(frame, df):
    hand_types = df['hand'].value_counts()
    
    fig, ax = plt.subplots()
    sizes = hand_types.values
    labels = hand_types.index
    ax.scatter(labels, sizes, s=sizes * 10, alpha=0.5)
    ax.set_title('Common Winning Hands')
    ax.set_xlabel('Hand Type')
    ax.set_ylabel('Frequency of Wins')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Main UI window
def launch_dashboard():
    df = load_data()
    root = tk.Tk()
    root.title("Poker Statistics Dashboard")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create tabs
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text="Betting Patterns")
    notebook.add(tab2, text="Win Rate Correlation")
    notebook.add(tab3, text="Winning Hands")

    # Plot inside tabs
    plot_betting_patterns(tab1, df)
    plot_winrate_correlation(tab2, df)
    plot_hand_stats(tab3, df)

    root.mainloop()

launch_dashboard()
