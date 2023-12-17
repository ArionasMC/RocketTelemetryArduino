import serial
import matplotlib.pyplot as plt
import numpy as np
import math

ser = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)
print(ser.is_open)

acc = np.array([])
gyro = np.array([])

def getLength(data):
    temp = data.split(': ')[1].split(', ')
    #print(temp)
    l = math.sqrt(math.pow(float(temp[0]),2) + math.pow(float(temp[1]),2) + math.pow(float(temp[2]),2))
    print(l)
    return l

time = 0

try:
    while True:
        data = ser.readline().decode()
        if data.startswith('Acc: '):
            acc = np.append(acc, getLength(data))
            time = time + 0.5
        elif data.startswith('Gyro: '):
            gyro = np.append(gyro, getLength(data))
            time = time + 0.5

except KeyboardInterrupt: # press CTRL+C to exit
    pass  

print('Successfully stopped reading data')
print('Acc size:',len(acc),"Gyro size:",len(gyro))

s = len(acc)
t = np.linspace(0, time, s)

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('A tale of 2 subplots')

ax1.plot(t, acc, linewidth=2.0)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Acceleration (m/s^2)")

ax2.plot(t, gyro, linewidth=2.0)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Angular velocity (rad/s)")

plt.show()