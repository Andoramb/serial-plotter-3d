import math
import time

import matplotlib.pyplot as plt
import serial

def make_client(url, apikey):
     """Creates and returns an instance of the OctoRest client.

     Args:
         url - the url to the OctoPrint server
         apikey - the apikey from the OctoPrint server found in settings
     """
     try:
         client = OctoRest(url='http://192.168.1.100:8441', apikey='DABF5FAE5B7348BA9ED5E159BC93FD83')
         return client
     except ConnectionError as ex:
         # Handle exception as you wish
         print(ex)

def file_names(client):
     """Retrieves the G-code file names from the
     OctoPrint server and returns a string message listing the
     file names.

     Args:
         client - the OctoRest client
     """
     message = "The GCODE files currently on the printer are:\n\n"
     for k in client.files()['files']:
         message += k['name'] + "\n"
     print(message)



# init serial - source for the data
SERIAL_PORT = 'COM3'  # path to serial output on Mac
SERIAL_RATE = 9600
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)

# containers for data to be displayed on plot
last_x, last_y, last_z = None, None, None
xs, ys, zs, cs = [], [], [], []
new_points_count = 0

# init plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.canvas.mpl_connect('close_event', lambda evt: quit())

while True:

    # Parse "x  y  z" value from serial
    try:
        xyz = ser.readline().decode('utf-8').split()
        if last_x is None:
            last_x = float(xyz[0])
            last_y = float(xyz[1])
            last_z = float(xyz[2])

        x = float(xyz[0])
        y = float(xyz[1])
        z = float(xyz[2])

    # reconnect to serial on errors
    except serial.SerialException as se:
        print('Serial has errors, trying to reconnect. err:', se)
        time.sleep(3)
        ser.close()
        ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
        print('Serial reconnected!')

    # ignore other non-data values
    except Exception as e:
        print("Bad read from serial:", xyz, e)
        continue

    # distance between current and last point in 3d
    distance_to_previous = math.sqrt(math.pow(x - last_x, 2) + math.pow(y - last_y, 2) + math.pow(z - last_z, 2))

    # if last point was too close, don't plot it
    if distance_to_previous > 0.15:
        xs.append(x)
        ys.append(y)
        zs.append(z)
        cs.append(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))  # vector length
        last_x, last_y, last_z = x, y, z
        new_points_count += 1

    # remove old dots, smaller buffer gives higher refresh rate on plot
    if len(xs) > 256:
        xs.pop(0)
        ys.pop(0)
        zs.pop(0)
        cs.pop(0)

    # draw when we have 2 points, too frequent draws cause lags
    if new_points_count > 1:
        ax.cla()
        #ax.scatter(xs, ys, zs, c=cs, cmap='cool')
        ax.plot(xs, ys, zs, 'bo-', linewidth=2, markersize=5)
        new_points_count = 0

    plt.draw()
    plt.pause(0.001)
