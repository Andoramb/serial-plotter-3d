import math
import time

import matplotlib.pyplot as plt

##
## This works for one request but websocket connection is needed for long-lived connection
##

#import requests
#octourl = 'http://192.168.1.100:8441/plugin/DisplayLayerProgress/values'
#octoapi = 'DABF5FAE5B7348BA9ED5E159BC93FD83'
#header={"x-api-key" : octoapi}
#
#response = requests.get(octourl, headers=header)
#print(response.json()['layer']['current'])


import websocket, json, requests
import configparser
import _thread

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    auth_message = "{ \"auth\": \""+config['auth']['octopi.username']+":"+session+"\" }"
    ws.send(auth_message)

def read_config(configfile):
    config.read(configfile)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    read_config("octo.ini")
    logindata = { 'user': config['auth']['octopi.username'], 'pass': config['auth']['octopi.password'] }
    r = requests.post("http://"+config['auth']['octopi.hostname']+"/api/login", json=logindata, verify=False)
    print('{} {} '.format(r.status_code, r.json()))
    data = r.json()
    #print('session: {}'.format(data['session']))
    session = data['session']
    ws_host = "ws://"+config['auth']['octopi.hostname']+"/sockjs/websocket"
    websocket.enableTrace(True)
    #ws = websocket.WebSocketApp(ws_host,
    #    on_open = on_open,
    #    on_message = on_message,
    #    on_error = on_error,
    #    on_close = on_close)
    #ws.run_forever()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.canvas.mpl_connect('close_event', lambda evt: quit())

with open('data/magnet.csv', 'r') as f:
    dots = f.readlines()

xs, ys, zs, cs = [], [], [], []

#for dot in dots:
#    xyz = dot.split()
#    x, y, z = float(xyz[0]), float(xyz[1]), float(xyz[2])
#    xs.append(x), ys.append(y), zs.append(z)
#
#    # vector length is color!
#    cs.append(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))
#
#    ax.cla()
#    #ax.scatter(xs, ys, zs, c=cs, cmap='cool')
#    ax.plot(xs, ys, zs, 'bo-', linewidth=2, markersize=5)
#
#    plt.title('Gantry movement plot')
#    plt.xlabel('X Axis')
#    plt.ylabel('Y Axis')
#    plt.draw()
#    plt.pause(0.001)

#while True:
    #plt.draw()
    #plt.pause(0.001)
