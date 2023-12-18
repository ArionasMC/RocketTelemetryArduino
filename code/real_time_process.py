import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

ser = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)
print(ser.is_open)

acc = np.array([])
gyro = np.array([])
time = 0

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def getLengthAndPrint(data):
    temp = data.split(': ')[1].split(', ')
    l = math.sqrt(math.pow(float(temp[0]),2) + math.pow(float(temp[1]),2) + math.pow(float(temp[2]),2))
    print(l)
    return l

def animate(i):
    global time
    global acc
    global gyro
    data = ser.readline().decode()
    while data:
        if data.startswith('Acc: '):
            acc = np.append(acc, getLengthAndPrint(data))
            time = time + 0.5
        elif data.startswith('Gyro: '):
            gyro = np.append(gyro, getLengthAndPrint(data))
            time = time + 0.5
        data = ser.readline().decode()
    
    s = len(acc)
    t = np.linspace(0, time, s)

    ax1.clear()
    ax1.plot(t, acc)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()