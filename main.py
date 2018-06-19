import epd2in9b
from PIL import Image, ImageFont, ImageDraw
import serial, sys, os
from time import sleep, time
#import imagedata

COLORED = 1
UNCOLORED = 0

def main():
    epd = epd2in9b.EPD()
    epd.init()

    # clear the frame buffer
    frame_black = [0xFF] * (epd.width * epd.height / 8)
    frame_red = [0xFF] * (epd.width * epd.height / 8)

    # For simplicity, the arguments are explicit numerical coordinates
    '''
    epd.draw_rectangle(frame_black, 10, 80, 50, 140, COLORED);
    epd.draw_line(frame_black, 10, 80, 50, 140, COLORED);
    epd.draw_line(frame_black, 50, 80, 10, 140, COLORED);
    epd.draw_circle(frame_black, 90, 110, 30, COLORED);
    epd.draw_filled_rectangle(frame_red, 10, 180, 50, 240, COLORED);
    epd.draw_filled_rectangle(frame_red, 0, 6, 128, 26, COLORED);
    epd.draw_filled_circle(frame_red, 90, 210, 30, COLORED);
    '''

    # write strings to the buffer
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 16)
    epd.draw_string_at(frame_black, 4, 30, "Weltraum... ", font, COLORED)
    epd.draw_string_at(frame_red, 6, 10, "", font, UNCOLORED)
    # display the frames
    epd.display_frame(frame_black, frame_red)

    # display images
    #frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
    #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
    #epd.display_frame(frame_black, frame_red)

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.IMAGE_BLACK, imagedata.IMAGE_RED)

    print 'Starting weltraum...'
    print 'Reading GPS coordinates from connected device...'
    ser = serial.Serial('/dev/ttyACM0')
    latitude = ''
    longitude = ''

    while 1:
        line = str(ser.readline())
        print 'GPS data:', line
        try:
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

                print 'Latitude: ', latitude
                print 'Longitude: ', longitude
                filehandle = open('/home/pi/Desktop/way.csv', 'a')
                filehandle.write(str(latitude)+', '+str(longitude)+', '+ str(time())+'\n')
                filehandle.close()
                                                        
                # clear the frame buffer
                frame_black = [0xFF] * (epd.width * epd.height / 8)
                frame_red = [0xFF] * (epd.width * epd.height / 8)
                #frame_red = [0xFF] * (epd.width * epd.height / 8)
                display_string = 'WELTRAUM\n\nGPS coords:\n'+str(latitude)+'\n'+str(longitude)+'\n\nANALOG.EARTH\nTO CONSENSUS\nAND BEYOND!'
                epd.draw_string_at(frame_black, 4, 30, display_string ,font, COLORED)
                #epd.draw_string_at(frame_red, 6, 10, "Long: "+longitude, font, UNCOLORED)
                # display the frames
                epd.display_frame(frame_black, frame_red)
                sleep(10)
        except:
            pass

if __name__ == '__main__':
    main()
