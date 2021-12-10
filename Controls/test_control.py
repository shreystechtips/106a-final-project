import numpy as np
import serial
import time

ser = serial.Serial('/dev/ttyACM1', 115200, timeout = 0.5)
ser.baudrate = 115200

time.sleep(2)
ser.write(bytes('G1 X10 Y20 F2000\r\n', 'utf-8'))
time.sleep(1)
ser.write(bytes('G1 X0 Y0 F2000\r\n', 'utf-8'))
time.sleep(1)
ser.write(bytes('G1 X100 Y100 F2000\r\n', 'utf-8'))
time.sleep(1)
ser.write(bytes('G1 X50 Y50 F2000\r\n', 'utf-8'))
time.sleep(1)
ser.write(bytes('G1 X200 Y200 F2000\r\n', 'utf-8'))
time.sleep(1)
ser.close()
