# -*- coding: UTF-8 -*-

import serial
import serial.tools.list_ports as port_list
import io
import time
import re


# This parses the input using regexp. Only valid inputs are processed.
regex = re.compile("^DA([ 0-9]{2}:[0-9]{2})(.{1})([0-9]{2})-([0-9]{2})([ 0-9]{2})(a|b)(b|w| )([ 0-9]{2}:[0-9]{2})" 
                   "([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})([ 0-9]{2}:[0-9]{2})")
def output_data(data):
    parsed = regex.search(data)
    if parsed:
        print(data)
        #print(parsed.groups())

        gametime = parsed.group(1)
        with open ('pelikello.txt','w') as gametime2screen:
            gametime2screen.write(gametime)

        goals_blue = parsed.group(3)
        with open ('maalitsininen.txt','w') as goalsblue:
            goalsblue.write(goals_blue.lstrip('0') or '0')

        goals_white = parsed.group(4)
        with open ('maalitvalkoinen.txt','w') as goalswhite:
            goalswhite.write(goals_white.lstrip('0') or '0')


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
            
        if gameStatus==" ":
            gameStatus="" # Waiting to be started
        if gameStatus=="R":
            gameStatus="" # Game Running
        if gameStatus=="E":
            gameStatus="Puoliaika"
        if gameStatus=="T":
            gameStatus="Aikalisä " + colour
        if gameStatus=="P":
            gameStatus="Rangaistuspallo " + colour

        with open ('infobar.txt','w') as infobar:
            infobar.write(gameStatus)

        bluePenalties = []
        for p in filter(lambda i: i != "  :00", [parsed.group(8),parsed.group(9),parsed.group(10)]):
            bluePenalties.append(p.lstrip())
        with open ('jäähytsininen.txt','w') as penaltiesblue:
            penaltiesblue.write(', '.join(bluePenalties))

        whitePenalties = []
        for p in filter(lambda i: i != "  :00", [parsed.group(11),parsed.group(12),parsed.group(13)]):
            whitePenalties.append(p.lstrip())
        with open ('jäähytvalkoinen.txt','w') as penaltieswhite:
            penaltieswhite.write(', '.join(whitePenalties))

# Open comport
try:
    # assume the first available port instead of hard-coded port address
    #ser=serial.Serial('COM3',timeout=1000)
    ser=serial.Serial(port_list.comports()[0].device,timeout=1)
except Exception as ex:
    print(ex)
    time.sleep(5) # to show error message before window is closed
    exit()

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
    print(ex)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    pass
 
# We try to close the port, but for some reason this does not work properly. The port
# remains reserved until plugged in again. 
ser.close()
time.sleep(5) # to show error message before window is closed
exit()
