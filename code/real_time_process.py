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
fig.suptitle('A tale of 2 subplots')

ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

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
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Acceleration (m/s^2)")

    ax2.clear()
    ax2.plot(t, gyro)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Angular velocity (rad/s)")

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()