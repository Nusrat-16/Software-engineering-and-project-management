from os import path
from .saveGame import *
import sys

def create_game_file():
    create_save_file()

def delete_game_file():
    delete_save_file()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
