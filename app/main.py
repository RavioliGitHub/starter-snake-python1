import json
import os
import random
import bottle
import brain
import game_engine
from api import ping_response, start_response, move_response, end_response
import time
import sys



previous_data_prediction = "f"
@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json


    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    global previous_data_prediction
    startTime = time.time()
    data = bottle.request.json

    #if data['turn'] > 0:
       # game_engine.check_if_update_was_accurate(previous_data_prediction, data)


    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(json.dumps(data))

    moveResponse = brain.get_best_move(data)

    previous_data_prediction = game_engine.update(data, [moveResponse])

    print(time.time()-startTime)

    return move_response(moveResponse)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    print(str(sys.argv))
    port = 8080
    if len(sys.argv) == 2:
        port += int(sys.argv[1])
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', str(port)),
        debug=os.getenv('DEBUG', True)
    )
