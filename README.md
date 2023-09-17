# MCTS-Hex

## Contributors

Luke Schultz <br>
Kamillah Hasham <br>
Zhihong Piao <br>

## Makefile

`make runs`
executes main.py which starts the CLI

## CLI Instructions

| Command | Description | Example |
| --- | --- | --- |
| `x <column><row>` | makes x move at (column, row) | `x a4` |
| `o <column><row>` | makes o move at (column, row) | `o i12` |
| `. <column><row>` | sets board to blank at (column, row) | `. a3` |
| `show` | prints the board | |
| `size <dimension>` | sets the board size, and resets the game | `size 7` |
| `reset`| resets the game | |
| `undo` | undoes previous change to game state | |
| `mcts <player>` | runs Monte Carlo Tree Search to make move for given player | `mcts x` |
| `gameversion <version>` | selects the version of board implementation | `gameversion 2` |
| `mctsversion <version>` | selects the version of mcts implementation | `mctsversion 0` |
