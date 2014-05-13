# -*- coding: utf-8 -*-

import pygame
from pyomxplayer import OMXPlayer
from json import loads, dumps
from urllib2 import urlopen
from random import randrange
from time import time, sleep, strptime, strftime
from os import path, listdir

SERVER_ADDRESS = "http://astrovandalistas.cc/sonoratelematica"
ENDPOINT_CLOCK = "reloj"
ENDPOINT_FILEINFO = "dbinfo"

MEDIA_CHANGE_FREQUENCY = 3
LOCATION_FILTER = ["mexico", "russia"]
DATE_FILTER = ["2010-01", "2012-02"]

def _checkEvent():
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            raise KeyboardInterrupt

def _makeFakeJSON():
    fakeData = []
    fakeData.append({"fecha": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "lugar":"brazil", "url":"bdjdjdj.wav"})
    fakeData.append({"fecha": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "lugar":"brazil", "url":"bfoo.txt"})
    fakeData.append({"fecha": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "lugar":"brazil", "url":"bhahaha.mp3"})
    fakeData.append({"fecha": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "lugar":"mexico", "url":"mdjdjdj.wav"})
    fakeData.append({"fecha": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "lugar":"mexico", "url":"mfoo.txt"})
    fakeData.append({"fecha": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "lugar":"mexico", "url":"mhahaha.mp3"})

    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"brazil", "url":"b1djdjdj.wav"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"brazil", "url":"b1foo.txt"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"brazil", "url":"b1hahaha.mp3"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"mexico", "url":"m1djdjdj.wav"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"mexico", "url":"m1hahaha.mp3"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"russia", "url":"r1djdjdj.wav"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"russia", "url":"r1foo.txt"})
    fakeData.append({"fecha": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "lugar":"russia", "url":"r1hahaha.mp3"})

    return dumps(fakeData)

def _readAndFormatJSON(jsonFromServer):
    result = {}
    fileInfoFromServer = loads(jsonFromServer)

    for d in [ e for e in fileInfoFromServer if ("fecha" in e and "lugar" in e and "url" in e) ]:
        ## "Wed May 21 2014 00:00:00 GMT-0500 (CDT)"
        date = strftime("%Y-%m", strptime(" ".join(d["fecha"].split()[:4]), "%a %b %d %Y"))
        if(not date in result):
            result[date] = {}
        if(not d["lugar"] in result[date]):
                result[date][d["lugar"]] = []
        result[date][d["lugar"]].append(d["url"])

    return result

def setup():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentDateValue, currentDateFiles
    global fileInfoData

    ## TODO: rsync

    #fileInfoData = _readAndFormatJSON(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_FILEINFO).read())
    fileInfoData = _readAndFormatJSON(_makeFakeJSON())

    omx = None

    pygame.init()
    #screen = pygame.display.set_mode((0, 0), (pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE))
    screen = pygame.display.set_mode((0, 0), (pygame.DOUBLEBUF|pygame.HWSURFACE))
    pygame.display.set_caption('LaSonora')
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    font = pygame.font.Font("./data/arial.ttf", 800)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    mSurface = font.render("La Sonora Telematica ", 1, (200,200,200), (0,0,0))
    mSurfaceRect = mSurface.get_rect()
    scale = min(float(background.get_width())/mSurfaceRect.width, float(mSurfaceRect.width)/background.get_width())
    mSurface = pygame.transform.scale(mSurface,(int(scale*mSurfaceRect.width),int(scale*mSurfaceRect.height)))
    mSurfaceRect = mSurface.get_rect(centerx=background.get_width()/2,
                                     centery=background.get_height()/2)

    lastMediaChangeTime = time()
    currentDateValue = "1900-00"
    currentDateFiles = []

def _populateFileListFromLocalDir():
    global currentDateFiles, currentDateValue

    currentDateFiles = []

    datePath = "./data/"+currentDateValue
    if(path.isdir(datePath)):
        ## if no country filter, but date, pick from all countries
        if((not LOCATION_FILTER) and (currentDateValue in DATE_FILTER)):
            locations = [ l for l in listdir(datePath) if path.isdir(datePath+"/"+l)]
            for l in locations:
                currentDateFiles.extend([datePath+"/"+l+"/"+f for f in listdir(datePath+"/"+l) if path.isfile(datePath+"/"+l+"/"+f)])
        ## country filter 
        for l in LOCATION_FILTER:
            if(path.isdir(datePath+"/"+l)):
                currentDateFiles.extend([datePath+"/"+l+"/"+f for f in listdir(datePath+"/"+l) if path.isfile(datePath+"/"+l+"/"+f)])

        ## print what we got
        print "files: %s" % (currentDateFiles)

def _populateFileListFromFileInfoData():
    global currentDateFiles, currentDateValue
    global fileInfoData

    currentDateFiles = []

    dataPath = "./data"
    if(currentDateValue in fileInfoData):
        ## if no country filter, but date, pick from all countries
        if((not LOCATION_FILTER) and (currentDateValue in DATE_FILTER)):
            for l in fileInfoData[currentDateValue]:
                currentDateFiles.extend([dataPath+"/"+f for f in fileInfoData[currentDateValue][l]])
        ## country filter
        for l in LOCATION_FILTER:
            if(l in fileInfoData[currentDateValue]):
                currentDateFiles.extend([dataPath+"/"+f for f in fileInfoData[currentDateValue][l]])

        ## print what we got
        print "files: %s" % (currentDateFiles)

def loop():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentDateValue, currentDateFiles
    global fileInfoData

    _checkEvent()
    background.fill((0,0,0))

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        ## TODO: make request to server, get JSON
        #inDateValue = loads(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_CLOCK).read())['reloj']
        inDateValue = "2010-01"

        ## if a new date, populate list
        if(not inDateValue is currentDateValue):
            currentDateValue = inDateValue    
            _populateFileListFromFileInfoData()
        lastMediaChangeTime = time()

        ## TODO: fade out ??
        if omx:
            omx.stop()

        ## TODO : filter by file type !?

        ## pick a file from list
        lengthOfCurrentDateFiles= len(currentDateFiles)
        randomIndex = randrange(0,lengthOfCurrentDateFiles)
        ## pop it from list so we don't pick again
        fileName = currentDateFiles.pop(randomIndex)
        ## if it was the lst one, populate list again
        if((lengthOfCurrentDateFiles > 0) and (len(currentDateFiles) == 0)):
            _populateFileListFromFileInfoData()

        ## play audio/video
        #omx = OMXPlayer(fileName)
        pass

        ## TODO: play text
        pass

if __name__=="__main__":
    setup()
    try:
        while(True):
            loopStart = time()
            loop()
            loopTime = time()-loopStart
            if (loopTime < 0.016):
                sleep(0.016 - loopTime)
        exit(0)
    except KeyboardInterrupt:
        if omx:
            omx.stop()
        exit(0)
