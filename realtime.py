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
ringbuffer1 = []
ringbuffer2 = []

# for the thread below
doRun = True

# This reads the data from the socket in an endless loop and stores the data in a buffer
def readSocket():
    global ringbuffer1
    global ringbuffer2
    global ECGchannel
    global EMGchannel
    while doRun:
        # check if data is available
        data = f.readline()
        values = np.array(data.split(','),dtype=np.float32)
        ringbuffer1.append(values[ECGchannel])
        ringbuffer2.append(values[EMGchannel])
    # here we might need to add 'return[ringbuffer1, ringbuffer2]'?

# start reading data from socket
t = threading.Thread(target=readSocket)
t.start()

# now let's plot the data
#fig, ax = plt.subplots()
# that's our plotbuffer
#plotbuffer = np.zeros(500)
# plots an empty line
#line, = ax.plot(plotbuffer)
# axis
#ax.set_ylim(0, 0.002)
#ax.set_xlim(0, 125)

# now let's plot the data
fig, (ax1,ax2) = plt.subplots(2,1)
fig.subplots_adjust(hspace=0.5)
plotbuffer1 = np.zeros(500)
plotbuffer2 = np.zeros(500)
line1, = ax1.plot(plotbuffer1)
line2, = ax2.plot(plotbuffer2)
ax1.set_xlim(0,125)
ax2.set_xlim(0,125)
# maybe set ylim later on
ax1.set_xlabel('Time/sec')
ax1.set_ylabel('Amplitude/V')
ax2.set_xlabel('Time/sec')
ax2.set_ylabel('Amplitude/V')
ax1.set_title('ECG (Channel 7)')
ax2.set_title('EMG (Channel 8)')


# receives the data from the generator below
def update(data):
    global plotbuffer1
    global plotbuffer2
    # add new data to the buffer
    plotbuffer1=np.append(plotbuffer1,data)
    plotbuffer2=np.append(plotbuffer2,data)
    # only keep the 500 newest points and discard the old ones
    plotbuffer1=plotbuffer1[-500:]
    plotbuffer2=plotbuffer2[-500:]
    # set the new 500 points of desired channel
    line1.set_ydata(plotbuffer1)
    line2.set_ydata(plotbuffer2)
    return [line1, line2]

# this checks in an endless loop if there is data in the ringbuffer
# of there is data then emit it to the update funnction above
def data_gen():
    global ringbuffer1
    #endless loop which gets data
    while True:
        # check if data is available
        if not ringbuffer1 == []:
            resultECG = ringbuffer1
            ringbuffer1 = []
            yield resultECG
    # do the same for EMG data
    global ringbuffer2
    while True:
        # check if data is available
        if not ringbuffer2 == []:
            resultEMG = ringbuffer2
            ringbuffer2 = []
            yield resultEMG

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
