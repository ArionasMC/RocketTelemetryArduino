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

fig1 = plt.figure()
fig1.suptitle('Acceleration and Angular Velocity lengths')

ax1 = fig1.add_subplot(2,1,1)
ax2 = fig1.add_subplot(2,1,2)

def getLength(data):
    temp = data.split(': ')[1].split(', ')
    l = math.sqrt(math.pow(float(temp[0]),2) + math.pow(float(temp[1]),2) + math.pow(float(temp[2]),2))
    print(l)
    return l

def animateFigure1(i):
    global time, acc, gyro
    data = ser.readline().decode()
    while data:
        if data.startswith('Acc: '):
            acc = np.append(acc, getLength(data))
            time = time + 0.5
        elif data.startswith('Gyro: '):
            gyro = np.append(gyro, getLength(data))
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

ani = animation.FuncAnimation(fig1, animateFigure1, interval=1000)

fig2 = plt.figure()
fig2.suptitle("Angular velocity per axis")

ax_gx = fig2.add_subplot(3,1,1)
ax_gy = fig2.add_subplot(3,1,2)
ax_gz = fig2.add_subplot(3,1,3)

gyro_x = np.array([])
gyro_y = np.array([])
gyro_z = np.array([])
time_g = 0

def animateFigure2(i):
    global gyro_x, gyro_y, gyro_z, time_g
    data = ser.readline().decode()
    while data:
        if data.startswith('Gyro: '):
            temp = data.split(': ')[1].split(', ')
            gyro_x = np.append(gyro_x, float(temp[0]))
            gyro_y = np.append(gyro_y, float(temp[1]))
            gyro_z = np.append(gyro_z, float(temp[2]))
            time_g += 0.5
        data = ser.readline().decode()
    t = np.linspace(0, time_g, len(gyro_x))

    ax_gx.clear()
    ax_gx.plot(t, gyro_x)
    ax_gx.set_xlabel("Time (s)")
    ax_gx.set_ylabel("Angular velocity x-axis(rad/s)")

    ax_gy.clear()
    ax_gy.plot(t, gyro_y)
    ax_gy.set_xlabel("Time (s)")
    ax_gy.set_ylabel("Angular velocity y-axis(rad/s)")

    ax_gz.clear()
    ax_gz.plot(t, gyro_z)
    ax_gz.set_xlabel("Time (s)")
    ax_gz.set_ylabel("Angular velocity z-axis(rad/s)")

ani2 = animation.FuncAnimation(fig2, animateFigure2, interval=1000)

plt.show()