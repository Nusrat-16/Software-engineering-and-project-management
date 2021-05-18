from .board import Board, Piece
from .player import Player

class Game:
    """A representation of the game and its rules.
    Contains a board located in the board variable.
    Contains players located in an array inside the players variable.
    Contains the current turn located in the turn variable.
    Contains the total amount of turns that has been played in the game in the total_turns variable.
    """

    class GameStage:
        Placing = 1
        Moving = 2

    def __init__(self, player_piece_count = 12):
        """Constructor for Game.
        Initializes a game with all variables and an empty board where it's blacks turn to play.
        """
        self.turn = Piece.Black
        self.board = Board()
        self.players = [Player(Piece.Black, player_piece_count), Player(Piece.White, player_piece_count)]
        self.state = Game.GameStage.Placing
        self.eliminating = 0
        self.ai_eliminated = 0
        self.total_turns = 0

    def get_player_from_piece(self, piece):
        """Gets the player belong to a piece

        Keyword arguments:
        piece -- the piece to check
        return -- the player belonging to the piece, or None if invalid piece
        """
        if (piece == Piece.Black):
            return self.players[0]
        if (piece == Piece.White):
            return self.players[1]
        return None

    class WinnerResults:
        GameInProgress = 1
        Tie = 2
        BlackWon = 3
        WhiteWon = 4
    def get_game_winner(self):
        """Gets a WinnerResults if there is one with the winner of the game, if there is one.
        Returns GameInProgress if the game is currently being played.
        Returns Tie if the game ended in a draw.
        Returns BlackWon if black won the game.
        Returns WhiteWon if white won the game.
        return -- WinnerResults with the game win state
        """
        if (self.check_if_tie()):
            return Game.WinnerResults.Tie
        if (self.check_if_piece_won_game(Piece.Black)):
            return Game.WinnerResults.BlackWon
        if (self.check_if_piece_won_game(Piece.White)):
            return Game.WinnerResults.WhiteWon

        return Game.WinnerResults.GameInProgress

    def check_if_piece_won_game(self, piece):
        """"Checks if the given piece has won the game

        Keyword arguments:
        piece -- the piece to check
        return -- True if the given piece has won, otherwise False
        """
        def check_if_piece_lost_game(self, piece):
            if (self.state == Game.GameStage.Placing):
                return False
            # Cant lose if it's the others piece's turn
            if (self.turn != piece):
                return False
            if (self.board.pieces_of_type_on_board(piece) <= 2):
                return True
            for position in range(Board.position_count):
                if (self.board[position] != piece):
                    continue
                for new_position in range(Board.position_count):
                    if (self.can_move_piece(position, new_position, True) == Game.CanMoveResults.Ok):
                        return False
            return True
        return check_if_piece_lost_game(self, self.board.get_other_piece(piece))


    def check_if_mill_is_ok(self, piece, position):
        """ Checks if the mill counts as a new mill

        Keyword arguments:
        piece -- the pieces who moved
        position -- the position the piece moved
        return -- True if the mill counts as a new one
        """
        player = self.get_player_from_piece(piece)
        if player.latest_mill[position] < 2:
            return False
        return True


    def check_if_tie(self):
        """"Checks if the total amount of turns has exceeded 200 turns which ends the game in a tie.

        Keyword arguments:
        return -- True if the game is a tie, otherwise False.
        """
        if(self.total_turns < 200):
            return False
        else: return True


    class PlaceResults:
        Failed = -1
        Placed = 1
        GotThree = 2
    def place_piece(self, piece, position):
        """Places a piece at the given location.
        If the placement was invalid it will return PlaceResults.Failed.
        If the placement resulted in a three it will return PlaceResults.GotThree.
        Otherwise it will return PlaceResults.Placed and increase total_turns by 1.

        Keyword arguments:
        piece -- the piece to place
        return -- a PlaceResults result
        """
        if (self.can_place_piece(piece, position) != self.CanPlaceResults.Ok):
            return self.PlaceResults.Failed

        self.board[position] = piece
        player = self.get_player_from_piece(self.turn)
        player.pieces_amount -= 1
        player.increase_position_move_count()

        if (self.players[0].pieces_amount == 0 and self.players[1].pieces_amount == 0):
            self.state = self.GameStage.Moving

        if (self.board.has_three_at_position(piece, position)):
            player.latest_created_mill = self.board.get_mill_at_position(piece, position)
            self.eliminating = True
            return self.PlaceResults.GotThree
        self.turn = self.board.get_other_piece(self.turn)
        self.total_turns = self.total_turns + 1
        return self.PlaceResults.Placed

    class CanPlaceResults:
        Ok = 1
        Occupied = -1
        WrongPiece = -2
        WrongState = -3
        OutsideBoard = -4
    def can_place_piece(self, piece, position):
        """ Checks wether the given position on board is valid to place piece.
        Returns a CanPlaceResults describing which condition did not hold or if position is valid.

        Returns Occupied if the given position is already occupied on the board.
        Returns WrongPiece if the given piece does not match with current turn.
        Returns WrongState if the current state is eliminating, which the player can not place a piece atm.
        Returns OutsideBoard if the given position is outside board.
        Otherwise it will return Ok and the player can place the piece in the given position.

        Keyword arguments:
        piece -- the piece to be placed on board
        position -- position on the board where the piece will be placed
        return -- A CanPlaceResults result
        """
        if (position < 0 or position >= Board.position_count):
            return self.CanPlaceResults.OutsideBoard
        if (self.turn != piece):
            return self.CanPlaceResults.WrongPiece
        if (self.board[position] != Piece.Empty):
            return self.CanPlaceResults.Occupied
        if (self.eliminating):
            return self.CanPlaceResults.WrongState
        return self.CanPlaceResults.Ok

    def eliminate_piece(self, position):
        """ Eliminates the piece on the given position and sets eliminating state to False.
        Returns False if the piece on the given position can not be eliminated.
        Otherwise returns True if the piece on the given position can be eliminated

        Keyword arguments:
        position -- position of a piece on the board to be eliminated
        return -- True if piece on the given position can be eliminated, otherwise False.
        """
        if (self.can_eliminate_piece(position) != self.CanElimateResults.Ok):
           return False
        self.board[position] = Piece.Empty
        self.eliminating = False
        self.ai_eliminated = True
        self.total_turns = self.total_turns + 1
        self.turn = self.board.get_other_piece(self.turn)

        return True
    class CanElimateResults:
        Ok = 1
        NoPiece = -1
        TargetAreThrees = -2
        WrongPiece = -3
        WrongState = -4
        OutsideBoard = -5
    def can_eliminate_piece(self, position):
        """Checks if a piece can be eliminated
        Returns Ok when it is ok to eliminate the piece
        Returns NoPiece when there is no piece to eliminate at that has_three_at_position
        Returns TargetAreThrees when the target is part of a threes and can not be eliminated
        Returns WrongPiece when the target do not belong to the opponent and can not be eliminated
        Returns WrongState when it is not time to eliminate a piece
        Returns OutsideBoard when the target is outside the board and can not be eliminated

        Keyword arguments:
        position -- The position to check
        """
        if (position < 0 or position >= Board.position_count):
            return self.CanElimateResults.OutsideBoard
        if (self.board[position] == Piece.Empty):
            return self.CanElimateResults.NoPiece
        if (self.board[position] == self.turn):
            return self.CanElimateResults.WrongPiece
        if (self.eliminating == False):
            return self.CanElimateResults.WrongState

        # If all opponent pieces are three, we can elimate anything
        opponent_piece = self.board.get_other_piece(self.turn)
        all_are_threes = True
        for check_position in range(24):
            if (self.board[check_position] == opponent_piece):
                if (self.board.has_three_at_position(opponent_piece, check_position) == False):
                    all_are_threes = False
                    break

        if (all_are_threes == False):
            if (self.board.has_three_at_position(opponent_piece, position)):
                return self.CanElimateResults.TargetAreThrees

        return self.CanElimateResults.Ok


    class MoveResults:
        Ok = 1
        GotThree = 2
        Failed = -1
    def move_piece(self, position, new_position):
        """Moves a piece from a position to another.
        Returns a MoveResults containing information about the move.
        Returns Ok if the move was successful and increase total_turns by 1.
        Returns GotThree if the resulting move resulted in threes.
        Returns Failed if the move was invalid.

        Keyword arguments:
        position -- the position we move from
        new_position -- the position we move to
        return -- a MoveResults result
        """
        if (self.can_move_piece(position, new_position) != self.CanMoveResults.Ok):
            return self.MoveResults.Failed
        piece_at_old_position = self.board[position]

        player = self.get_player_from_piece(piece_at_old_position)
        if (self.board.has_three_at_position(piece_at_old_position, position)):
            player.latest_mill[position] = 0

        player.increase_position_move_count()
        self.board[position] = Piece.Empty
        self.board[new_position] = piece_at_old_position


        if (self.board.has_three_at_position(piece_at_old_position, new_position)):
            self.eliminating = True
            player.latest_move_from = position
            player.latest_move_to = new_position
            return self.MoveResults.GotThree

        self.turn = self.board.get_other_piece(self.turn)
        self.total_turns = self.total_turns + 1
        player.latest_move_from = position
        player.latest_move_to = new_position
        return self.MoveResults.Ok

    class CanMoveResults:
        Ok = 1
        WrongPiece = -1
        SamePosition = -2
        OutsideBoard = -3
        NotAdjacent = -4
        NewPositionOccupied = -5,
        OldMillAtPosition = -6,
        WrongState = -7
    def can_move_piece_from(self, position, ignore_turn = False):
        """Checks if a piece at a position can be moved from the given position.
        Returns a CanMoveResults containing information about the move.
        Returns Ok if the move was successful.
        Returns WrongPiece if the piece was not associated with the current turn.
        Returns OutSideBoard if the position was outside the board.
        Returns WrongState if the game is not in a movement state

        Keyword arguments:
        position -- the position we move from
        ignore_turn -- optional argument, defaults to False. If true it will ignore the turn check
        return -- a CanMoveResult result that shows how to implement
        """
        if (position < 0 or position >= Board.position_count):
            return Game.CanMoveResults.OutsideBoard
        if (ignore_turn == False and self.turn != self.board[position]):
            return Game.CanMoveResults.WrongPiece
        if (self.state != Game.GameStage.Moving):
            return Game.CanMoveResults.WrongState

        return Game.CanMoveResults.Ok


    def can_move_piece(self, position, new_position, ignore_turn = False):
        """Checks if a piece at a position can be moved to the given position.
        Returns a CanMoveResults containing information about the move.
        Returns Ok if the move was successful.
        Returns WrongPiece if the piece was not associated with the current turn.
        Returns SamePosition if the position and the new position are the same.
        Returns OutSideBoard if any position was outside the board.
        Returns NotAdjacent if the two positions are not adjacent and adjacent movements are required.
        Returns NewPositionOccupied if there's already a piece at the target location.
        Returns WrongState if the game is not in a movement state
        Returns RecreateBrokenMill if the player moves back the same piece to the mill it broke the previous turn.

        Keyword arguments:
        position -- the position we move from
        new_position -- the position we move to
        ignore_turn -- optional argument, defaults to False. If true it will ignore the turn check
        return -- a CanMoveResult result
        """

        can_move_from_result = self.can_move_piece_from(position, ignore_turn)
        if (can_move_from_result != Game.CanMoveResults.Ok):
            return can_move_from_result
        if (new_position < 0 or new_position > Board.position_count):
            return Game.CanMoveResults.OutsideBoard
        if (position == new_position):
            return Game.CanMoveResults.SamePosition
        if (self.board[new_position] != Piece.Empty):
            return Game.CanMoveResults.NewPositionOccupied
        if (self.check_if_mill_is_ok(self.board[position], new_position) == False):
            return Game.CanMoveResults.OldMillAtPosition

        


        moved_piece = self.board[position]
        total_on_board = self.board.pieces_of_type_on_board(moved_piece)
        # If you have three pieces left you're allowed to fly so the adjacent rule doesn't apply
        if (total_on_board > 3):
            if (self.board.positions_are_adjacent(position, new_position) == False):
                return Game.CanMoveResults.NotAdjacent

        return Game.CanMoveResults.Ok


    def get_valid_moves_from_position(self, position, ignore_turn = False):
        """Gets a list of valid moves from a position

        Keyword arguments:
        position -- the position we move from
        ignore_turn -- optional argument, defaults to False. If true it will ignore the turn check
        return -- a list of positions we can move
        """
        valid_moves = []
        for i in range(Board.position_count):
            if (self.can_move_piece(position, i, ignore_turn) == Game.CanMoveResults.Ok):
                valid_moves.append(i)
        return valid_moves


    def serialize(self):

        players_json = [self.players[0].serialize(), self.players[1].serialize()]

        json = {
            "board": self.board.serialize(),
            "turn": Piece.serialize(self.turn),
            "stage": "placing" if self.state == Game.GameStage.Placing else "moving",
            "eliminating": self.eliminating,
            "total_turns": self.total_turns,
            "players": players_json
        }
        return json

    @staticmethod
    def deserialize(json_object):
        game = Game()
        game.board = Board.deserialize(json_object["board"])
        game.turn = Piece.deserialize(json_object["turn"])
        game.state = Game.GameStage.Placing if json_object["stage"] == "placing" else Game.GameStage.Moving
        game.eliminating = json_object["eliminating"]
        game.total_turns = json_object["total_turns"]
        game.players[0] = Player.deserialize(json_object["players"][0])
        game.players[1] = Player.deserialize(json_object["players"][1])


        return game