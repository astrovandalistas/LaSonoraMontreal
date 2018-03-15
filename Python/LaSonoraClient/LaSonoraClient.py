# -*- coding: utf-8 -*-

from LaSonoraUtils import populateFileListFromDbAndTag, loadDbFromJSON, _makeFakeJSON
from LaSonoraUtils import SERVER_ADDRESS, ENDPOINT_WORD, ENDPOINT_WORD_INIT, ENDPOINT_FILEINFO, ENDPOINT_ARCHIVE
from LaSonoraUtils import initScreen, stopAudio, stopVideo, clearScreen, playAudio, playVideo, displayImage, displayText
import pygame
from json import loads, dumps
from urllib2 import urlopen
from random import randrange
from time import time, sleep

MEDIA_CHANGE_FREQUENCY = 15
MEDIA_TO_PLAY = ["text", "audio", "video", "image"]

def _checkEvent():
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            raise KeyboardInterrupt

def setup():
    global video, audio
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb, lastNonFrozenStateTime

    try:
        fileInfoDb = loadDbFromJSON(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_FILEINFO, timeout=2).read())
    except:
        fileInfoDb = loadDbFromJSON(dumps({}))
        print "can't open %s" % (SERVER_ADDRESS+"/"+ENDPOINT_FILEINFO)

    video = None
    audio = None

    initScreen()

    lastMediaChangeTime = time()-MEDIA_CHANGE_FREQUENCY
    currentState = "ice"
    lastNonFrozenStateTime = time()
    currentFileList = []

def loop():
    global video, audio
    global lastMediaChangeTime, currentState, currentFileList
    global fileInfoDb, lastNonFrozenStateTime

    _checkEvent()

    if(time() - lastMediaChangeTime > MEDIA_CHANGE_FREQUENCY):
        if(time()-lastNonFrozenStateTime > 45):
            try:
                response = urlopen(SERVER_ADDRESS+"/"+ENDPOINT_WORD_INIT, timeout=2).read()
                lastNonFrozenStateTime = time()
            except:
                print "can't do word init"

        try:
            ## make request to server, get clock
            inState = urlopen(SERVER_ADDRESS+"/"+ENDPOINT_WORD, timeout=2).read()
            print inState
        except:
            inState = "frozen"
            print "can't open %s" % (SERVER_ADDRESS+"/"+ENDPOINT_WORD)

        if(not inState == "frozen"):
            lastNonFrozenStateTime = time()

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
