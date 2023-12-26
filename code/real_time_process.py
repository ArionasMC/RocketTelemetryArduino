import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

ser = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)
print(ser.is_open)

acc = np.array([])
gyro = np.array([[], [], []])
time = 0
g_time = 0

fig = plt.figure()
fig.suptitle('A tale of 4 subplots')

ax1 = fig.add_subplot(4,1,1)
ax2 = fig.add_subplot(4,1,2)
ax3 = fig.add_subplot(4,1,3)
ax4 = fig.add_subplot(4,1,4)

def getLengthAndPrint(data):
    temp = data.split(': ')[1].split(', ')
    l = math.sqrt(math.pow(float(temp[0]),2) + math.pow(float(temp[1]),2) + math.pow(float(temp[2]),2))
    print(l)
    return l

def animate(i):
    global time
    global g_time
    global acc
    global gyro
    data = ser.readline().decode()
    while data:
        if data.startswith('Acc: '):
            acc = np.append(acc, getLengthAndPrint(data))
            time = time + 0.5
        elif data.startswith('Gyro: '):
            temp = data.split(': ')[1].split(', ')
            print("processing:",temp)
            gyro = np.c_(gyro, np.array([float(temp[0]), float(temp[1]), float(temp[2])]))
            print("processed",gyro)
            g_time = g_time + 0.5
        data = ser.readline().decode()
    
    s = len(acc)
    t = np.linspace(0, time, s)
    gt = np.linspace(0, g_time, len(gyro[0]))

    ax1.clear()
    ax1.plot(t, acc)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Acceleration (m/s^2)")

    ax2.clear()
    print("gt=",gt,"gyro[0]=",gyro[0])
    ax2.plot(gt, gyro[0])
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Angular velocity x-axis(rad/s)")

    ax3.clear()
    ax3.plot(gt, gyro[1])
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Angular velocity y-axis(rad/s)")
    
    ax4.clear()
    ax4.plot(gt, gyro[2])
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Angular velocity z-axis(rad/s)")

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()