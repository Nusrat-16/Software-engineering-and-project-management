from .classes import *
from .saveGame import *
from random import choice
from copy import deepcopy
from math import inf
import sys
# Defining constant values.
PLAYER = 'X'
AI = 'O'
EMPTY = '-'

def undo_move(gamestate, move, prev, phase):
    if (phase == 1):
        move.owner = EMPTY
        gamestate.AI.previous_move = prev
    raise NotImplementedError('this function was replaced, and should not be used.')

def update_markers_on_board_numbers(gamestate):
    '''
        Function that updates how many markers player/ai has on the board currently.
        It simply uses the function get_possible_nodes to get a list of the nodes beloning
        to either player, checks the length of that list and updates the gamestates values.
    '''
    gamestate.AI.markers_on_board = len(get_possible_nodes(gamestate, AI))
    gamestate.player.markers_on_board = len(get_possible_nodes(gamestate, PLAYER))

def change_owner(gamestate, chosen_node, target):
    '''
        Function that changes the chosen nodes owner to the specified target.

        Due to the way minmax is implemented this function is needed for changing a given nodes owner.
        If this function is not used, the node will probably be changed on another gamestate instance -
        this will make the game unplayable.
    '''
    for line in gamestate.gameboard.lines:
            for node in line.nodes:
                if (chosen_node.get_node_label() == node.get_node_label()):
                    node.owner = target

def make_move(gamestate, chosen_node, phase, real):
    '''
        Function that takes in a single node, in phase one, and a pair of nodes in phases 2/3.
        Takes nodes and places or moves a piece there depending on phase.
        Includes real argument which is a flag for when to actually make a move and when function
        is used in min-max recursion (for debugging).
        Returns True if move was made, as well as opponent node removed if any. Returns False and None if move failed
    '''
    # Phase 1 move.
    if(phase == 1):
        # Given move gets placed by changing the owner of the given node.
        change_owner(gamestate, chosen_node, AI)
        # Updates the gamestate for the AI.
        gamestate.player.markers_left_to_play -= 1
        gamestate.AI.markers_left_to_play -= 1
        gamestate.AI.markers_on_board += 1
        # Checks three-in-a-row.
        removed = None
        if (check_three_in_a_row(gamestate, chosen_node, AI)):
            gamestate.AI.previous_move[2] = True
        else:
            gamestate.AI.previous_move[2] = False
        if (check_three_in_a_row(gamestate, chosen_node, AI)):

            # If we find one, remove an opponent piece.
            removed = remove_opponent_piece(gamestate, real)

        return True, removed

    # Phase 2 or 3 move.
    if(phase != 1):
        # Node source and destination are paired in a dict: {source : dest}
        # so they are unpacked.

        removed = None
        for node_from, node_to in chosen_node.items():
            # Check if the move can be made.
            if(check_legal_move(gamestate, node_from, node_to, real)):
                # Updating gamestate for checking if illegal move next turn.
                gamestate.AI.previous_move[0] = node_from.get_node_label()
                gamestate.AI.previous_move[1] = node_to.get_node_label()
                if (check_three_in_a_row(gamestate, node_from, AI)):
                    gamestate.AI.previous_move[2] = True
                else:
                    gamestate.AI.previous_move[2] = False
                # Actual updating of nodes happens here.
                change_owner(gamestate, node_from, EMPTY)
                change_owner(gamestate, node_to, AI)
                # Checking.
                if (check_three_in_a_row(gamestate, node_to, AI)):
                    removed = remove_opponent_piece(gamestate, real)
                return True, removed
            else:
                return False, None

def make_opponent_move(gamestate, chosen_node, phase):
    '''
        Function that works the same as make_move except is used in minmax to
        check the opponent's best move in a future turn.
    '''
    # Phase 1 move.
    if(phase == 1):
        # Given move gets placed by changing the owner of the given node.
        change_owner(gamestate, chosen_node, PLAYER)
        # Updates the gamestate for the AI.
        gamestate.player.markers_left_to_play -= 1
        gamestate.player.markers_on_board += 1
        # Checks three-in-a-row.
        if (check_three_in_a_row(gamestate, chosen_node, PLAYER)):
            remove_AI_piece(gamestate)
        return True

    if(phase != 1):
        # Node source and destination are paired in a dict: {source : dest}
        # so they are unpacked.
        for node_from, node_to in chosen_node.items():
            # Check if the move can be made.
            if(check_legal_move(gamestate, node_from, node_to, False)):
                # Actual updating of nodes happens here.
                change_owner(gamestate, node_from, EMPTY)
                change_owner(gamestate, node_to, PLAYER)
                # Updating gamestate for checking if illegal move next turn.
                gamestate.AI.previous_move[0] = node_from.get_node_label()
                gamestate.AI.previous_move[1] = node_to.get_node_label()
                if (check_three_in_a_row(gamestate, node_from, PLAYER)):
                    gamestate.AI.previous_move[2] = True
                else:
                    gamestate.AI.previous_move[2] = False

                if (check_three_in_a_row(gamestate, node_to, PLAYER)):
                    remove_AI_piece(gamestate)
                    # removed =
                return True
            else:
                return False


def check_legal_move(gamestate, node_from, node_to, real):
    '''
    Checks that AI doesn't move back to a three-in-a-row from another three-in-a-row.
    Returns True if valid move, and False otherwise
    '''
    if(check_three_in_a_row(gamestate, node_from, AI) and (gamestate.AI.previous_move[2] == True) and (node_to.get_node_label() == gamestate.AI.previous_move[0])):
        return False
    else:
        return True


def get_possible_nodes(gamestate, target):
    '''
        Function that checks the gamestate
        and returns the nodes that are target.
    '''

    possible = []
    # Iterates through the lines ...
    for line in gamestate.gameboard.lines:
        # and the nodes in the lines ...
        for node in line.nodes:
            # to see if the owner is our target and if we haven't seen it before.
            if (node.owner == target and node not in possible):
                # Add to our list.
                possible.append(node)
    return possible

def check_three_in_a_row(gamestate, the_node, target):
    '''
    Checks if the target has gotten three pieces in a row.
    ----------
    Parameters
    ----------
    gamestate:
        a gamestate object containing the AI, PLAYER and gameboard
    the_node:
        the node to check if it contributes to three in a row
    target:
        Can either be AI or PLAYER
    ----------
    Returns:
        True if the target has gotten three in a row, else false.
    '''
    for line in gamestate.gameboard.lines:
        for node in line.nodes:
            if (the_node.get_node_label() == node.get_node_label()):
                if (all_nodes_in_line_belongs_to_target(gamestate, line, target)):
                    return True
    return False

def all_nodes_in_line_belongs_to_target(gamestate, line, target):
    '''
    Checks if all three markers in a line belongs to the target.
    ----------
    Parameters
    ----------
    gamestate:
        a gamestate object containing the gamestate
    line:
        A line containing three nodes
    target:
        Can either be AI or PLAYER
    ----------
    Returns:
        True if the target has won
        , else false.
    '''

    for node in line.nodes:
        if(node.owner != target):
            return False
    return True

def removal_node_in_row(gamestate, node_to_remove, target):
    '''
    Checks if the node to remove is part of a three in a row
    ----------
    gamestate:
        a gamestate object containing the AI, PLAYER and gameboard
    '''
    if(check_three_in_a_row(gamestate, node_to_remove, target)):
        return True
    else:
        return False


def remove_opponent_piece(gamestate, real):
    '''
    Removes one of the PLAYERs pieces from the board.
    ----------
    gamestate:
        a gamestate object containing the AI, PLAYER and gameboard.
    real:
        a flag for debugging puropses which indicates if the function
        is used in minmax recursion.
    ----------
    Returns:
        Name of opponent node removed, and None if removal failed
    '''
    opponent_nodes = get_possible_nodes(gamestate, PLAYER)
    if (len(opponent_nodes) > 0):
        chosen_node = choice(opponent_nodes)
        nodes_checked = 0
        while(nodes_checked <= len(opponent_nodes) and (removal_node_in_row(gamestate, chosen_node, PLAYER))):
            nodes_checked += 1
            chosen_node = choice(opponent_nodes)
        if (real):
            pass
        for line in gamestate.gameboard.lines:
            for node in line.nodes:
                if ((node.get_node_label() == chosen_node.get_node_label()) and (node.owner == PLAYER)):
                    change_owner(gamestate, node, EMPTY)
                    gamestate.AI.previous_move[3] = node.get_node_label()
                    gamestate.player.markers_on_board -= 1
                    return node.get_node_label()
    else:
        return None


def remove_AI_piece(gamestate):
    '''
    Removes one of the AIs pieces from the board.
    ----------
    gamestate:
        a gamestate object containing the AI, PLAYER and gameboard

    This function is used in the minmax recursion when it is in a minimizing turn
    after the minimizing actor gets a three-in-a-row and removes an AI piece.
    '''
    opponent_nodes = get_possible_nodes(gamestate, AI)
    if (len(opponent_nodes) > 0):
        chosen_node = choice(opponent_nodes)
        nodes_checked = 0
        while(nodes_checked <= len(opponent_nodes) and (removal_node_in_row(gamestate, chosen_node, AI))):
            nodes_checked += 1
            chosen_node = choice(opponent_nodes)

        for line in gamestate.gameboard.lines:
            for node in line.nodes:
                if ((node.get_node_label() == chosen_node.get_node_label()) and (node.owner == AI)):
                    change_owner(gamestate, node, EMPTY)
                    gamestate.AI.markers_on_board -= 1
                    return True
    else:
        return False


def get_neighbours(gamestate, node_list):
    '''
        Function that takes the gamestate and a target node
        and looks at the gamestates lines to find the surrounding
        nodes and returns them in a list.
    '''
    if(not isinstance(node_list, list)):
        node_list = [node_list]
    neighbours = {}
    for node in node_list:
        neighbours[node] = []
        for line in gamestate.gameboard.lines:
            '''
                Compares node labels instead of instances since nodes belong to different
                gamestates most of the time. Matching with labels makes sure that the
                conditionals work even though the nodes are different.
                (if comparing node1 == node2 the result is always False, since they are not the
                exact same)
            '''
            if (line.nodes[0].get_node_label()) == node.get_node_label():
                neighbours[node].append(line.nodes[1])
            elif (line.nodes[1].get_node_label()) == node.get_node_label():
                neighbours[node].append(line.nodes[0])
                neighbours[node].append(line.nodes[2])

            elif (line.nodes[2].get_node_label()) == node.get_node_label():
                neighbours[node].append(line.nodes[1])
    return neighbours

def winning_check(gamestate, target):
    '''
    Checks if the target has won
    ----------
    Parameters
    ----------
    gamestate:
        a gamestate object containing the gamestate
    target:
        Can either be AI or PLAYER
    ----------
    Returns:
        True if opponent has no markers left to play
        and less than 3 markers on the board, else false
    '''

    if(target == AI):
        if (gamestate.player.markers_left_to_play == 0):
            if (gamestate.player.markers_on_board <= 2):
                return True
    elif(target == PLAYER):
        if (gamestate.AI.markers_left_to_play == 0):
            if (gamestate.AI.markers_on_board <= 2):
                return True
    return False


def node_to_piece(node_list):
    '''
    Function that takes a list of nodes (possibly a list containing only one node)
    and returns the corresponding owners of sAId nodes in a list of the same order
    as the passed list.

    This is not in use.
    '''
    raise NotImplementedError('this function is outdated and should not be used.')
    pieces = []
    for node in node_list:
        piece = node.owner
        pieces.append(piece)

    return pieces

def get_all_possible_moves(gamestate, phase, target):
    '''
    ----------
    Parameters
    ----------
    gamestate:
        a gamestate object containing the gamestate.
    phase:
        the phase in which to move.
    target:
        Can either be AI or PLAYER.
    ----------
    Returns:
        Phase 1: A list of nodes which an actor can move to.
        Phase 2: A list of possible Node pairs {source : dest}.
    '''
    if(phase == 1):
        # Any empty node is a possible destination in phase 1.
        return get_possible_nodes(gamestate, EMPTY)
    if(phase == 2):
        '''
            In phase 2 we find all nodes where the actor has nodes and then
            find all the adjacent nodes.
            For each possible node: if an adjacent node is empty, it is a possible destination and the
            possible node and its neighbour are paired {possible node : neighbour}
        '''
        possible_nodes = get_possible_nodes(gamestate, target)
        neighbours = get_neighbours(gamestate, possible_nodes)
        possible_neighbours = []
        for n in possible_nodes:
            for neighbour in neighbours[n]:
                if(neighbour.owner == EMPTY):
                    possible_neighbours.append({n : neighbour})

        return possible_neighbours
    if(phase == 3):
        '''
            In phase 3 any node beloning to the actor is a possible source and
            any empty node is a possible destination, and the same kind of pairing
            as above is made ({possible source : possible destination})
        '''
        moves = []
        moveable_nodes = get_possible_nodes(gamestate, target)
        placeable_nodes = get_possible_nodes(gamestate, EMPTY)
        for moveable in moveable_nodes:
            for placeable in placeable_nodes:
                moves.append({moveable : placeable})
        return moves

def check_phase(gamestate, is_opponent):
    '''
    Helper function to check which phase the gamestate is in based on the rules of the game.
    Returns the phase as an int.
    '''
    if (not is_opponent):
        if(gamestate.AI.markers_left_to_play):
            return 1
        elif(gamestate.AI.markers_on_board > 3):
            return 2
        elif(gamestate.AI.markers_left_to_play <= 3):
            return 3
    else:
        if(gamestate.player.markers_left_to_play):
            return 1
        elif(gamestate.player.markers_on_board > 3):
            return 2
        elif(gamestate.player.markers_left_to_play <= 3):
            return 3

def board_score(gamestate, target):
    '''
    Scoring function for the minmax recursion when it has reached depth.
    '''
    score = 0
    if target == AI:
        opponent = PLAYER
    else:
        opponent = AI

    for line in gamestate.gameboard.lines:
        owners = []
        for node in line.nodes:
            owners.append(node.owner)
        if owners.count(target) == 3:
            score += 10
        if owners.count(target) == 2 and owners.count(EMPTY) == 1:
            score += 7
        if owners.count(opponent) == 3:
            score -= -9
        if owners.count(opponent) == 2 and owners.count(EMPTY) == 1:
            score -= 8

    return score

def get_line_owners(line):
    # Finds a lines owners and returns as a list.
    owners = []
    for node in line.nodes:
        owners.append(node.owner)

    return owners

def blocking_move(gamestate, node, target):
    # Checks if a node will block a three-in-a-row.
    if target == AI:
        opp = PLAYER
    else:
        opp = AI
    for line in gamestate.gameboard.lines:
        for n in line.nodes:
            if (n.get_node_label() == node.get_node_label()):
                line_owners = get_line_owners(line)
                if (line_owners.count(opp) == 2 and line_owners.count(target) == 1):
                    return True
    return False

def minmax(is_AI, gamestate, phase, depth, alpha, beta):
    '''
    Recursive optimization to find which move leads to the most promising branch of moves.
    Will play optimally if search space allows algorithm to find winning moves, else will use
    a defined scoring function to interpret the gamestate and score at depth 0.
    ----------
    Parameters
    ----------
    gamestate:
        a gamestate object containing the gamestate.
    phase:
        the phase in which to move.
    depth:
        How many turns ahead the algorithm will look before using the score function.
        Used to avoid hitting recursion limit and to speed up the calculation.
    alpha/beta:
        The alpha and beta parameters in the alpha-beta pruning method.
    ----------
    Returns:
        The best move and best score at the current depth.
        If algorithm finds a win, returns max or min score.
    '''
    if winning_check(gamestate, AI):
        return None, 100000
    elif winning_check(gamestate, PLAYER):
        return None, -100000
    elif(depth == 0):
        return (None, board_score(gamestate, AI))

    if (is_AI):
        all_possible_moves = get_all_possible_moves(gamestate, phase, AI)
        max_score = -inf
        best_move = choice(all_possible_moves)

        for move in all_possible_moves:
            g = deepcopy(gamestate)
            make_move(g, move, phase, False)

            if(phase == 1):
                if(check_three_in_a_row(g, move, AI)):
                    best_score = 1000
                    best_move = move
                    return best_move, best_score
                elif(blocking_move(g, move, AI)):
                    best_score = 500
                    best_move = move
                    return best_move, best_score
            elif(phase == 2):
                for _, node_to in move.items():
                    if(check_three_in_a_row(g, node_to, AI)):
                        best_score = 1000
                        best_move = move
                        return best_move, best_score
                    elif(blocking_move(g, node_to, AI)):
                        best_score = 500
                        best_move = move
                        return best_move, best_score
            elif(phase == 3):
                for _, node_to in move.items():
                    if(check_three_in_a_row(g, node_to, AI)):
                        best_score = 1000
                        best_move = move
                        return best_move, best_score
                    elif(blocking_move(g, node_to, AI)):
                        best_score = 500
                        best_move = move
                        return best_move, best_score


            is_AI = not is_AI
            _, score = minmax(is_AI, g, phase, depth-1, alpha, beta)
            if(score > max_score):
                max_score = score
                best_move = move

            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return best_move, max_score

    else:
        all_possible_moves = get_all_possible_moves(gamestate, phase, PLAYER)
        min_score = inf
        best_move = choice(all_possible_moves)

        for move in all_possible_moves:
            g = deepcopy(gamestate)
            make_opponent_move(g, move, phase)

            is_AI = not is_AI
            _, score = minmax(is_AI, g, phase, depth-1, alpha, beta)
            if(score < min_score):
                min_score = score
                best_move = move

            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return best_move, min_score

def run_game_hard(data):
    '''
    Runs the hard AI
    ----------
    Parameters
    ----------
    data:
        data in JSON format
    ----------
    Returns:
        An object containing:
        - status: a status code (0 if game is still in play, 1 if player has won or -1 if AI has won)
        - gamestateJSON: the full updated gamestate in JSON format
        - place: the node placed at in phase 1. Will be none in phase 2 and 3
        - move: an object with the node moved from as key and node moved to as value. Will be None in phase 1
        - removed: opponent node removed if any
    '''

    data = load_save_file()
    gamestate = Gamestate(data)


    update_markers_on_board_numbers(gamestate)

    status = 0
    if (winning_check(gamestate, AI)):
        status = -1
        response = {'status': status, 'gamestateJSON': gamestate.to_json(),
                    'place': None, 'move': None, 'removed': None
        }
        return response
    elif (winning_check(gamestate, PLAYER)):
        status = 1
        response = {'status': status, 'gamestateJSON': gamestate.to_json(),
                    'place': None, 'move': None, 'removed': None
        }
        return response
    else:
        status = 0

    # Checking if in phase 1 of the game.
    if (gamestate.AI.markers_left_to_play > 0):
        possible_nodes = get_possible_nodes(gamestate, EMPTY)
        if (len(get_possible_nodes(gamestate, EMPTY)) > 9):
            chosen_place, max_score = minmax(True, gamestate, 1, 3, -inf, inf)
        else:
            chosen_place, max_score = minmax(True, gamestate, 1, 4, -inf, inf)

        # Placing.
        _, removed = make_move(gamestate, chosen_place, 1, True)
        chosen_place_label = chosen_place.get_node_label() if chosen_place != None else None
#This is where we update the AIs previous move!!!! (GROUP F!!!!!)
        gamestate.AI.previous_move[1] = f'{chosen_place_label}'
        chosen_move_labels = None

    # Checking if in phase 2 of the game.
    elif (gamestate.AI.markers_left_to_play == 0 and (gamestate.AI.markers_on_board > 3)):
        # Phase 2!
        possible_nodes = get_possible_nodes(gamestate, AI)
        neighbours = get_neighbours(gamestate, possible_nodes)

        possible_neighbours = []
        for n in possible_nodes:
            for neighbour in neighbours[n]:
                if(neighbour.owner == EMPTY):
                    possible_neighbours.append({n : neighbour})

        if(len(possible_neighbours) > 0):
            moved = False
            while (not moved):
                if (len(get_possible_nodes(gamestate, EMPTY)) > 11):
                    chosen_move, max_score = minmax(True, gamestate, 2, 3, -inf, inf)
                else:
                    chosen_move, max_score = minmax(True, gamestate, 2, 4, -inf, inf)

                moved, removed = make_move(gamestate, chosen_move, 2, True)
                for node_from, node_to in chosen_move.items():
                    chosen_move_labels = {node_from.get_node_label() : node_to.get_node_label()}
                chosen_place_label = None
        else:
            pass

    # Checking if in phase 3 of the game.
    elif(gamestate.AI.markers_left_to_play == 0 and gamestate.AI.markers_on_board == 3):

        chosen_move, max_score = minmax(True, gamestate, 3, 3, -inf, inf)

        _, removed = make_move(gamestate, chosen_move, 3, True)
        for node_from, node_to in chosen_move.items():
                    chosen_move_labels = {node_from.get_node_label() : node_to.get_node_label()}
        chosen_place_label = None

    save_save_file(gamestate.to_json())

    if (winning_check(gamestate, AI)):
        status = -1
    elif (winning_check(gamestate, PLAYER)):
        status = 1
    else:
        status = 0
    response = {
                'status': status, 'gamestateJSON': gamestate.to_json(),
                'place': chosen_place_label,
                'move': chosen_move_labels,
                'removed': removed
                }
    return response
