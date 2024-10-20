# -*- coding: UTF-8 -*-

import serial
import serial.tools.list_ports as port_list
import io
import time
import re

# assume the first available port instead of hard-coded port address
#ser=serial.Serial('COM3',timeout=1000)
ser=serial.Serial(port_list.comports()[0].device,timeout=1)


# This parses the input using regexp. Only valid inputs are processed.
def output_data(data):
    print(data)
    regex = ("^DA([ 0-9]{2}:[0-9]{2})(.{1})([0-9]{2})-([0-9]{2})([ 0-9]{2})(a|b)(b|w| )([ 0-9]{2}:[0-9]{2})" 
             "([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})")
    
    parsed = re.search(regex, data)
    if parsed:
        #print(parsed.groups())

        gametime = parsed.group(1)
        with open ('pelikello.txt','w') as gametime2screen:
            gametime2screen.write(gametime)

        goals_blue = parsed.group(3)
        with open ('maalitsininen.txt','w') as goalsblue:
            goalsblue.write(goals_blue.lstrip('0'))

        goals_white = parsed.group(4)
        with open ('maalitvalkoinen.txt','w') as goalswhite:
            goalswhite.write(goals_white.lstrip('0'))


        RoundNr = parsed.group(6)
        if RoundNr=='a':
            RoundNr='1'
        elif RoundNr=="b":
            RoundNr='2'
        else:
            RoundNr='E'
        with open ('erä.txt','w') as RoundNr2screen:
            RoundNr2screen.write(RoundNr)


        gameStatus=parsed.group(2)
        colour = parsed.group(7)
        if colour=="w":
            colour="val"
        if colour=="b":
            colour="sin"
            
        if gameStatus=="R":
            gameStatus=""
        if gameStatus=="E":
            gameStatus=""
        if gameStatus=="T":
            gameStatus="Aikalisä " + colour
        if gameStatus=="P":
            gameStatus="Rangaistuspallo " + colour

        with open ('infobar.txt','w') as infobar:
            infobar.write(gameStatus)

# Reading starts here. Can be stopped by Control-C
buffer = ""
try:
    while True: 
        # read in byte by byte, process when full buffer is received
        byte = ser.read()
        if byte:            
            char = byte.decode("ascii", errors="ignore")
            # datagram ends with newline
            if char == '\n':
                output_data(buffer)
                buffer = ""
            else:
                buffer += char
        else:
            time.sleep(1) # wait for data


except Exception as ex:
    print(str(ex))
except KeyboardInterrupt:
    print("KeyboardInterrupt")
 
# We try to close the port, but for some reason this does not work properly. The port
# remains reserved until plugged in again. 
ser.close()
time.sleep(1)
exit()
