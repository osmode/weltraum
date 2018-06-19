# Weltraum 
Log and display GPS data from USB GPRS module 
on Waveshare 2.9in ePaper display

Author: Omar Metwally, MD
        omar@analog.earth

## Usage
### 1. Get USB GPRS module path
```
dmesg | grep tty
```
(On my machine, this is /dev/ttyACM0)

### 2. Log latitude and longitude to file
```
sudo python3 log_gps.py
```

### 3. Install gpsbabel
```
sudo apt-get install gpsbabel
```

### 4. Convert file from step to GPX file 
```
gpsbabel -i csv -f way.csv -o gpx -F way.gpx

alernatively, run this script:

chmod +x gen_gpx.sh
./gen_gpx.sh

```

### 5. Run on Pi boot
```
cd ~
sudo vim .bashrc
    (add this line to the bottom:)
    python /home/pi/Desktop/weltraum/main.py 
```
### 6. Display GPS coordinates on ePaper module
```
sudo python main.py
```
Notice that *main.py* is run with the Python2 interpreter


