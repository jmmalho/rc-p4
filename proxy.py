#!/usr/bin/env python3
import sys
from threading import Thread
import socket
from queue import Queue


def requestTrackSeq(manifest, trackNum, sck, host):
    numSeq = getSegmentsNum(manifest)
    startOffset = 2 + 5 * trackNum + numSeq * (trackNum-1)

    print(startOffset, len(manifest))


    split = manifest[startOffset].split(" ")
    startIndex = int(split[0])
    size = int(split[1])
    finalIndex = finalIndex = startIndex + size - 1 

    moviePath = f"{movieName}/{movieName}-{trackNum}.mp4"
    rangeHeader = f"Range: bytes={startIndex}-{finalIndex}\r\n"
    (header, data) = getParcial(sck, host, moviePath, rangeHeader)

    print(header.decode())
    return

def getTracksNum(manifest):
    return int(manifest[1])

def getSegmentsNum(manifest):
    return int(manifest[6])

def get(sck, host, path):
    ## cria o GET https... HTTP/1.0
    get = (f"GET /{path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"
        f"\r\n")
    sck.sendall(get.encode())
    return processSckAnswer(sck)

def getParcial(sck, host, path, header):
    ## cria o GET https... HTTP/1.0
    get = (f"GET /{path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"+
        header
        +f"\r\n")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(get.encode())
    return processSckAnswer(s)

def processSckAnswer(sck):
    header = "empty"
    data = b""
    while True:
        chunk = sck.recv(4096)
        if not chunk:
            break
        if header == "empty":
            header = chunk
        else:
            data += chunk

    return (header, data)
 
# producer task
def producer(queue, sck, host, port):
    sck.connect((host,port))
    manifestPath = f"{movieName}/manifest.txt"

    (_,manifest) = get(sck, host, manifestPath)
    manifest = manifest.decode().split("\n")

    ## se a track não existir
    if(getTracksNum(manifest) < trackNum):
        print("Track not available")
        return
    
    numSeg = getSegmentsNum(manifest)

    requestTrackSeq(manifest, trackNum, sck, host)

    queue.put(None)

    print('Producer: Done')
 
# consumer task
def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
    print('Consumer: Done')

url = sys.argv[1]
movieName = sys.argv[2]
trackNum = int(sys.argv[3])

splitHostPort = url.split(":")
host = splitHostPort[0]
port = int(splitHostPort[1])

sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

queue = Queue()

consumer = Thread(target=consumer, args=(queue,))
consumer.start()

producer = Thread(target=producer, args=(queue,sck, host, port))
producer.start()

producer.join()
consumer.join()



    

