from .game import Game
from .board import Piece
from ..utils import *

import colorama
import json
import sys
import os


class CommandLine:
    """Handles the GUI and the user's input. Contains a game in the variable game."""

    def input_number(self, prompt):
        """Checks if the user's given input is an integer. If the user's input is q or Q the program will exit.
          It will keep asking the user for an input until it is valid.

          Keyword arguments:
          prompt -- The message to be printed to the user.
          return -- Exits the program if the user's input is q or Q. Otherwise the users input if it is an integer.
        """
        while True:
            result = input(prompt)
            if (result == 'q' or result == 'Q'):
                self.quit()
            if result.isdigit():
                return int(result)

    def input_number_or_other(self, prompt, other):
        """Checks if the user's given input is an integer or inside other. If the user's input is q or Q the program will exit.
        It will keep asking the user for an input until it is valid.

        Keyword arguments:
        prompt -- The message to be printed to the user.
        other -- Array of other allowed inputs
        return -- Exits the program if the user's input is q or Q. Otherwise the users input if it is an integer.
        """
        while True:
            result = input(prompt)
            if (result == 'q' or result == 'Q'):
                sys.exit()
            if result.isdigit():
                return int(result)
            if (result in other):
                return result

    def __init__(self, game):
        """A commandline that plays a certain game"""
        self.game = game

    def print_board(self):
        """Prints the board and the pieces on the board. It also prints how many pieces each player has.

          Keyword arguments:
          return -- Prints out the board.
        """
        board = [""] * 24

        reset_code = colorama.Style.RESET_ALL + colorama.Style.DIM
        black_piece = colorama.Fore.MAGENTA + 'B' + reset_code
        white_piece = colorama.Style.BRIGHT + 'W' + reset_code

        for x in range(24):
            if (self.game.board[x] == Piece.Empty):
                board[x] = ' '
            elif (self.game.board[x] == Piece.Black):
                board[x] = black_piece
            else:
                board[x] = white_piece

        clear_screen()

        board_text = """
1                            2                             3
  A-----------------------------C-----------------------------D
  |)                            |                           / |
  |  )                          |                         /   |
  |    )                        |                       /     |
  |      ) 4                  5 |                   6 /       |
  |        E--------------------F--------------------G        |
  |        | )                  |                 /  |        |
  |        |   )                |               /    |        |
  |        |     )              |             /      |        |
  |        |       ) 7        8 |         9 /        |        |
  |        |         H----------I----------J         |        |
  |        |         |                     |         |        |
  |        |         |                     |         |        |
10|     11 |      12 |                  13 |      14 |     15 |
  K--------L---------M                     N---------O--------P
  |        |         |                     |         |        |
  |        |      16 |         17       18 |         |        |
  |        |         Q----------R----------S         |        |
  |        |       /            |            )       |        |
  |        |     /              |              )     |        |
  |        |   /                |                )   |        |
  |     19 | /               20 |                  ) | 21     |
  |        T--------------------U--------------------V        |
  |      /                      |                      )      |
  |    /                        |                        )    |
  |  /                          |                          )  |
22|/                         23 |                          24)|
  X-----------------------------Y-----------------------------Z  """

        # So the preview looks nice, use ] instead of \\ to make the size match
        board_text = board_text.replace(")", "\\")

        # replace characters with board pieces
        board_positions = "ACDEFGHIJKLMNOPQRSTUVXYZ"

        # replace in two steps, because color codes include characters that might be replaced otherwise
        for i in range(24):
            board_text = board_text.replace(board_positions[i], "pos_" + board_positions[i])

        # replace numbers, also in two steps...
        for i in range(10):
            board_text = board_text.replace(str(i), "num_" + str(i))

        for i in range(24):
            board_text = board_text.replace("pos_" + board_positions[i], board[i])

        for i in range(10):
            board_text = board_text.replace("num_" + str(i), colorama.Fore.YELLOW + str(i) + reset_code)

        print(board_text)

        # if (self.game.state == Game.GameState.Placing):
        # print("Pieces left                Black: " + str(self.game.players[0].pieces_amount) + "                White: " + str(self.game.players[1].pieces_amount))
        pieces_presentation = [' '] * 63
        for i in range(self.game.players[0].pieces_amount):
            pieces_presentation[i] = black_piece
        for i in range(self.game.players[1].pieces_amount):
            pieces_presentation[62 - i] = white_piece
        print("".join(pieces_presentation))

    def identify_piece(self, turn):
        """ Identifies which player's turn it is.

          Keyword arguments:
          turn -- The current turn of the game.
          return -- Returns Black if the given turn is 1 or White if the given turn is 2.
        """
        if turn == 1:
            return 'Black'
        if turn == 2:
            return 'White'

    def eliminate(self):
        """Gets the user's input on which opponent piece it wants to eliminate when the user has created a mill.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid opponent piece, the opponent piece will be removed.
        Prints out different messages depending on the user's input and updates the board accordingly.

        Keyword arguments:
      """
        self.print_board()
        print(self.identify_piece(self.game.turn) + ' player has three in a row!')

        while True:
            position = self.input_number('Choose a piece to eliminate: ') - 1
            result = self.game.can_eliminate_piece(position)
            if result == Game.CanElimateResults.Ok:
                self.game.eliminate_piece(position)
                player = self.game.get_player_from_piece(self.game.turn)
                player.previous_move[2] = position
                break
            elif result == Game.CanElimateResults.NoPiece:
                print("No piece at that position.")
            elif result == Game.CanElimateResults.TargetAreThrees:
                print("Target are threes and can not be removed.")
            elif result == Game.CanElimateResults.WrongPiece:
                print("You can't eliminate your own piece")
            elif result == Game.CanElimateResults.OutsideBoard:
                print("Position is outside the board")
            else:
                print("Something went wrong")



    def place(self):
        """Ask the user for input on where to place, and then places there.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid position, a piece will be placed.

        Keyword arguments:
        """
        print('Its ' + self.identify_piece(self.game.turn) + ' player\'s turn to play')
        while True:
            position = self.input_number('Choose a spot to place: ') - 1

            result = self.game.can_place_piece(self.game.turn, position)
            if result == Game.CanPlaceResults.Ok:
                self.game.place_piece(self.game.turn, position)
                player = self.game.get_player_from_piece(self.game.turn)
                player.previous_move[1] = position
                break
            elif result == Game.CanPlaceResults.Occupied:
                print("There is already something at this position.")
            elif result == Game.CanPlaceResults.WrongPiece:
                print("Wrong turn (this shouldn't be possible to happen).")
            elif result == Game.CanPlaceResults.WrongState:
                print("Placing is not allowed at this time (this shouldn't be possible to happen).")
                return  # Safety return here. Wrong state means no placement can happen
            elif result == Game.CanPlaceResults.OutsideBoard:
                print("Position is outside the board.")
            else:
                print("Something went wrong.")

    def move(self):
        """Gets the user's input on where to move.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid position, a piece will be moved.

        Keyword arguments:
        """
        print('Its ' + self.identify_piece(self.game.turn) + ' player\'s turn to play')
        while True:
            position = self.input_number('Which piece would you like to move?: ') - 1

            result = self.game.can_move_piece_from(position)

            if (result == Game.CanMoveResults.Ok):
                valid_moves = self.game.get_valid_moves_from_position(position)
                str_valid_moves = [str(valid_move + 1) for valid_move in valid_moves]
                query = "To what position would you like to move? (" + ", ".join(str_valid_moves) + " or \"back\"): "
                new_position = self.input_number_or_other(query, ["b", "B", "back", "Back"])
                if (isinstance(new_position, int)):
                    new_position -= 1
                    result = self.game.can_move_piece(position, new_position)
                else:
                    continue

            if result == Game.CanMoveResults.Ok:
                self.game.move_piece(position, new_position)
                player = self.game.get_player_from_piece(self.game.turn)
                player.previous_move[0] = position
                player.previous_move[1] = new_position
                break
            elif result == Game.CanMoveResults.WrongPiece:
                print("Can't move opponents/empty piece.")
            elif result == Game.CanMoveResults.SamePosition:
                print("Can't move to same position")
            elif result == Game.CanMoveResults.OutsideBoard:
                print("Position is outside the board.")
            elif result == Game.CanMoveResults.NotAdjacent:
                print("The positions are not nearby.")
            elif result == Game.CanMoveResults.NewPositionOccupied:
                print("The new position is occupied.")
            elif result == Game.CanMoveResults.WrongState:
                print("Moving pieces are not allowed at this time (this shouldn't be possible to happen).")
                return  # Safety return here. Wrong state means no moving can happen
            else:
                print("Something went wrong.")


    def play(self):
        """It checks first which game state the game is in. If the game state is on state Placing then it will ask the user which position it wants to place its piece.
          Depending on the user's input, different messages will be printed out. If the user places a piece on which it creates a mill, the user will be asked which
          opponent piece it wants to eliminate. If the game state is on s1
          tate Moving then it will ask the user which one of its pieces it wants to move. Depending on the
          user's input, different messages will be printed out. If the user moves its piece on another valid position which it creates a mill, the user will be
          asked which opponent piece it wants to eliminate.

          Keyword arguments:
          return -- Prints out different messages depending on the user's input and updates the board accordingly.
        """
        if self.game.state == Game.GameStage.Placing:
            self.place()
            if self.game.eliminating:
                self.eliminate()
        elif self.game.state == Game.GameStage.Moving:
            self.move()
            if self.game.eliminating:
                self.eliminate()
