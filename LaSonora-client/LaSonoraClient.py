# -*- coding: utf-8 -*-

from LaSonoraUtils import populateFileListFromDbAndTag, loadDbFromJSON, _makeFakeJSON
from LaSonoraUtils import SERVER_ADDRESS, ENDPOINT_CLOCK, ENDPOINT_FILEINFO, ENDPOINT_ARCHIVE
from LaSonoraUtils import initScreen
import pygame
#from pyomxplayer import OMXPlayer
from json import loads
from urllib2 import urlopen
from random import randrange
from time import time, sleep

MEDIA_CHANGE_FREQUENCY = 3

def _checkEvent():
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            raise KeyboardInterrupt

def setup():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb

    #fileInfoDb = loadDbFromJSON(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_FILEINFO).read())
    fileInfoDb = loadDbFromJSON(_makeFakeJSON())

    omx = None

    initScreen()

    lastMediaChangeTime = time()-MEDIA_CHANGE_FREQUENCY
    currentState = "ice"
    currentFileList = []

def loop():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb

    _checkEvent()

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        ## make request to server, get clock
        #inState = loads(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_CLOCK).read())
        inState = "boiling"

        ## if a new date, populate list
        if(not inState is currentState):
            currentState = inState
            currentFileList = populateFileListFromDbAndTag(fileInfoDb, currentState, ["audio", "video", "text"])
        lastMediaChangeTime = time()

        ## TODO : filter by file type !?

        ## pick a file from list
        lengthOfCurrentFileList = len(currentFileList)
        if(lengthOfCurrentFileList > 0):
            randomIndex = randrange(0,lengthOfCurrentFileList)
            ## pop it from list so we don't pick again
            fileName = currentFileList.pop(randomIndex)
            ## was > 0, but now 0
            if(len(currentFileList) == 0):
                currentFileList = populateFileListFromDbAndTag(fileInfoDb, currentState, ["audio", "video", "text"])

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
