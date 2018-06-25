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
altitude = ''
vel = ''

while True:
        try:
                line = str(ser.readline())
                print('GPS data: ',line)

                if '$GPGGA' in line:
                    line = line.split(',')
                    #print(str(line[2]), str(line[4]))
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
                    print('Longitude: ', longitude)
                    print('Latitude: ', latitude)

                    altitude = float(line[9])
                    print('Altitude: ', altitude, ' meters')
               
                if '$GPVTG' in line:
                    line = line.split(',K')
                    vel = float(line[0].split(',')[-1])
                    print('Velocity: ',str(vel),' km/hr')

                if len(str(longitude))*len(str(latitude))*len(str(altitude))*len(str(vel)) > 0:
                        print('Writing coordinates, altitude, and velocity to file...')
                        filehandle = open('/home/breitkopf/Desktop/way.csv', 'a')
                        filehandle.write(str(longitude)+', '+str(latitude)+', '+str(altitude)+', '+str(velocity)+', '+str(time())+'\n')
                        filehandle.close()
                        longitude = ''
                        latitude = ''
                        altitude = ''
                        vel = ''
        except:
                pass

