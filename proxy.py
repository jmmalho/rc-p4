#!/usr/bin/env python3
import sys
from threading import Thread
import socket
from queue import Queue

def getTracksNum(manifest):
    return int(manifest[3])

def getSegmentsNum(manifest):
    return int(manifest[6])

def get(sck, host, path):
    ## cria o GET https... HTTP/1.0
    get = (f"GET /{path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"
        f"\r\n")
    sck.sendall(get.encode())
    ## recebe o reply
    header = "empty"
    data = b""
    while True:
        chunk = sck.recv(4096)
        if not chunk:
            break
        if header == "empty":
            header = chunk
            print(header)
        else:
            data += chunk
    return (header, data)
 
# producer task
def producer(queue):
    url = sys.argv[1]
    movieName = sys.argv[2]
    trackNum = sys.argv[3]

    splitHostPort = url.split(":")
    host = splitHostPort[0]
    port = int(splitHostPort[1])
    sck.connect((host,port))

    manifestPath = f"{movieName}/manifest.txt"
    moviePath = f"{movieName}/{movieName}-{trackNum}.mp4"

    (_,manifest) = get(sck, host, manifestPath)

    ## se a track não existir
    if(getTracksNum(manifest) < trackNum){
        print("Track not available")
        exit()
    }

    segmentIndex = 1;
    print(getSegmentsNum(manifest))

    print('Producer: Done')
 
# consumer task
def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
    print('Consumer: Done')

sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

queue = Queue()

consumer = Thread(target=consumer, args=(queue,))
consumer.start()

producer = Thread(target=producer, args=(queue,))
producer.start()

producer.join()
consumer.join()



    

