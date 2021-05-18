import json
from os import path


class Player:
    """
    A class used to represent Player

    Attributes
    ----------
    symbol: string
        the symbol representing the player, either 'X' or 'O'
    markers_left_to_play : int
        amount of markers the player has not yet placed
    markers_on_board : int
        amount of markers the player has on the board
    prevous_move : [string]
        the players previous move, previous_move[0] is the
        node the marker was moved from, previous_move[1] is
        the node the marker was moved to

    Methods
    -------

    """
    def __init__(self, symbol, markers_left_to_play, markers_on_board, previous_move):
        """
        Parameters
        ----------
        see class attributes
        """
        self.symbol = symbol
        self.markers_left_to_play = markers_left_to_play
        self.markers_on_board = markers_on_board
        self.previous_move = previous_move

    def to_json(self):
        return({'marker' : self.symbol,
                'markers_left' : self.markers_left_to_play,
                'markers_on_board' : self.markers_on_board,
                'previous_move' : self.previous_move})


class Node:
    """
    A class used to represent a node on the game board

    Attributes
    ----------
    vertical: char
        the character representing the vertical position
    horizontal: int
        the number representing the horizontal position
    owner: string
        the symbol of the player who has their marker
        on this node, or '-' if empty

    Methods
    -------

    """
    def __init__(self, vertical, horizontal, owner):
        """
        Parameters
        ----------
        see class attributes
        """
        self.vertical = vertical
        self.horizontal = horizontal
        self.owner = owner

    def __str__(self):
        """
        Returns
        ----------
        the string representation of a node,
        example: "a1 : X"
        """
        return (self.vertical + self.horizontal + ' : ' + self.owner)

    def get_node_label(self):
        '''
            Function that returns the label of the node.
        '''
        return self.vertical + self.horizontal
    def to_json(self):
        position = self.vertical + self.horizontal
        node = ({position : self.owner});
        return(node)

    def get_position(self):
        return(self.vertical + self.horizontal)

    def get_owner(self):
        return(self.owner)

class Line:
    """
    A class used to represent a line on the game board

    Attributes
    ----------
    nodes: [Node]
        a list of the three nodes in this line

    Methods
    -------

    """
    def __init__(self, nodes):
        """
        Parameters
        ----------
        see class attributes
        """
        self.nodes = nodes
        self.tot = 0

    def __str__(self):
        """
        Returns
        ----------
        the string representation of a line,
        example: "a1 : X, a4 : O, a7: -"
        """
        return (str(self.nodes[0]) + ', ' + str(self.nodes[1]) + ', ' + str(self.nodes[2]))

    def to_json(self):
        nodes = [self.nodes[0].to_json(),
                 self.nodes[1].to_json(),
                 self.nodes[2].to_json()]
        line = []
        for node in nodes:
            for key in node.keys():
                line.append(key)

        return({'line' : line})

class Gameboard:
    """
    A class used to represent the gameboard

    Attributes
    ----------
    a_nodes: [Node]
        a list of the three a nodes
    b_nodes: [Node]
        a list of the three b nodes
    c_nodes: [Node]
        a list of the three c nodes
    d_nodes: [Node]
        a list of the six d nodes
    e_nodes: [Node]
        a list of the three e nodes
    f_nodes: [Node]
        a list of the three f nodes
    g_nodes: [Node]
        a list of the three g nodes
    lines: [Lines]
        a list of all the lines on the gameboard

    Methods
    -------

    """
    def __init__(self, map, lines):
        """
        Parameters
        ----------
        map:
            a json object containing the nodes
            on the gameboard
        lines:
            a json object containing the lines
            on the gameboard
        """
        map_lines = []
        for node_row in map.keys():
            nodes = []
            for key in map[node_row].keys():
                value = map[node_row][key]
                node = Node(key[0], key[1], value)
                nodes.append(node)
            setattr(self, node_row, nodes)

        for line in lines:
            target_nodes = []
            for node in line:
                vertical = node[0]
                horizontal = node[1]
                node_row_str = vertical + '_nodes'
                node_row = getattr(self, node_row_str)
                for target in node_row:
                    if (target.horizontal == horizontal):
                        target_nodes.append(target)
            current_line = Line(target_nodes)
            map_lines.append(current_line)
        self.lines = map_lines

    def __str__(self):
        """
        Returns
        ----------
        the string representation of the gameboard,
        which is all the lines and nodes
        """
        #print(self.lines[0].to_json())
        return('\n'.join(map(str, self.lines)))

    def to_json(self):
        a_json = {self.a_nodes[0].get_position() : self.a_nodes[0].get_owner(),
                  self.a_nodes[1].get_position() : self.a_nodes[1].get_owner(),
                  self.a_nodes[2].get_position() : self.a_nodes[2].get_owner()}
        b_json = {self.b_nodes[0].get_position() : self.b_nodes[0].get_owner(),
                  self.b_nodes[1].get_position() : self.b_nodes[1].get_owner(),
                  self.b_nodes[2].get_position() : self.b_nodes[2].get_owner()}
        c_json = {self.c_nodes[0].get_position() : self.c_nodes[0].get_owner(),
                  self.c_nodes[1].get_position() : self.c_nodes[1].get_owner(),
                  self.c_nodes[2].get_position() : self.c_nodes[2].get_owner()}
        d_json = {self.d_nodes[0].get_position() : self.d_nodes[0].get_owner(),
                  self.d_nodes[1].get_position() : self.d_nodes[1].get_owner(),
                  self.d_nodes[2].get_position() : self.d_nodes[2].get_owner(),
                  self.d_nodes[3].get_position() : self.d_nodes[3].get_owner(),
                  self.d_nodes[4].get_position() : self.d_nodes[4].get_owner(),
                  self.d_nodes[5].get_position() : self.d_nodes[5].get_owner()}
        e_json = {self.e_nodes[0].get_position() : self.e_nodes[0].get_owner(),
                  self.e_nodes[1].get_position() : self.e_nodes[1].get_owner(),
                  self.e_nodes[2].get_position() : self.e_nodes[2].get_owner()}
        f_json = {self.f_nodes[0].get_position() : self.f_nodes[0].get_owner(),
                  self.f_nodes[1].get_position() : self.f_nodes[1].get_owner(),
                  self.f_nodes[2].get_position() : self.f_nodes[2].get_owner()}
        g_json = {self.g_nodes[0].get_position() : self.g_nodes[0].get_owner(),
                  self.g_nodes[1].get_position() : self.g_nodes[1].get_owner(),
                  self.g_nodes[2].get_position() : self.g_nodes[2].get_owner()}
        lines_json = [['a1', 'a4', 'a7'], ['b2', 'b4', 'b6'], ['c3', 'c4', 'c5'],
                 ['d1', 'd2', 'd3'], ['d5', 'd6', 'd7'], ['e3', 'e4', 'e5'],
                 ['f2', 'f4', 'f6'], ['g1', 'g4', 'g7'], ['a7', 'd7', 'g7'],
                 ['b6', 'd6', 'f6'], ['c5', 'd5', 'e5'], ['a4', 'b4', 'c4'],
                 ['e4', 'f4', 'g4'], ['c3', 'd3', 'e3'], ['b2', 'd2', 'f2'],
                 ['a1', 'd1', 'g1'], ['a7', 'b6', 'c5'], ['g7', 'f6', 'e5'],
                 ['a1', 'b2', 'c3'], ['g1', 'f2', 'e3']]
        map_json = {'a_nodes' : a_json, 'b_nodes' : b_json, 'c_nodes' : c_json,
                    'd_nodes' : d_json,'e_nodes' : e_json, 'f_nodes' : f_json,
                    'g_nodes' : g_json}

        return({'a_nodes' : a_json, 'b_nodes' : b_json, 'c_nodes' : c_json,
               'd_nodes' : d_json, 'e_nodes' : e_json, 'f_nodes' : f_json,
                'g_nodes' : g_json, 'map' : map_json, 'lines' : lines_json})

class Gamestate:
    """
    A class used to represent the gamestate

    Attributes
    ----------
    AI: Player
        a Player object representing the AI
    opponent: Player
        a Player object representing the player
    gameboard: Gameboard
        the gameboard

    Methods
    -------

    """
    def __init__(self, data):
        """
        Parameters
        ----------
        data:
            a json object containing information about
            the AI, the player and the gameboard
        """
        data_data = data['data']
        self.AI = Player(data_data['ai_marker'],
                        data_data['ai_markers_left'],
                        data_data['ai_markers_on_board'],
                        data_data['ai_previous_move'])
        self.player = Player(data_data['player_marker'],
                         data_data['player_markers_left'],
                         data_data['player_markers_on_board'],
                         data_data['player_previous_move'])
        self.gameboard = Gameboard(data['map'], data['lines'])

    def __str__(self):
        """
        Returns
        ----------
        the string representation of the gamestates gameboard
        """
        #print(self.gameboard.to_json())
        #print(self.to_json())
        
        return (str(self.gameboard))

    def to_json(self):
        data = {'ai_marker' : self.AI.to_json().get('marker'),
                'ai_markers_left' : self.AI.to_json().get('markers_left'),
                'ai_markers_on_board' : self.AI.to_json().get('markers_on_board'),
                'ai_previous_move' : self.AI.to_json().get('previous_move'),
                'player_marker' : self.player.to_json().get('marker'),
                'player_markers_left' : self.player.to_json().get('markers_left'),
                'player_markers_on_board' : self.player.to_json().get('markers_on_board'),
                'player_previous_move' : self.player.to_json().get('previous_move')}
        return({'data' : data, 'map' : self.gameboard.to_json().get('map'),
                'lines' : self.gameboard.to_json().get('lines')})
                # 'a_nodes' : self.gameboard.to_json().get('a_nodes'),
                # 'b_nodes' : self.gameboard.to_json().get('b_nodes'),
                # 'c_nodes' : self.gameboard.to_json().get('c_nodes'),
                # 'd_nodes' : self.gameboard.to_json().get('d_nodes'),
                # 'e_nodes' : self.gameboard.to_json().get('e_nodes'),
                # 'f_nodes' : self.gameboard.to_json().get('f_nodes'),
                # 'g_nodes' : self.gameboard.to_json().get('g_nodes'),})

"""
The following code was used to test the classes
and print out the gamestate of the loaded file

Before testing this file, you must run the program
saveGame.py first (in order to create the file
save_file.json if you dont already have it)
Ugly solution, but works for testing
it for now :)
"""
"""
def load_save_file():
    exists = path.exists("save_file.json")
    if (exists):
        with open("save_file.json", "r") as save_file:
            data = json.load(save_file)
            gamestate = Gamestate(data)
            #print(str(gamestate))
            print("test to json")
            print(gamestate.to_json())
            return data

def save_save_file(data):
    with open("save_file.json", "w") as save_file:
        json.dump(data, save_file, indent=1, sort_keys=True)



gamestate = Gamestate(load_save_file())

node = Node('a', '1', '-');
nodes = [node, node, node]
player = Player('X', '4', '3', ['a1', 'a4']);
line = Line(nodes)
save_save_file(gamestate.to_json());
"""