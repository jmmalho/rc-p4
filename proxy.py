#!/usr/bin/env python3

import sys

from threading import Thread

import socket

from queue import Queue

import requests

def requestTrackSeq(manifest, trackNum, url, idx):

    numSeq = getSegmentsNum(manifest) 

    startOffset = 2 + 5 * trackNum + numSeq * (trackNum-1)

    track = manifest[startOffset - 5]

    split = manifest[startOffset+idx].split(" ")

    startIndex = int(split[0])

    size = int(split[1])

    finalIndex = startIndex + size - 1

    totalUrl = "http://" + url + "/" + movieName + "/" + track
    headers = {
    	"Range": f"bytes={startIndex}-{finalIndex}",
	}
    r = requests.get(totalUrl, headers=headers)
    return r

def getTracksNum(manifest):
    return int(manifest[1])

def getSegmentsNum(manifest):
    return int(manifest[6])

# producer task
def producer(queue, sck, url):

    totalUrl = "http://" + url + "/" + movieName + "/" + "manifest.txt"
    r = requests.get(totalUrl)
    manifest = r.text.split("\n")

    ## se a track não existir
    if(getTracksNum(manifest) < trackNum):
        print("Track not available")
        return
    
    numSeg = getSegmentsNum(manifest)
    for i in range(numSeg):
        r = requestTrackSeq(manifest, trackNum, url, i)
        queue.put(r.content)

    queue.put(None)

    print('Producer: Done')

# consumer task
def consumer(queue, sck):
    while True:
        item = queue.get()
        if item is None:
            break
        sck.sendall(item)
    print('Consumer: Done')

url = sys.argv[1]

movieName = sys.argv[2]

trackNum = int(sys.argv[3])

splitHostPort = url.split(":")

sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sck.connect(("",8000))

queue = Queue()

consumer = Thread(target=consumer, args=(queue, sck))

consumer.start()

producer = Thread(target=producer, args=(queue,sck, url))
producer.start()

producer.join()
consumer.join()