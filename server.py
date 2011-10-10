import zmq
import time
import util

context = zmq.Context()

# Socket to reply to requests from individual clients
pull_socket = context.socket(zmq.PULL)
pull_socket.bind("tcp://*:5555")

# Socket to broadcast to all clients
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5556")

def send(players, recipient='all'):
    pub_socket.send(recipient + ':' + util.pickle(players))

player_list = []
player_details = {}

while True:
    
    time.sleep(0.016)

    send(player_details)

    try:
        msg = pull_socket.recv_pyobj(flags=zmq.core.NOBLOCK)
    except zmq.core.error.ZMQError:
        pass
    else:
        if msg['cmd'] == 'new':
            player = util.unpickle(msg['player'])
            print 'new player %s' % player.name
            player_details[player.name] = player
        elif msg['cmd'] == 'update':
            player = util.unpickle(msg['player'])
            del player_details[player.name]
            player_details[player.name] = player
        elif msg['cmd'] == 'update_stop':
            player = util.unpickle(msg['player'])
            del player_details[player.name]
            player_details[player.name] = player

