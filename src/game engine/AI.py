from .classes import *
from .saveGame import *
from random import choice
import sys
# Defining constant values.
PLAYER = 'X'
AI = 'O'
EMPTY = '-'

def update_markers_on_board_numbers(gamestate):
    '''
        Function that takes in a gamestate and updates the number of player and AI markers on board
        in that gamestate.
    '''
    gamestate.AI.markers_on_board = len(get_possible_nodes(gamestate, AI))
    gamestate.player.markers_on_board = len(get_possible_nodes(gamestate, PLAYER))

def make_move(gamestate, chosen_node, phase):
    '''
        Function that takes in a node and places or moves a piece there depending on phase.
        Returns True if move was made, as well as opponent node removed if any. Returns False and None if move failed
    '''
    if(phase == 1):
        chosen_node.owner = AI
        #node_to.owner = AI
        gamestate.player.markers_left_to_play -= 1
        gamestate.AI.markers_left_to_play -= 1
        gamestate.AI.markers_on_board += 1
        #gamestate.AI.previous_move[1] = node_to.get_node_label()

        removed = None
        if (check_three_in_a_row(gamestate, chosen_node, AI)):
            gamestate.AI.previous_move[2] = True
        else:
            gamestate.AI.previous_move[2] = False
        if (check_three_in_a_row(gamestate, chosen_node, AI)):

            removed = remove_opponent_piece(gamestate)


        return True, removed

    if(phase != 1):

        removed = None
        for node_from, node_to in chosen_node.items():
            if(check_legal_move(gamestate, node_from, node_to)):
                node_from.owner = EMPTY
                node_to.owner = AI

                gamestate.AI.previous_move[0] = node_from.get_node_label()
                gamestate.AI.previous_move[1] = node_to.get_node_label()
                if (check_three_in_a_row(gamestate, node_from, AI)):
                    gamestate.AI.previous_move[2] = True
                else:
                    gamestate.AI.previous_move[2] = False

                if (check_three_in_a_row(gamestate, node_to, AI)):
                    removed = remove_opponent_piece(gamestate)

                return True, removed
            else:
                return False, None


def check_legal_move(gamestate, node_from, node_to):
    '''
    Checks that AI doesn't move back to a three-in-a-row from another three-in-a-row.
    Returns True if valid move, and False otherwise
    '''
    if(check_three_in_a_row(gamestate, node_from, AI) and gamestate.AI.previous_move[2] == True and node_to.get_node_label() == gamestate.AI.previous_move[0]):
        return False
    else:
        return True


def get_possible_nodes(gamestate, target):
    '''
        Function that takes in the loaded save file
        and returns the nodes that correspond to target.
    '''
    possible = []
    for line in gamestate.gameboard.lines:
        for node in line.nodes:
            if (node.owner == target and node not in possible):
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
            if (the_node == node):
                if (all_nodes_in_line_belongs_to_target(gamestate, line, target)):
                    return True
    return False

def all_nodes_in_line_belongs_to_target(gamestate, a_line, target):
    '''
    Checks if all three markers in a line belongs to the target.
    ----------
    Parameters
    ----------
    gamestate:
        a gamestate object containing the gamestate
    a_line:
        A line containing three nodes
    target:
        Can either be AI or PLAYER
    ----------
    Returns:
        True if the target has won
        , else false.
    '''
    for node in a_line.nodes:
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

def remove_opponent_piece(gamestate):
    '''
    Removes one of the PLAYERs pieces from the board.
    ----------
    gamestate:
        a gamestate object containing the AI, PLAYER and gameboard.
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
        for line in gamestate.gameboard.lines:
            for node in line.nodes:
                if ((node.get_node_label() == chosen_node.get_node_label()) and (node.owner == PLAYER)):
                    node.owner = EMPTY
                    gamestate.player.markers_on_board -= 1
                    gamestate.AI.previous_move[3] = node.get_node_label()
                    return node.get_node_label()
    else:
        return None

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
    else:
        if (gamestate.AI.markers_left_to_play == 0):
            if (gamestate.AI.markers_on_board <= 2):
                return True

    return False


def node_to_piece(node_list):
    '''
    Function that takes a list of nodes (possibly a list contAIning only one node)
    and returns the corresponding owners of sAId nodes in a list of the same order
    as the passed list.
    '''
    pieces = []
    for node in node_list:
        piece = node.owner
        pieces.append(piece)

    return pieces


def run_game_easy(data):
    '''
    Runs the easy AI
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

        # Chosing randomly where to place next piece.
        chosen_place = choice(possible_nodes)

        # Placing.
        _, removed = make_move(gamestate, chosen_place, 1)
        chosen_place_label = chosen_place.get_node_label() if chosen_place != None else None
#This is where we update the AIs previous move!!!! (GROUP F!!!!!)
        gamestate.AI.previous_move[1] = f'{chosen_place_label}'
        chosen_move_labels = None

    elif (gamestate.AI.markers_on_board > 3):
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
                chosen_move = choice(possible_neighbours)
                moved, removed = make_move(gamestate, chosen_move, 2)
                for node_from, node_to in chosen_move.items():
                    chosen_move_labels = {node_from.get_node_label() : node_to.get_node_label()}
                chosen_place_label = None
        else:
            pass

    elif(gamestate.AI.markers_on_board <= 3):
        # Phase 3!
        if(gamestate.AI.markers_on_board <= 2):
            exit()
        moveable_nodes = get_possible_nodes(gamestate, AI)
        placeable_nodes = get_possible_nodes(gamestate, EMPTY)

        moved = False
        while (not moved):
            move = choice(moveable_nodes)
            place = choice(placeable_nodes)
            chosen_move = {move : place}
            moved, removed = make_move(gamestate, chosen_move, 3)
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
