from flask import Flask, render_template, jsonify
from flask import request
from webapi.piece import Piece
import webapi.game_constants as constants
from webapi.game import Game
from webapi.agents.base_agent import BaseAgent
import sys
import pprint as pp
import datetime

app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/api/get-initial-setup', methods=['GET'])
def get_initial_setup():
    players = {0: {'name': 'Computer', 'type': 0}, 1: {'name': 'Human', 'type': 1}}
    game = Game(players).asdict()
    return jsonify(game)


# @api.route('/api/get-rules', methods=['GET'])
# def get_rules():
#     rules = {'move_matrix': rules_config.move_matrix, 'take_matrix': rules_config.take_matrix}
#     return jsonify(rules)


@app.route('/api/move', methods=["POST"])
def move():
    #try:
        req = request.get_json()
        print(type(req))
        game = Game.fromdict(req)
        agent = BaseAgent(game)
        # print(type(game))
        # pp.pprint(game.asdict())
        return jsonify({'error': False})
    # except Exception as e:
    #     print(e)
    #     return jsonify({'error': True})