# Final Project Proposal

## Poker with Cheats

### 1. Project Overview

This is a simple two-player poker game. You play against a bot, but there’s a twist where you can see your hand’s win rate. It calculates your chances of winning based on the community cards and your opponent’s hand, giving you a huge advantage.

### 2. Project Review

I will study PyPokerEngine, an open-source poker simulator that allows bots and AI strategies. And maybe take some of their code and improve it by displaying real-time win rate instead.

### 3. Programming Development

#### 3.1 Game Concept

It’s just basically poker with standard poker rules where everyone draws 2 and just gambles (without using real money) while each community card gets revealed. But you, the player, will see your own win rate so you can decide when to fold or just go all in.

#### UML

Link: [Figma UML Diagram](https://www.figma.com/board/Jy0BgqFlQyyYlj0d4zlDq5/Untitled?node-id=0-1&t=2gDsbJ93iWDcF8cq-1)

#### 3.3 Algorithms Involved

- **Hand Evaluation Algorithm**:  
  Determines the strength of a player’s hand based on standard Texas Hold’em rankings.

- **Monte Carlo Simulation (Win Rate Calculation)**:  
  Estimates win probability by simulating thousands of outcomes based on the remaining deck.

### 4. Statistical Data (Prop Stats)

#### 4.1 Data Features

| Feature Name           | Why is it good to have this data?                      | How will you obtain 50 values of this feature data?       | Which variable/class will you collect this from?        | How will you display this data?                                 |
|------------------------|--------------------------------------------------------|-----------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------------------|
| Total Round Played     | To know what size of data we are dealing with.         | Simulate the game 50 times                                | rounded_played                                           | Histogram: Shows distribution across simulations                |
| Average Estimated Win Rate | To know average win rate and how accurate it is.     | Simulate game 25 times and take estimated win rate         | estimated_winrate                                        | Box Plot + Mean Value                                           |
| Win/Loss Ratio         | To compare bot and player strength                     | Simulate game 25 times and gather both players' data       | total_wins, total_losses                                 | Bar Graph / Stacked Bar                                         |
| Net Chips Gained       | To see how win/loss affects chips gained              | Simulate game 25 times and gather both players' data       | total_chips_win, total_chips_lost                        | Histogram / Violin Plot / Scatter Plot                          |
| Showdown Win Rate      | To understand expectations in showdown                 | Simulate game 25 times and gather both players' data       | showdown_win                                             | Grouped Bar Chart + Table                                       |

#### Statistical Data Revision

| Feature Name              | Graph Objective                                 | Graph Type         | X-axis                | Y-axis           | Statistical Value              |
|--------------------------|--------------------------------------------------|---------------------|------------------------|------------------|--------------------------------|
| Action Distribution       | Show frequency of actions per game stage        | Stacked Bar         | Game Stage             | Frequency        | Frequency Distribution         |
| Win Rate Distribution     | Visualize spread of estimated win rates         | Histogram           | Estimated Win Rate (%) | Frequency        | Distribution Spread, Mean      |
| Winrate by Hand Type      | Show which hands lead to wins                   | Horizontal Bar      | Hand Type              | Win Rate (%)     | Mean Win Rate per Hand Type    |
| Estimated Winrate vs Chips Won | Explore relationship between winrate and chips | Scatter Plot        | Estimated Winrate (%)  | Chips Won        | Correlation/Trend              |
| Winrate vs Fold Rate      | Analyze folding tendencies at various winrates  | Scatter Plot        | Estimated Winrate (%)  | Fold Rate (%)    | Correlation/Trend              |

#### 3.2 Data Recording Method

I’m planning to use CSV files for simplicity. If the data grows larger, I may consider using MongoDB or SQL Server.

#### 3.3 Data Analysis Report

I will analyze data mainly using tables and the five types of graphs listed above.

---

### 4. Project Timeline

| Week         | Task Description                                       |
|--------------|--------------------------------------------------------|
| 1 (10 March) | Proposal submission / Project initiation               |
| 2 (17 March) | Full proposal submission                               |
| 3 (24 March) | Develop base code for all features                     |
| 4 (31 March) | Finish implementing all features                       |
| 5 (7 April)  | Final bug and error checking                           |
| 6 (14 April) | Draft submission week                                  |

#### Continue Planning

| Week              | Task Description                                |
|-------------------|--------------------------------------------------|
| 26 Mar – 2 Apr    | Complete main game logic                         |
| 3 Apr – 9 Apr     | Add missing features and UI elements             |
| 10 Apr – 16 Apr   | Refactor code for clarity and reusability        |
| 17 Apr – 23 Apr   | Check for UI and feature bugs                    |
| 24 Apr – 11 May   | Final prep for submission                        |

---

### 5. Document Version

- **Version**: 3.0  
- **Date**: 31 March 2025  
- **Author**: Munyin Sam (6710545962)

#### Revision History

| Date   | Name     | Comments                                                                 |
|--------|----------|--------------------------------------------------------------------------|
| 14/3   | Rattapoom | Data Analysis report requires explanation on statistical issues. Good job! |
| 16/3   | Parima   | The overall document is clear.                                           |
| 28/3   | Rattapoom | Comments on UML class diagram. Specify which variables are used.         |
| 30/3   | Parima   | UML diagram needs revision.                                              |
