import json

class Piece:
    """A representation of the color of the pieces.
	A piece is Empty if it has not been assigned a color yet. Otherwise it is Black or White.
    """

    Empty = 0
    Black = 1
    White = 2

    @staticmethod
    def serialize(piece):
        if (piece == Piece.Black):
            return 'B'
        if (piece == Piece.White):
            return 'W'
        return ' '

    @staticmethod
    def deserialize(string):
        if (string == 'B'):
            return Piece.Black
        if (string == 'W'):
            return Piece.White
        return Piece.Empty


class Board:
    """A representation of the board.
	Contains a board located in variable board that is filled with 24 empty positions.
	Contains all mill possibilities located in variable lines.
    """

    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [9, 10, 11],
        [12, 13, 14],
        [15, 16, 17],
        [18, 19, 20],
        [21, 22, 23],
        [0, 9, 21],
        [3, 10, 18],
        [6, 11, 15],
        [8, 12, 17],
        [5, 13, 20],
        [2, 14, 23],
        [0, 3, 6],
        [2, 5, 8],
        [15, 18, 21],
        [17, 20, 23],
        [1, 4, 7],
        [16, 19, 22]
    ]

    position_count = 24

    def __init__(self):
        """Constructor for Board.
        Initializes an instance with an empty board."""
        self.board = [Piece.Empty] * self.position_count

    def pieces_of_type_on_board(self, piece):
        """Counts how many of the given piece is on the board.

        Keyword arguments:
        piece -- The piece to count.
        return -- The amount of the given piece that is on the board.
        """
        count = 0
        for piece_in_board in self.board:
            if (piece == piece_in_board):
                count += 1
        return count

    def positions_are_adjacent(self, position, other_position):
        """Checks if the given position and the given other_position are adjacent to each other on the board.

        Keyword arguments:
        position -- The first position.
        other_position -- The second position.
        return -- True if both positions are adjacent to each other. Otherwise False.
        """
        if (position == other_position):
            return False

        lines = self.get_lines_for_position(position)
        for line in lines:
            if (other_position in line):
                if (abs(line.index(position) - line.index(other_position)) == 1):
                    return True

        return False

    def get_lines_for_position(self, position):
        """Looks for which lines the given position can be in.
        It will go through every line to find those who contain the given position.
		It will then return all lines that contains the given position.

        Keyword arguments:
        position -- The position to look for in lines.
        return -- An array of all lines the given position can be in.
        """
        found_lines = []

        for line in self.lines:
            if (position in line):
                found_lines.append(line)

        return found_lines

    def has_three_at_position(self, piece, position):
        """Checks wether the given piece on the given position is in a mill.

        Keyword arguments:
        piece -- The piece to check if it is in a mill.
        position -- The position to look for in possible mills.
        return -- True if the given piece on the given position is in a mill. Otherwise False.
        """
        lines = self.get_lines_for_position(position)
        for line in lines:
            line_full = True
            for position in line:
                if (self.board[position] != piece):
                    line_full = False
                    break
            if (line_full):
                return True

        return False

    def get_mill_at_position(self, piece, position):
        """Returns a line that contains the given position and piece if it is a mill.

        Keyword arguments:
        piece -- The piece to check if it is in a mill.
        position -- The position to look for in possible mills.
        return -- Returns the line that is a mill given the piece and position. Otherwise returns an empty line.
        """
        lines = self.get_lines_for_position(position)
        for line in lines:
            line_full = True
            for position in line:
                if (self.board[position] != piece):
                    line_full = False
                    break
            if (line_full):
                return line

        return []

    def get_other_piece(self, piece):
        """Gets the opposite color of the given piece.
        If the given piece is Piece.Black it will return Piece.White and vice versa. Otherwise it will return Piece.Empty.

        Keyword arguments:
        piece -- The given color to get its opposite color.
        return -- Returns Piece.White if the given piece is Piece.Black and vice versa. Otherwise it will return Piece.Empty.
        """
        if (piece == Piece.Black):
            return Piece.White
        if (piece == Piece.White):
            return Piece.Black
        return Piece.Empty

    def __getitem__(self, index):
        """Gets what is on the given position on the board.

        Keyword arguments:
        index -- An index on the board
        return -- Returns what is on the given index on the board.
        """
        return self.board[index]

    def __setitem__(self, index, value):
        """Updates the board on the given index with the given value.

        Keyword arguments:
        index -- An index on the board to place the given value.
        value -- The value to be placed on the given index on the board.
        return -- Returns nothing. Sets the given value on the given index on the board.
        """
        self.board[index] = value

    def serialize(self):
        array = [' '] * Board.position_count
        for i in range(24):
            array[i] = Piece.serialize(self.board[i])

        return array

    @staticmethod
    def deserialize(array):
        board = Board()
        for i in range(24):
            board[i] = Piece.deserialize(array[i])
                
        return board