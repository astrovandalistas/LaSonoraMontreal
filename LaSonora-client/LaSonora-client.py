# -*- coding: utf-8 -*-

import pygame
from pyomxplayer import OMXPlayer
from time import time, sleep
from os import path, listdir

MEDIA_CHANGE_FREQUENCY = 3
LOCATION_FILTER = ["MEXICO", "RUSSIA"]
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

def _populateFileList():
    global currentDateFiles, currentDateValue

    datePath = "./data/"+currentDateValue
    if(path.isdir(datePath)):
        currentDateFiles = []
        ## if no country filter, pick from all countries 
        if((not LOCATION_FILTER) and (currentDateValue in DATE_FILTER)):
            locations = [ l for l in listdir(datePath) if path.isdir(datePath+"/"+l)]
            for l in locations:
                currentDateFiles.extend([datePath+"/"+l+"/"+f for f in listdir(datePath+"/"+l) if path.isfile(datePath+"/"+l+"/"+f)])
        ## country filter 
        for l in LOCATION_FILTER:
            if(path.isdir(datePath+"/"+l)):
                currentDateFiles.extend([datePath+"/"+l+"/"+f for f in listdir(datePath+"/"+l) if path.isfile(datePath+"/"+l+"/"+f)])

        ## what we got?
        print "files: %s" % (currentDateFiles)

def loop():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastMediaChangeTime, currentDateValue, currentDateFiles

    _checkEvent()
    background.fill((0,0,0))

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        ## TODO: make request to server, get JSON
        inDateValue = "2010-01"

        ## if a new date, populate list
        if(not inDateValue is currentDateValue):
            currentDateValue = inDateValue    
            _populateFileList()
        lastMediaChangeTime = time()

        ## TODO: fade out ??
        if omx:
            omx.stop()

        ## TODO: pick a file from list
        ##       use a filter for file type
        ##       pop it from list so we don't pick again
        ##       if it was the lst one, populate list again
        pass

        ## TODO: play audio/video
        #omx = OMXPlayer('./data/vids/vd1.mp4')
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
