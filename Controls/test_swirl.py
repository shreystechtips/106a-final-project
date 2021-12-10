import numpy as np
import serial
import time

# Make sure to run sudo chmod 777 /dev/ttyACM1

ser = serial.Serial('/dev/ttyACM0', 115200)
ser.baudrate = 115200
# move to center to start
time.sleep(2)

# create spiral with width of 10
x = 160
y = 160
i = 0
prev_x = x
direction = 1
while i <= 120:
    ser.write(bytes(f'G1 X{prev_x} Y{y + i} F2500\r\n', 'utf-8')) #move up
    time.sleep(.015*i + .2)
    ser.write(bytes(f'G1 X{x + i} Y{y + i} F2500\r\n', 'utf-8')) #move right
    time.sleep(.015*i + .2)
    prev_x = x + i
    i += 10
    ser.write(bytes(f'G1 X{prev_x} Y{y - i} F2500\r\n', 'utf-8')) #move up
    time.sleep(.015*i + .2)
    ser.write(bytes(f'G1 X{x - i} Y{y - i} F2500\r\n', 'utf-8')) #move right
    time.sleep(.015*i + .2)
    prev_x = x - i
    i += 10
    print(i)
print("escaped loop1")
while i >= 0:
    ser.write(bytes(f'G1 X{prev_x} Y{y + i} F2500\r\n', 'utf-8')) #move up
    time.sleep(.015*i + .2)
    ser.write(bytes(f'G1 X{x + i} Y{y + i} F2500\r\n', 'utf-8')) #move right
    time.sleep(.015*i + .2)
    prev_x = x + i
    i -= 10
    ser.write(bytes(f'G1 X{prev_x} Y{y - i} F2500\r\n', 'utf-8')) #move up
    time.sleep(.015*i + .2)
    ser.write(bytes(f'G1 X{x - i} Y{y - i} F2500\r\n', 'utf-8')) #move right
    time.sleep(.015*i + .2)
    prev_x = x - i
    i -= 10
    print(i)
print("escaped loop2")

time.sleep(2)
ser.write(bytes('G1 X0 Y0 F2500\r\n', 'utf-8'))
time.sleep(2)
ser.close()

# def send_to_coords(coords: np.array):
#     ''' Moves magnet mechanism to specify coordinates in "coords"
#         Input coords in a np.array of size (2,) representing x, y in millimeters in workspace frame 
#     '''
# command = f'G01 X{coords[0]} Y{coords[1]}'
#     ser.println(command)
#     ser.write(bytes(command, 'utf-8'))


