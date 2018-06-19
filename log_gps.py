# log_gps.py
# Read GPS coordinates from USB module in real time and
# Log coordinates to file 
# Author: Omar Metwally, MD 
#         omar@analog.earth
# License: MIT

import serial, sys, os
from time import time

ser = serial.Serial('/dev/ttyACM0')
latitude = ''
longitude = ''

while True:
        line = str(ser.readline())
        print('GPS data: ',line)
        if '$GPGGA' in line:
            line = line.split(',')
            print(str(line[2]), str(line[4]))
            lat_dd = float(str(line[2])[0:2])
            lat_mm = float(str(line[2])[2:])/60
            latitude = lat_dd + lat_mm
            if line[3].lower() == 's':
                latitude = latitude * -1

            long_dd = float(str(line[4])[0:3]) 
            long_mm = float(str(line[4][3:]))/60
            longitude = long_dd + long_mm
            if line[5].lower() == 'w':
                longitude = longitude * -1

            print('Latitude: ', latitude)
            print('Longitude: ', longitude)
            filehandle = open('/home/pi/Desktop/way.csv', 'a')
            filehandle.write(str(latitude)+', '+str(longitude)+', '+ str(time())+'\n')
            filehandle.close()
