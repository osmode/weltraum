# weltraum.py
# GPS system and odometer.
#( (C) 2018 Omar Metwally :: ANALOG LABS
# omar@analog.earth
# LICENSE: Analog Labs License (analog.earth)

import serial, sys, os
from random import randint
from time import sleep, time
import hashlib


GPS_TRACE_PATH = '/home/pi/Desktop/way.csv'

ser = serial.Serial('/dev/ttyACM0')
latitude = '' 
longitude = ''
altitude = ''
velocity = ''
velocity_whole = ''
velocity_decimals = ''
velocity_1decimals = 0.0
description = ''

last_timestamp = 0
last_velocity = 0.0
dist_traveled = 0.0

while True:
                line = str(ser.readline())
                #print('GPS data: ',line)

                if '$GPGGA' in line:
                    line = line.split(',')
                    try:
                        lat_dd = float(str(line[2])[0:2])
                        lat_mm = float(str(line[2])[2:])/60
                        latitude = lat_dd + lat_mm
                    except:
                        latitude = None

                    if len(line) >3:
                        if line[3].lower() == 's':
                            latitude = latitude * -1

                    if len(line) > 4:
                        try:
                            long_dd = float(str(line[4])[0:3]) 
                            long_mm = float(str(line[4][3:]))/60
                            longitude = long_dd + long_mm
                        except:
                            longitude = None

                    if len(line) > 5:
                        if line[5].lower() == 'w':
                            longitude = longitude * -1

                    if latitude and longitude:
                        latitude = str(latitude)
                        longitude = str(longitude)
                        #print('Longitude: ', longitude)
                        #print('Latitude: ', latitude)

                    try:
                        altitude = float(line[9])
                        #print('Altitude: ', altitude, ' meters')
                    except:
                        altitude = None
               
                if '$GPVTG' in line:
                    line = line.split(',K')
                    if len(line) > 0:
                        if ',' in line[0]:
                            try:
                                velocity = float(line[0].split(',')[-1])
                                velocity_whole = str(velocity).split('.')[0]
                                velocity_decimals = str(velocity).split('.')[1][:1]
                                velocity_1decimals = float( velocity_whole+'.'+velocity_decimals )

                                #print('Velocity: ',str(velocity),' km/hr')
                            except: pass

                if (last_timestamp == 0) and velocity:
                    last_timestamp = time()
                    last_velocity = velocity_1decimals
                elif velocity:
                    delta_time = float( time() - last_timestamp )
                    dist_traveled += ( float(last_velocity) * float((delta_time / 3600)) * 1000)
                    last_timestamp = time()
                    last_velocity = velocity_1decimals

                if len(str(longitude))*len(str(latitude)) > 0:
                        display_string = ''
                        display_string += 'Latitude: '+latitude[:8]+' \n'
                        display_string += 'Long: '+longitude[:8]+' \n'
                        display_string += 'Altitude: '+str(altitude)+' meters \n'
                        display_string += 'Velocity: '+str(velocity)+' km/h \n'
                        display_string += 'Distance: '+str(dist_traveled)+'\n'

                        #print('display_string before formatting: ',display_string)
                        print(display_string)

                        filehandle = open(GPS_TRACE_PATH, 'a')
                        filehandle.write(str(longitude)+', '+str(latitude)+', '+str(altitude)+', '+str(velocity)+', '+str(dist_traveled)+', '+str(time())+', '+description+'\n')
                        filehandle.close()

                        longitude =''
                        latitude = ''
                        altitude = ''
                        velocity = ''

