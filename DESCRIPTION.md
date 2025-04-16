Poker with Cheats
 
Project Overview
This is a simple two-player poker game. You play against a bot, but there’s a twist where you can see your hand’s win rate. It calculates your chances of winning based on the community cards and your opponent’s hand, giving you a huge advantage.


2.                Project Review
I will study PyPokerEngine, an open-source poker simulator that allows bots and AI strategies. And maybe take some of their code and improve it by displaying real-time win rate instead.
3.                Programming Development
3.1 Game Concept
It’s just basically poker with standard poker rules where everyone draws 2 and just gambles (without using real money) while each community card gets revealed. But you, the player will see your own win rate so you can decide when to fold or just go all in.
 
3.2  Object-Oriented Programming Implementation
PokerGame – Controls overall game flow (rounds, betting, turns)
Player – Represent each player (hand, chips, action)
Dealer – Manage the deck, deals cards and controls game rules
Deck – Handles shuffling and dealing cards
Hand – Manages each player’s best 5-card combinations
PokerTable – Handles the display of cards, chips and UI in Pygame
ProbabilityCalculator – Shows the win percentage cheat in real-time


 UML Diagram (Old)


UML Diagram (Fixed) - Notes: I have been doing my project since last week i have made large changes to these classes I will update the new uml diagram later


3.3 Algorithms Involved
There would be 2 main algorithms involved.
Hand Evaluation Algorithm
This algorithm determines the strength of a player’s hand based on standard Texas Hold’em hand rankings (e.g., High Card, Pair, Flush, Straight, Full House, etc.) (rule-based evaluation system.
Monte Carlo Simulation (Win Rate Calculation)
The Monte Carlo method is used to estimate win probability by estimating the win rate by simulating thousands of possible outcomes based on the remaining deck.
4.                Statistical Data (Prop Stats)
4.1 Data Features
Describe at least five features you will track in the game, which may include player behavior or game-related metrics (e.g., character movement, keystrokes, pixels moved, player score, time played, enemies defeated, accuracy, and completion rate). Each feature should have at least 50 rows of data. (For example, in football, a player’s performance can be analyzed by collecting and analyzing statistical data.)
1. Player Betting Patterns, Rounds Played (pre-flop, flop, turn, river), win rate, opponent actions (?)
2. Win rate at each decision point (bet, fold, call, raise)
3. Bot response behavior (I plan to make to bot behavior random)
4. Number of times the player folds, win rate at fold, bot’s previous action
5. Number of hands played, hands won, hands lost.








Why it is good to have this data? What can it be used for
How will you obtain 50 values of this feature data?
Which variable (and which class will you collect this from?)
How will you display this feature data (via summarization statistics or via graph)?
Player Betting Patterns
Used for predicting what most players do
I can take the patterns round by round instead of game by game
betting_patterns (from Player)
Bar Graph: Shows the frequency of each betting action (fold, bet, call, raise) per round
Rounds Played
To know how long does the average goes
Simulate for 50 games
rounds_played (from PokerGame)
Bar Graph: Displays the average number of rounds per game
Number of folds, bet, call, raise in a game
To know which action leads to the most win
I can take the patterns round by round instead of game by game
action_counts (from PokerGame
Bar Graph: Compares the frequency of each action type in winning vs. losing games
cheat engine win rate and the actual win rate (after the game ends)
show how accurate the cheat engine can predict winning games
Simulate for 50 games
predicted_win_rate (from ProbabilityCalculator)
Scatter Plot: Plots cheat engine win rate against actual win rate to observe correlation
Number of hands played, hands won, hands lost.
To show which hands are the most common and which hand won the most
Simulate for 50 games
hand_history (from PokerGame)
 Table + Bubble Plot: Table summarizes hand statistics Bubble Plot visualizes the most frequent winning hands


Could put more but I’m not sure that it is necessary
Update Note: The variables that I have stated haven't been added to the uml because i have made major changes to my code and class structure but this is what I have planned out.

Statistical Data Revision
Feature Name
 Graph objective
Graph type
 X-axis
 Y-axis
Statistical Value
Player Betting Patterns 
Show the frequency of different betting actions per round 
Bar Graph 
Betting Action Type 
Frequency  
Mode, Frequency Distribution
Cheat Engine Win Rate vs. Actual Win Rate
Show accuracy of cheat engine predictions
Scatter Plot 
Predicted Win Rate 
Actual Win Rate
Correlation Coefficient
Number of Hands Played, Won, Lost 
Identify the most common winning hands  
Bubble Plot 
Hand Type 
Frequency of Wins 
Average (Mean)






3.2 Data Recording Method
Explain how the game will store statistical data. Will it be saved in a database, CSV file, or another format?
I’m planning to go easy on the CSV file but if I’m working with a larger db. I would maybe consider mongo or SQL server. (Planning to use CSV)


3.3 Data Analysis Report
Outline how you will analyze the recorded data. What statistical measures will you use? How will the analysis be presented (e.g., graphs, tables, charts)?
I would analyze the data using the table, it would be the easiest.
I will use a scatter plot graph between the cheat engine win rate and the actual win rate (after the game ends). This will show how accurate the cheat engine can predict winning games.
4. Project Timeline
 
Week
Task
1 (10 March)
Proposal submission / Project initiation
2 (17 March)
Full proposal submission
3 (24 March)
Do the base code for every feature
4 (31 March)
Finished all the feature
5 (7 April)
Last check up on bugs and error done
6 (14 April)
Submission week (Draft)

 Continue Planning

Week
Task
26 March-2 April


Try to finish the main game logic and making the game work
3 April-9 April


Add more features that have been missed out or necessary UI
10 April-16 April


Refactor All the code so it looks cleaner and more reusable
17 April-23 April


Check for bugs (UI & Features)
24 April-11 May
Last check up to get ready for the submission



5. Document version
Version: 3.0
Date: 31 March 2025
Munyin Sam 6710545962


Date
Name
Description of Revision, Feedback, Comments
14/3
Rattapoom
Data Analysis report requires explanation on statistical issues. Other than that, Good Job!
16/3
Parima
The overall document is clear.
28/3
Rattapoom
Some comments on UML class diagram
Please also tell us which variable you’re planning to use to collect those data
30/3
Parima
The UML diagram needs some revision.




