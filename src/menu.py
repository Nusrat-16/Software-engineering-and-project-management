import os
from .game_platform import Game, CommandLine, Piece
from .game_platform.ai_player import AI_Player
from .communication_platform.communicator import Communicator
from .utils import *

import colorama
import sys

class Menu:
    def __init__(self):
        colorama.init(True)

    def menu(self):
        """Prints out the menu and gets the user's input.
        If the input is 1, it will create and start the game. It will check after every turn if any player has won. If a player has won, it will print who won and the menu again.
        If the input is 2, it will describe how to play the game.
        If the input is 3, it will quit the program.

        Keyword arguments:
        return -- Prints out the menu which the user can choose from.
      """
        clear_screen()
        while True:
            print('### UU-GAME ###')
            print("### You can at all times quit the game by inputting [Q] ###")
            print('1. Play Local')
            print('2. Play Online')
            print('3. How to play')
            print('4. Quit')

            user_input = input('Please enter your choice from the menu and press enter: ')
            if user_input == '1':
                clear_screen()
                print('### LOCAL-GAME ###')
                print('1. Player 1 vs Player 2')
                print('2. Player 1 vs Computer')
                user_input_again = input('Please enter your choice from the menu and press enter: ')
                if user_input_again == '1':
                    game = Game()
                    cmd = CommandLine(game)
                    while (True):

                        cmd.print_board()
                        self.info()
                        cmd.play()

                        if (cmd.game.check_if_piece_won_game(Piece.Black)):
                            cmd.print_board()
                            print("Black has won the game")
                            break
                        if (cmd.game.check_if_piece_won_game(Piece.White)):
                            cmd.print_board()
                            print("White has won the game")
                            break
                elif user_input_again == '2':
                    game = Game()
                    cmd = CommandLine(game)
                    self.ai = AI_Player(game)
                    # Makes sure that its a new game_file every new game against the AI.
                    print('This is where we play against the AI')
                    difficulty = "-1"
                    while difficulty not in ["0", "1", "2"]:
                        difficulty = input("Choose difficulty level (Easy - 0, Medium - 1, Hard - 2): ")
                        
                    # Calls on the funciton that mainly manage the game against the AI.
                    self.play_against_AI(cmd, difficulty)

                    menu_input = input('<- Back to main menu, input 3 and press enter: ')
                    if menu_input == '3':
                        clear_screen()
            elif user_input == '2':
                clear_screen()
                communicator = Communicator()
                communicator.start()
            elif user_input == '3':
                clear_screen()
                game = Game()
                cmd = CommandLine(game)
                cmd.print_board()
                howto_text = f"""
This is preview of the board.
Black players pieces are denoted by {colorama.Fore.MAGENTA}B{colorama.Style.RESET_ALL} and white players pieces are denoted by {colorama.Style.BRIGHT}W{colorama.Style.RESET_ALL}.
The pieces you have not placed yet are represented below the board.

* Both players in the game will have twelve pieces each and have twenty four places to place on the board.
* The player who starts first will always be black.
* The board starts empty and each player will have to place their pieces on the board taking turns.
* You can take your opponents piece out of the board if you have a three in a row.
* Three in a row can be done horizontally, vertically or even diagonally.
* Once all the pieces are placed on the board, each player can move their pieces to adjacent empty places along the lines.
* When a player has three pieces left on the board, the player can move their pieces to any empty place on the board.

A player will win the game if you satisfy any of these two conditions
1. When their opponent’s pieces are reduced to less than three.
2. If you can surround your opponent’s pieces making them unable to move or match three in a row.

The game will end in a draw when the total amount of turns reaches 200.
"""
                print(howto_text)
                menu_input = input('<- Back to main menu, input 1 and press enter: ')
                if menu_input == '1':
                    clear_screen()

            elif user_input == '4':
                self.quit_in_main_menu()

    def quit(self):
        """"
        Gives the user 3 options when quit() is being called in terminal by input [q] or [Q]. The user can quit the
        session by heading back to main menu with inout [M] or [m], quit the complete game in terminal with input
        [q] or [Q] or cancel and head back to the session the user was on before calling for quit by cancelling with
        input [c] or [C].

        Keyword arguments:
        """
        alternatives = ["M", "m", "Q", "q", "C", "c"]
        while True:
            user_input = input("To quit the game insert [Q], to get back to main menu [M] or cancel [C]: ")
            if user_input in alternatives:
                break

        if user_input == 'M' or user_input == 'm':
            clear_screen()
            self.menu()

        elif user_input == 'Q' or user_input == 'q':
            clear_screen()
            sys.exit('You have quited the UU-Game')

        elif user_input == 'C' or user_input == 'c':
            return

    def quit_in_main_menu(self):
        """"
        Gives the user 2 options when they want to quit the game from the main menu. Quit the complete game in terminal
        with input [q] or [Q] or cancel and head back to the main menu with input [c] or [C].

        Keyword arguments:
        """
        alternatives = ["Q", "q", "C", "c"]
        while True:
            user_input = input("To quit the game insert [Q] or cancel [C]: ")
            if user_input in alternatives:
                break

        if user_input == 'Q' or user_input == 'q':
            clear_screen()
            sys.exit('You have quited the UU-Game')

        elif user_input == 'C' or user_input == 'c':
            clear_screen()
            self.menu()

    def info(self):
        """"
        Static print information under the game board to inform the user how to quit the game.
        """
        padding = 25
        reset_code = colorama.Style.RESET_ALL + colorama.Style.DIM
        print(" "*padding + colorama.Fore.YELLOW + "To quit input [Q]" + reset_code)

    def play_against_AI(self, cmd, difficulty):
        """ This function takes in the chosen difficulty level (string) of the
            AI and plays against the AI. It lets both the AI and the Player play
            and translates the moves and updates both the boards between the
            turns. This is the function to call than manage the overall game
            against the AI.
        """
        # Delete save_file
        # Create save_file
        # While loop that checks how long we play
        # Player as Input -> Translate Input -> Save in save_file
        # AI plays -> Read save_file -> Translate output -> Send it in as Player 2
        # If phase 1 call moves_to and check if eliminate
        # If phase 2 call ai_moves_from

        while (True):
            cmd.print_board()
            if (cmd.game.turn == Piece.Black):
               cmd.play()
            else:
                self.ai.the_ai_turn(difficulty)
            result = cmd.game.get_game_winner()

            if (result == Game.WinnerResults.BlackWon):
                cmd.print_board()
                print("Black has won the game")
                break
            if (result == Game.WinnerResults.WhiteWon):
                cmd.print_board()
                print("White has won the game")
                break
            if (result == Game.WinnerResults.Tie):
                cmd.print_board()
                print("It's a draw! Max amount of turns is 200")
                break

