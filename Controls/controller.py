import numpy as np
import serial

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200

def send_to_coords(coords: np.array):
    ''' Moves magnet mechanism to specify coordinates in "coords"
        Input coords in a np.array of size (2,) representing x, y in millimeters in workspace frame 
    '''
    command = f'G01 X{coords[0]} Y{coords[1]}'
    ser.write(bytes(command, 'utf-8'))

