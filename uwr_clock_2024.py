# -*- coding: UTF-8 -*-

import serial
import io

ser=serial.Serial('COM4',timeout=1000)
#score=open('score.txt','w')
#time=open('time.txt','w')
#all2screen=open('all2screen.txt','w')

while True: #tämän voisi korvata jollakin IfNotAnyKeyPressed
    rawdata=ser.readline()
#    print(rawdata)      #testirivi
#    print(rawdata[2:7]) #testirivi
    rawdata_utf8=rawdata
    gametime=rawdata_utf8[2:7].decode("ascii") 
    gameStatus=rawdata_utf8[6:8].decode("ascii")
    goals_blue=rawdata_utf8[8:10].decode("ascii")
    goals_white=rawdata_utf8[11:13].decode("ascii")

    RoundNr=rawdata_utf8[15:16].decode("ascii")
    if RoundNr=='a':
        RoundNr='1'
    elif RoundNr=="b":
            RoundNr='2'
    else:
            RoundNr='E'
    
    colour=rawdata_utf8[16:17].decode("ascii")

#	jätetään nyt etunollien täyttö pois, mitä niillä tekee...       
#    ## testataan onko maalimäärä 1- vai 2-numeroinen ja poistetaan tuloksesta etunolla
    if goals_blue[0]=='0':
        goals_blue=goals_blue[1]
        if len(goals_blue) == 1:
            goals_blue = "  " + goals_blue
    if goals_white[0]=='0':
        goals_white=goals_white[1]

    with open ('erä.txt','w') as RoundNr2screen:
        RoundNr2screen.write(RoundNr)
    
    gameStatus=gameStatus[1:]
    
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

    with open ('pelikello.txt','w') as gametime2screen:
        gametime2screen.write(gametime)
    
    with open ('maalitvalkoinen.txt','w') as goalswhite:
        goalswhite.write(goals_white)

    with open ('maalitsininen.txt','w') as goalsblue:
        goalsblue.write(goals_blue)

    with open ('infobar.txt','w') as infobar:
        infobar.write(gameStatus)

ser.close()
all2screen.close()
#score.close()
#time.close()
