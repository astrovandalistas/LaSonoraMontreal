from json import loads, dumps
from os import path, listdir, remove
from urllib2 import urlopen
from peewee import *

SERVER_ADDRESS = "http://foocoop.mx:1337"
ENDPOINT_CLOCK = "clock/currentddmmyy"
ENDPOINT_FILEINFO = "media"
ENDPOINT_ARCHIVE = "uploads"

class MediaFileDb(Model):
    fileName = CharField()
    hasSound = BooleanField()
    waterState = CharField()
    typeOfMedia = CharField()
    title = BlobField()
    date = CharField()
    country = CharField()
    class Meta:
        database = SqliteDatabase('./data/tmp.db')

def populateFileListFromDbAndTag(dataBase, tag):
    currentFiles = []

    dataPath = "./data"
    for f in dataBase.select().where(MediaFileDb.waterState == tag):
        currentFiles.append(dataPath+"/"+f.fileName)

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
                "waterstate" in e and
                "title" in e and
                "typeofmedia" in e and
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
                            waterState = d['waterstate'],
                            typeOfMedia = d['typeofmedia'],
                            title = d['title'],
                            date = d['date'],
                            country = d['country'])
    return MediaFileDb

def _makeFakeJSON():
    fakeData = []
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b0.mov",
                    "waterstate":"boiling",
                    "typeofmedia":"water",
                    "title":"foo video 1",
                    "hassound":True})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b1.mov",
                    "waterstate":"boiling",
                    "typeofmedia":"water",
                    "title":"foo video 2",
                    "hassound":False})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b0w.wav",
                    "waterstate":"boiling",
                    "typeofmedia":"water",
                    "title":"fooo audio",
                    "hassound":True})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b0j.jpg",
                    "waterstate":"ice",
                    "typeofmedia":"water",
                    "title":"hey hey hey image",
                    "hassound":True})
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)',
                    "country":"brazil",
                    "filename":"b0m.mp4",
                    "waterstate":"rain",
                    "typeofmedia":"water",
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
