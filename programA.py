import sys
import requests

INFO_OFFSET = 4
nextIndex = 2


def getTracksNum(manifest):
    return int(manifest[1])

def getSegmentsNum(manifest):
    return int(manifest[6])

def getTotalSize(manifest):
    sizeBlock = manifest[INFO_OFFSET + getSegmentsNum(splittedManifest)]
    sizeBlock = sizeBlock.split(" ")

    start = int(sizeBlock[0])
    numBytesuntilEnd = int(sizeBlock[1])
    return start + numBytesuntilEnd

serverURL = sys.argv[1]
movieName = sys.argv[2]
resultFileName = sys.argv[3]
fullURL = "http://" + serverURL + "/" + movieName + "/" + "manifest.txt"

resultFile = open(resultFileName,'w')

resposta = requests.get(fullURL)
splittedManifest = resposta.text.split("\n")

numTracks = getTracksNum(splittedManifest)
numSegments = getSegmentsNum(splittedManifest)

print(numTracks, file= resultFile)
print(numSegments, file= resultFile)

start_index = 2

## gets tracks info
for i in range(numTracks):
    manifest = splittedManifest[start_index::]
    size = getTotalSize(manifest)
    print(size, file= resultFile)
    start_index += INFO_OFFSET + numSegments


resultFile.close()
