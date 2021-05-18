from os import path
from .AI_hard import run_game_hard
from .AI_medium import run_game_medium
from .AI import run_game_easy
from .saveGame import load_save_file
import sys

def run_AI(difficulty): #Add second argument here with the current gamestate
    data = load_save_file()
    if(int(difficulty) == 0):
        response = run_game_easy(data)
    elif(int(difficulty) == 1):
        response = run_game_medium(data)
    elif(int(difficulty) == 2):
        response = run_game_hard(data)
    else:
        print("Please enter valid difficulty level as an argument: Easy - 0, Medium - 1, Hard - 2")
    
    return response

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        run_AI(sys.argv[1]) 
    else:
        print("Please enter valid difficulty level as an argument: Easy - 0, Medium - 1, Hard - 2")

