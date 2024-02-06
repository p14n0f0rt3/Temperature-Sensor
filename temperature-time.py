import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import time
import math
import serial
import re
# configure the serial port
ser = serial.Serial(
 port='COM5',
 baudrate=115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_TWO,
 bytesize=serial.EIGHTBITS
)
#extract the values we want
def extract_decimal(given):
 text = given.decode() #first decode to normalize into a string
 search_string = r'(\d+\.\d+)'
 match = re.search(search_string, text)
 if match:
  value = float(match.group(1))
  return value
 else:
  return None

 ser.isOpen()
 while 1:
     strin = ser.readline()
     use_val = extract_decimal(strin)
     print(use_val)
xsize=60

def data_gen():
    t = data_gen.t
    while True:
        ser.isOpen()
        output = ser.readline()
        useval = extract_decimal(output)

        t += 1
        val = useval
        yield t, val


def run(data):
    # update the data
    t, y = data
    if t > -1:
        xdata.append(t)
        ydata.append(y)
        if t > xsize:  # Scroll to the left.
            ax.set_xlim(t - xsize, t)
        line.set_data(xdata, ydata)

    return line,


def on_close_figure(event):
    sys.exit(0)

cache_frame_data=False
data_gen.t = -1
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close_figure)
ax = fig.add_subplot(111)
line, = ax.plot([], [], lw=2)
ax.set_ylim(20, 90)
ax.set_xlim(0, xsize)
ax.grid()
xdata, ydata = [], []

# Important: Although blit=True makes graphing faster, we need blit=False to prevent
# spurious lines to appear when resizing the stripchart.
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100, repeat=False)
plt.show()
