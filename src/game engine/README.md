# Extreme Three-in-a-Row

This program required Python3 to run.

The game requires a game file which the player manually updates when they want to make a move. Create a new game file through the following command (can also be used to overwrite an old game file):
```bash
python3 manage_game.py create_game_file
```
This will create the file save_file.json

To delete an old game file:
```bash
python3 manage_game.py delete_game_file
```

To have the AI make a move:

```bash
python3 run_AI.py x
```
where x is replaced by desired difficulty (0 - easy, 1 - medium and 2- hard)

To make a move in phase 1 the player manually replaces an empty spot ('-') with the players marker ('X') in the map object in save_file.json. The player also has to manually update 'player_markers_left' in the data object (subtract by one when a marker is placed). 

To make a move in phase 2 the player manually replaces an empty spot ('-') (adjacent to one of their own markers) with the players marker ('X') in the map object in save_file.json.

To make a move in phase 2 the player manually replaces any empty spot ('-') with the players marker ('X') in the map object in save_file.json.

If the player constructs a three-in-a-row with their markers they manually replace any AI marker ('O') with an empty marker ('-').
