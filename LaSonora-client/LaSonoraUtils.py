from json import loads, dumps
from os import path, listdir

def populateFileListFromLocalDir(currentDateValue):
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
    return currentDateFiles

def populateFileListFromFileInfoData(currentDateValue, fileInfoData):
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
    return currentDateFiles

def readAndFormatJSON(jsonFromServer):
    result = {}
    fileInfoFromServer = loads(jsonFromServer)

    for d in [ e for e in fileInfoFromServer if ("date" in e and "country" in e and "filename" in e) ]:
        ## keep files consistent with server db
        if(not path.isfile('./data/'+d['filename'])):
            f = open('./data/'+d['filename'], 'wb')
            f.write(urlopen(SERVER_ADDRESS+"/"+ENDPOINT_ARCHIVE+"/"+d['filename']).read())
            f.close()

        ## "Wed May 21 2014 00:00:00 GMT-0500 (CDT)"
        date = strftime("%Y-%m", strptime(" ".join(d["date"].split()[:4]), "%a %b %d %Y"))
        if(not date in result):
            result[date] = {}
        if(not d["country"] in result[date]):
                result[date][d["country"]] = []
        result[date][d["country"]].append(d["filename"])

    return result

def _makeFakeJSON():
    fakeData = []
    fakeData.append({"date": 'Wed Jan 01 2010 00:00:00 GMT-0500 (CDT)', "country":"brazil", "filename":"bdjdjdj.wav"})
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
