import random
import math
import time
import json

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)
list_of_rooms = {}
list_of_players = {}

list_of_locations = {1: "Airplane", 2: "Bank", 3: "Beach", 4: "Casino", 5: "Cathedral", 6: "Circus"}
# 7: "Corporate", 8: "Crusader", 9: "Dayspa", 10: "Embassy", 11: "Hospital", 12: "Hotel",
# 13: "Military", 14: "Movie", 15: "Ocean", 16: "Passenger", 17: "Pirate", 18: "Polar"}
list_of_roles = {1: {0: "Spy", 1: "1st Class Passenger", 2: "Air Marshall", 3: "Mechanic",
                     4: "Drunk passenger", 5: "Flight Attendant", 6: "Co-pilot", 7: "Captain"}}


# list of rooms
# state (string); players_qty (int); pass (string); last_update (bigint); players (list)
# state could be open, closed, deleted

# list of players
# key: player, room, role


def randomizer():
    return 100000 + math.floor(random.random() * 100000)


def last_upd():
    return math.floor(time.time() * 10)


def gen_passwd():
    return math.floor(random.random() * 100)


def create_room():
    room_number = randomizer()
    # check if room_number already exists
    while room_number in list_of_rooms:
        room_number = randomizer()
    list_of_rooms[room_number] = {"state": "open", "players_qty": 0, "pass": gen_passwd(),
                                  "last_update": last_upd(), "players": []}
    return room_number


def create_player(room_no):
    player_number = randomizer()
    # check if player_number already exists
    while player_number in list_of_players:
        player_number = randomizer()
    list_of_players[player_number] = {"room_no": room_no, "role": "unset"}
    list_of_rooms[room_no]["players_qty"] = list_of_rooms[room_no]["players_qty"] + 1
    list_of_rooms[room_no]["players"].append(player_number)
    return player_number


def get_json_from_post():
    data_to_parse = str(request.get_data())
    data_to_parse = data_to_parse[2:-1]
    myjson = json.loads(data_to_parse)
    return myjson


@app.route('/room_create', methods=['POST', 'OPTIONS'])
def room_create():
    room_no = create_room()
    passwd = list_of_rooms[room_no]["pass"]
    player_no = create_player(room_no)
    return {"status": 200, "room_no": room_no, "pass": passwd, "player_no": player_no}, 200, \
           {"Access-Control-Allow-Origin": "*",
            "Content-type": "application/json",
            "Access-Control-Allow-Methods": "POST"}


@app.route('/room_join', methods=['POST', 'OPTIONS'])
def room_join():
    room_no = int(get_json_from_post()["room_no"])
    player_no = create_player(room_no)
    return {"status": 200, "player_no": player_no}, 200, {"Access-Control-Allow-Origin": "*",
                                                          "Content-type": "application/json",
                                                          "Access-Control-Allow-Methods": "POST"}


# private method!
@app.route('/room_check', methods=['POST', 'OPTIONS'])
def room_check():
    room_no = int(get_json_from_post()["room_no"])
    print(list_of_rooms[room_no])
    print(list_of_players)
    return {"status": 200}, 200, {"Access-Control-Allow-Origin": "*",
                                  "Content-type": "application/json",
                                  "Access-Control-Allow-Methods": "POST"}


def get_role():
    # returns from 1 to 7. the zero is for spy
    return random.randrange(1, 8)


def set_roles(room_no):
    # get all players except for spy
    players_qty = list_of_rooms[room_no]["players_qty"]
    roles_stack = [0]
    # get random from 1 to players number
    for x in range(1, players_qty):
        next_role = get_role()
        while next_role in roles_stack:
            next_role = get_role()
        roles_stack.append(next_role)
        print('we are appended an role '+str(next_role))
    print(roles_stack)
    for x in range(1, players_qty):
        player_no = list_of_rooms[room_no]["players"][x]
        list_of_players[player_no]["role"] = roles_stack[x]
    print(list_of_players)
    return 0


@app.route('/room_stop', methods=['POST', 'OPTIONS'])
def room_stop():
    room_no = int(get_json_from_post()["room_no"])
    print(room_no)
    passwd = int(get_json_from_post()["pass"])
    print(passwd)
    if list_of_rooms[room_no]["pass"] == passwd:
        set_roles(room_no)
        list_of_rooms[room_no]["state"] = "closed"
        code = 200
    else:
        print("incorrect password")
        code = 500
    return {"status": 200}, code, {"Access-Control-Allow-Origin": "*",
                                   "Content-type": "application/json",
                                   "Access-Control-Allow-Methods": "POST"}


if __name__ == "__main__":
    print('run web server')
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
