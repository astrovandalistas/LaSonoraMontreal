from json import loads, dumps
from os import path, listdir, remove
from urllib2 import urlopen
from peewee import *
from subprocess import Popen, PIPE
import pygame

SERVER_ADDRESS = "http://foocoop.mx:1337"
ENDPOINT_CLOCK = "clock/currentddmmyy"
ENDPOINT_FILEINFO = "media"
ENDPOINT_ARCHIVE = "uploads"

class MediaFileDb(Model):
    fileName = CharField()
    hasSound = BooleanField()
    waterType = CharField()
    mediaType = CharField()
    contentType = CharField()
    title = BlobField()
    date = CharField()
    country = CharField()
    class Meta:
        database = SqliteDatabase('./data/tmp.db')

def populateFileListFromDbAndTag(dataBase, tag, mediaTypes):
    currentFiles = []

    dataPath = "./data"
    for f in dataBase.select().where(MediaFileDb.waterType == tag):
        if(f.mediaType in mediaTypes):
            if(f.mediaType is "text"):
                currentFiles.append((f.mediaType, f.contentText))
            else:
                currentFiles.append((f.mediaType, dataPath+"/"+f.fileName))

    ## print what we got
    print "current files: %s" % (currentFiles)
    return currentFiles

def loadDbFromJSON(jsonFromServer):
    if(path.isfile('./data/tmp.db')):
        remove('./data/tmp.db')
    MediaFileDb.create_table()
    fileInfoFromServer = loads(jsonFromServer)

    def isValidEntry(e):
        return ("date" in e and
                "country" in e and
                "filename" in e and
                "waterType" in e and
                "contentText" in e and
                "title" in e and
                "mediaType" in e and
                "contentType" in e and
                "hassound" in e)

    for d in [ e for e in fileInfoFromServer if isValidEntry(e)]:
        ## keep files consistent with server db
        if(not path.isfile('./data/'+d['filename'])):
            try:
                f = open('./data/'+d['filename'], 'wb')
                f.write(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_ARCHIVE+"/"+d['filename']).read())
            except:
                print "couldn't download %s" % str(SERVER_ADDRESS+"/"+ENDPOINT_ARCHIVE+"/"+d['filename'])
            finally:
                f.close()

        MediaFileDb.create(fileName = d['filename'],
                            hasSound = (d['hassound'] is "True"),
                            waterType = d['waterType'],
                            contentType = d['contentType'],
                            title = d['title'],
                            date = d['date'],
                            contentText = d['contentText'],
                            mediaType = d['mediaType'],
                            country = d['country'])
    return MediaFileDb

def initScreen():
    global pyScreen, font, mSurface, mSurfaceRect
    pygame.init()

    #pyScreen = pygame.display.set_mode((0, 0), (pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE))
    pyScreen = pygame.display.set_mode((0, 0), (pygame.DOUBLEBUF|pygame.HWSURFACE))
    pygame.display.set_caption('LaSonora')
    pygame.mouse.set_visible(False)

    background = pygame.Surface(pyScreen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    font = pygame.font.Font("./data/arial.ttf", 800)
    pyScreen.blit(background, (0, 0))
    pygame.display.flip()

    mSurface = font.render("La Sonora Telematica ", 1, (200,200,200), (0,0,0))
    mSurfaceRect = mSurface.get_rect()
    scale = min(float(background.get_width())/mSurfaceRect.width, float(mSurfaceRect.width)/background.get_width())
    mSurface = pygame.transform.scale(mSurface,(int(scale*mSurfaceRect.width),int(scale*mSurfaceRect.height)))
    mSurfaceRect = mSurface.get_rect(centerx=background.get_width()/2,
                                     centery=background.get_height()/2)

def clearScreen():
    global pyScreen
    background = pygame.Surface(pyScreen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    pyScreen.blit(background, (0, 0))
    pygame.display.flip()
def stopAudio(audioPlayer):
    if(audioPlayer):
        audioPlayer.stdin.write('q')
def stopVideo(videoPlayer):
    if(videoPlayer):
        videoPlayer.stop()
def playAudio(fileName):
    return Popen(["mplayer", fileName], stdin=PIPE, stdout=PIPE, stderr=PIPE)
def playVideo(fileName, db):
    pass
def displayImage(fileName):
    background = pygame.Surface(pyScreen.get_size())
    img=pygame.image.load(fileName)
    imgRect = img.get_rect()
    pyScreen.blit(img,((background.get_width()-imgRect.width)/2 ,(background.get_height()-imgRect.height)/2))
    pygame.display.flip()
def displayText(text):
    pass

def _makeFakeJSON():
    fakeData = []
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b0.mov",
                    "waterType":"boiling",
                    "contentType":"water",
                    "mediaType":"video",
                    "contentText":"hello hello text test",
                    "title":"foo video 1",
                    "hassound":True})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b1.mov",
                    "contentText":"hello hello text test",
                    "waterType":"boiling",
                    "contentType":"water",
                    "mediaType":"video",
                    "title":"foo video 2",
                    "hassound":False})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b0w.wav",
                    "waterType":"boiling",
                    "contentType":"water",
                    "mediaType":"audio",
                    "contentText":"hello hello text test",
                    "title":"fooo audio",
                    "hassound":True})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"image0.jpg",
                    "waterType":"ice",
                    "contentType":"water",
                    "mediaType":"image",
                    "contentText":"hello hello text test",
                    "title":"hey hey hey image",
                    "hassound":False})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"image1.jpg",
                    "waterType":"boiling",
                    "contentType":"water",
                    "mediaType":"image",
                    "contentText":"hello hello text test",
                    "title":"hey hey hey image",
                    "hassound":False})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"image2.jpg",
                    "waterType":"boiling",
                    "contentType":"water",
                    "mediaType":"image",
                    "contentText":"hello hello text test",
                    "title":"hey hey hey image",
                    "hassound":False})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "waterType":"rain",
                    "contentType":"water",
                    "mediaType":"text",
                    "contentText":"hello hello text test",
                    "title":"foo video 4",
                    "hassound":False})

    return dumps(fakeData)

def _makeFakeJSON1():
    fakeData = []
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "country":"brazil", "filename":"bfoo.txt"})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "country":"brazil", "filename":"bhahaha.mp3"})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "country":"mexico", "filename":"mdjdjdj.wav"})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "country":"mexico", "filename":"mfoo.txt"})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "country":"mexico", "filename":"mhahaha.mp3"})

    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"brazil", "filename":"b1djdjdj.wav"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"brazil", "filename":"b1foo.txt"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"brazil", "filename":"b1hahaha.mp3"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"mexico", "filename":"m1djdjdj.wav"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"mexico", "filename":"m1hahaha.mp3"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"russia", "filename":"r1djdjdj.wav"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"russia", "filename":"r1foo.txt"})
    fakeData.append({"date": 'Wed Feb 21 2012 00:00:00 GMT-0500 (CDT)', "country":"russia", "filename":"r1hahaha.mp3"})

    return dumps(fakeData)
