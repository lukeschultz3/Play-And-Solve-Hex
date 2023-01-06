# MCTS-Hex

The Makefile target
`make runs`
executes main.py which starts the CLI

## CLI Instructions
| Command | Description | Example |
| --- | --- | --- |
| `x <x coord> <y coord>` | makes x move at (x, y) | `x 3 5` |
| `o <x coord> <y coord>` | makes o move at (x, y) | `o 2 0` |
| `show` | prints the board | |
| `size <dimention>` | sets the board size, and resets the game | `size 7` |
| `reset`| resets the game | |
| `mcts <player>` | runs Monte Carlo Tree Search to make move for given player | `mcts x` |