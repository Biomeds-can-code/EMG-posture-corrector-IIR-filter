import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading # we use threading as several things happening simultaneously

# read from channels 7 and 8
ECGchannel = 7
EMGchannel = 8

# socket connection to attys_scope
# first constant (AF_INET) is address family, second (SOCK_DGRAM) is socket type
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
listen_addr = ("",65000)
'''
Broadcast must be 'on' in attys-scope so that recording can be accessed on Python code

The port to be used is 65000
'''
s.bind(listen_addr)
f = s.makefile()

#That's our ringbuffer which accumluates the samples
#It's emptied every time when the plot window below does a repaint
ringbuffer = []


# for the thread below
doRun = True

# This reads the data from the socket in an endless loop and stores the data in a buffer
def readSocket():
    global ringbuffer
    global ECGchannel
    global EMGchannel
    while doRun:
        # check if data is available
        data = f.readline()
        values = np.array(data.split(','),dtype=np.float32)
        ringbuffer.append(values[EMGchannel])
        

# start reading data from socket
t = threading.Thread(target=readSocket)
t.start()

# now let's plot the data
fig, ax = plt.subplots()
# that's our plotbuffer
plotbuffer = np.zeros(500)
# plots an empty line
line, = ax.plot(plotbuffer)
# axis
#ax.set_ylim(0, 0.002)
ax.set_xlim(0, 125) # might be best to increase this value so we can observe more data (maybe over 5 seconds)


# receives the data from the generator below
def update(data):
    global plotbuffer
    # add new data to the buffer
    plotbuffer=np.append(plotbuffer,data)
    # only keep the 500 newest ones and discard the old ones
    plotbuffer=plotbuffer[-500:]
    # set the new 500 points of desired channel
    line.set_ydata(plotbuffer)
    return line,

# this checks in an endless loop if there is data in the ringbuffer
# of there is data then emit it to the update funnction above
def data_gen():
    global ringbuffer
    #endless loop which gets data
    while True:
        # check if data is available
        if not ringbuffer == []:
            result = ringbuffer
            ringbuffer = []
            yield result

# start the animation
ani = animation.FuncAnimation(fig, update, data_gen, interval=100)

# show it
plt.show()

# stop the thread which reads the data
doRun = False
# wait for it to finish
t.join()

# close the file and socket
f.close()
s.close()

print("finished")
