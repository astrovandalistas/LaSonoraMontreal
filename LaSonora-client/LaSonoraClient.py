# -*- coding: utf-8 -*-

from LaSonoraUtils import populateFileListFromDbAndTag, loadDbFromJSON, _makeFakeJSON
from LaSonoraUtils import SERVER_ADDRESS, ENDPOINT_WORD, ENDPOINT_FILEINFO, ENDPOINT_ARCHIVE
from LaSonoraUtils import initScreen, stopAudio, stopVideo, clearScreen, playAudio, playVideo, displayImage, displayText
import pygame
from json import loads
from urllib2 import urlopen
from random import randrange
from time import time, sleep

MEDIA_CHANGE_FREQUENCY = 5
MEDIA_TO_PLAY = ["text", "audio", "video", "image"]

def _checkEvent():
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            raise KeyboardInterrupt

def setup():
    global video, audio
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb

    fileInfoDb = loadDbFromJSON(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_FILEINFO).read())

    video = None
    audio = None

    initScreen()

    lastMediaChangeTime = time()-MEDIA_CHANGE_FREQUENCY
    currentState = "ice"
    currentFileList = []

def loop():
    global video, audio
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb

    _checkEvent()

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        ## make request to server, get clock
        inState = urlopen(SERVER_ADDRESS+"/"+ENDPOINT_WORD).read()
        print inState

        ## if a new date, populate list
        if(not inState == currentState):
            currentState = inState
            currentFileList = populateFileListFromDbAndTag(fileInfoDb, currentState, MEDIA_TO_PLAY)
        lastMediaChangeTime = time()

        ## pick a file from list
        nextFile = ()
        lengthOfCurrentFileList = len(currentFileList)
        if(lengthOfCurrentFileList > 0):
            randomIndex = randrange(0,lengthOfCurrentFileList)
            ## pop it from list so we don't pick again
            nextFile = currentFileList.pop(randomIndex)
            ## was > 0, but now 0
            if(len(currentFileList) == 0):
                currentFileList = populateFileListFromDbAndTag(fileInfoDb, currentState, MEDIA_TO_PLAY)

        stopAudio(audio)
        stopVideo(video)
        clearScreen()

        if(nextFile is ()):
            return

        if(nextFile[0] == "audio"):
            audio = playAudio(nextFile[1])
        elif(nextFile[0] == "video"):
            video = playVideo(nextFile[1], fileInfoDb)
        elif(nextFile[0] == "image"):
            displayImage(nextFile[1])
        elif(nextFile[0] == "text"):
            displayText(nextFile[1])

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
        stopAudio(audio)
        stopVideo(video)
        clearScreen()
        exit(0)
