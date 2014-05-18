# -*- coding: utf-8 -*-

from LaSonoraUtils import populateFileListFromFileInfoData, readAndFormatJSON, _makeFakeJSON
import pygame
from pyomxplayer import OMXPlayer
from json import loads
from urllib2 import urlopen
from random import randrange
from time import time, sleep, strptime, strftime

SERVER_ADDRESS = "http://foocoop.mx:1337"
ENDPOINT_CLOCK = "clock/currentddmmyy"
ENDPOINT_FILEINFO = "media"
ENDPOINT_ARCHIVE = "uploads"

MEDIA_CHANGE_FREQUENCY = 3
LOCATION_FILTER = ["mexico", "russia"]
DATE_FILTER = ["2010-01", "2012-02"]

def _checkEvent():
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            raise KeyboardInterrupt

def setup():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentDateValue, currentDateFiles
    global fileInfoData

    fileInfoData = readAndFormatJSON(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_FILEINFO).read())
    #fileInfoData = _readAndFormatJSON(_makeFakeJSON())

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

    lastMediaChangeTime = time()-MEDIA_CHANGE_FREQUENCY
    currentDateValue = "1900-00"
    currentDateFiles = []

def loop():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentDateValue, currentDateFiles
    global fileInfoData

    _checkEvent()
    background.fill((0,0,0))

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        ## make request to server, get clock
        inDateValueList = loads(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_CLOCK).read()).split('/')
        inDateValue = inDateValueList[2]+'-'+inDateValueList[1]

        ## if a new date, populate list
        if(not inDateValue is currentDateValue):
            currentDateValue = inDateValue    
            currentDateFiles = populateFileListFromFileInfoData(currentDateValue, fileInfoData)
        lastMediaChangeTime = time()

        ## TODO: fade out ??
        if omx:
            omx.stop()

        ## TODO : filter by file type !?

        ## pick a file from list
        lengthOfCurrentDateFiles = len(currentDateFiles)
        if(lengthOfCurrentDateFiles > 0):
            randomIndex = randrange(0,lengthOfCurrentDateFiles)
            ## pop it from list so we don't pick again
            fileName = currentDateFiles.pop(randomIndex)
            ## was > 0, but now 0
            if(len(currentDateFiles) == 0):
                currentDateFiles = populateFileListFromFileInfoData(currentDateValue, fileInfoData)

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
