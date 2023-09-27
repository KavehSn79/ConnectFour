# ConnectFour
# Connect Four Game

This is a simple implementation of the classic game Connect Four using Python and Pygame. Connect Four is a two-player connection game in which the players choose a color and take turns dropping one colored disc from the top into a vertically suspended grid. The object of the game is to connect four of one's own discs of the same color next to each other vertically, horizontally, or diagonally before the opponent.

## Dependencies

Before running this game, make sure you have the following dependencies installed:

- Python 3.x
- Pygame library (`pip install pygame`)

## How to Play

1. Run the script in a Python environment.
2. Enter the number of rows and columns for the game board. This determines the size of the grid.
3. Choose a game mode:
   - Player vs. Player (P vs. P)
   - Player vs. AI (P vs. AI)
   - AI vs. AI (AI vs. AI)

### Game Modes

- **Player vs. Player (P vs. P):** Two human players take turns making moves by clicking on the desired column to drop their colored discs. The game ends when one of the players connects four discs or the board is full.

- **Player vs. AI (P vs. AI):** You play against an AI opponent. You take your turn by clicking on the desired column, and the AI uses a minimax algorithm to make its moves. The game ends when either you or the AI connects four discs or the board is full.

- **AI vs. AI (AI vs. AI):** Watch two AI players compete against each other. The game automatically plays out, and you can observe the AI's moves and strategy.

### Winning

The game checks for a winning condition in four ways:

1. Vertical: Four consecutive discs of the same color in a column.
2. Horizontal: Four consecutive discs of the same color in a row.
3. Diagonal (positive slope): Four consecutive discs of the same color diagonally from bottom-left to top-right.
4. Diagonal (negative slope): Four consecutive discs of the same color diagonally from bottom-right to top-left.

The first player to connect four discs wins the game. If the board is full and no one has won, the game is a draw.

## AI Strategy

In the Player vs. AI and AI vs. AI modes, the AI player uses a minimax algorithm with alpha-beta pruning to determine its moves. The AI calculates a score for each possible move and selects the move with the highest score. The scoring considers various factors, including the presence of consecutive pieces and their positions on the board.

## Controls

- In Player vs. Player mode, each player takes turns clicking on a column to drop their disc.
- In Player vs. AI and AI vs. AI modes, the AI makes its moves automatically.
