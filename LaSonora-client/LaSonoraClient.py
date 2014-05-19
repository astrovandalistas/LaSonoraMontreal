# -*- coding: utf-8 -*-

from LaSonoraUtils import populateFileListFromDbAndTag, loadDbFromJSON, _makeFakeJSON
from LaSonoraUtils import SERVER_ADDRESS, ENDPOINT_CLOCK, ENDPOINT_FILEINFO, ENDPOINT_ARCHIVE
import pygame
#from pyomxplayer import OMXPlayer
from json import loads
from urllib2 import urlopen
from random import randrange
from time import time, sleep, strptime, strftime

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
    currentState = "ice"
    currentFileList = []

def loop():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb

    _checkEvent()
    background.fill((0,0,0))

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        ## make request to server, get clock
        #inState = loads(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_CLOCK).read())
        inState = "boiling"

        ## if a new date, populate list
        if(not inState is currentState):
            currentState = inState
            currentFileList = populateFileListFromDbAndTag(fileInfoDb, currentState)
        lastMediaChangeTime = time()

        ## TODO: fade out ??
        if omx:
            omx.stop()

        ## TODO : filter by file type !?

        ## pick a file from list
        lengthOfCurrentFileList = len(currentFileList)
        if(lengthOfCurrentFileList > 0):
            randomIndex = randrange(0,lengthOfCurrentFileList)
            ## pop it from list so we don't pick again
            fileName = currentFileList.pop(randomIndex)
            ## was > 0, but now 0
            if(len(currentFileList) == 0):
                currentFileList = populateFileListFromDbAndTag(fileInfoDb, currentState)

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
