from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from game import *
from greedy_player import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello():
    return 'hello'

units = [Infantry,Mech,Recon,Tank,Artillery]


@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    
    map = [[None for j in range(len(data[0]))] for i in range(len(data))]
    turn = data[0][0].get("turn")

    for r in range(len(data)):
        for c in range(len(data[0])):
            unit = data[r][c].get("unit")
            if (unit != None):
                id = unit.get('type')
                team = unit.get('team')
                hp = unit.get('hp')
                isExhausted=unit.get('isExhausted')
                # print(id)
                # print(hp)
                # print(isExhausted)
                newUnit = units[id](team,hp,isExhausted)
                map[r][c] = newUnit
    
    game = Game(map,turn)

    # moveset = 
    # print()

    # Process the data and return a response
    # return jsonify(get_next_greedy(game))
    return jsonify(get_move_order(game,1000))



def create_game_from_json(json_str):
    json_data = json.loads(json_str)
    map_data = json_data["map"]
    map_grid = [[map_data[row][col] for col in range(len(map_data[row]))] for row in range(len(map_data))]
    return Game(json_data["title"], json_data["description"], map_grid, json_data["start"], json_data["end"])

if __name__ == '__main__':
    app.run()