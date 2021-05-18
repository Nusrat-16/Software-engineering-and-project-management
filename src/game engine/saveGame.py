import json
from os import path
from os import remove

def create_save_file():
    with open("save_file.json", "w") as save_file:
        a_nodes = {'a1' : "-", 'a4' : "-", 'a7' : "-"}
        b_nodes = {'b2' : "-", 'b4' : "-", 'b6' : "-"}
        c_nodes = {'c3' : "-", 'c4' : "-", 'c5' : "-"}
        d_nodes = {'d1' : "-", 'd2' : "-", 'd3' : "-", 'd5' : "-", 'd6' : "-", 'd7' : "-"}
        e_nodes = {'e3' : "-", 'e4' : "-", 'e5' : "-"}
        f_nodes = {'f2' : "-", 'f4' : "-", 'f6' : "-"}
        g_nodes = {'g1' : "-", 'g4' : "-", 'g7' : "-"}
        lines = [['a1', 'a4', 'a7'], ['b2', 'b4', 'b6'], ['c3', 'c4', 'c5'],
                 ['d1', 'd2', 'd3'], ['d5', 'd6', 'd7'], ['e3', 'e4', 'e5'],
                 ['f2', 'f4', 'f6'], ['g1', 'g4', 'g7'], ['a7', 'd7', 'g7'],
                 ['b6', 'd6', 'f6'], ['c5', 'd5', 'e5'], ['a4', 'b4', 'c4'],
                 ['e4', 'f4', 'g4'], ['c3', 'd3', 'e3'], ['b2', 'd2', 'f2'],
                 ['a1', 'd1', 'g1'], ['a7', 'b6', 'c5'], ['g7', 'f6', 'e5'],
                 ['a1', 'b2', 'c3'], ['g1', 'f2', 'e3']]
        map = {'a_nodes' : a_nodes, 'b_nodes' : b_nodes, 'c_nodes' : c_nodes, 'd_nodes' : d_nodes,
                'e_nodes' : e_nodes, 'f_nodes' : f_nodes,'g_nodes' : g_nodes}
        data = {
            'data': {'ai_marker' : 'O',
            'ai_markers_left' : 12,
            'ai_markers_on_board' : 0,
            'ai_previous_move' : [None, None, False, None],
            'player_marker' : 'X',
            'player_markers_left' : 12,
            'player_markers_on_board' : 0,
            'player_previous_move': [None, None, None],}, #[Node moves from, node moved to, if moved from a three in a row (true or false)]
            

            'map' : map,
            'lines' : lines
        }
        json.dump(data, save_file, indent=1, sort_keys=True)
        return data

def save_save_file(data):
    with open("save_file.json", "w") as save_file:
        json.dump(data, save_file, indent=1, sort_keys=True)


def load_save_file():
    exists = path.exists("save_file.json")
    if (exists):
        with open("save_file.json", "r") as save_file:
            data = json.load(save_file)
            return data
    else:
        return create_save_file()

def delete_save_file():
    exists = path.exists("save_file.json")
    if (exists):
        remove('save_file.json')

# Tests

#create_save_file()
'''
#save_file = load_save_file()

#save_file["map"]["a_nodes"] = {'a1' : "X", 'a4' : "X", 'a7' : "-"}
#save_file["map"]["d_nodes"]["d1"] = "X"
#save_file["map"]["d_nodes"]["d2"] = "O"
#save_file["map"]["d_nodes"]["d3"] = "O"

#save_save_file(save_file)

#save_file = load_save_file()

#save_file = load_save_file()

'''


