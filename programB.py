import sys
import requests
import time

header_size = 5

url = sys.argv[1]

movieName = sys.argv[2]

fileName = sys.argv[3]

totalUrl = "http://" + url + "/" + movieName + "/" + "manifest.txt"

r = requests.get(totalUrl)

data = r.text.split('\n')

track_nr = int(data[1])

offset = 1

segments_nr = int(data[offset + header_size])

f = open(fileName, "w")

for i in range(track_nr):
	
	bytes = 0
	
	time_init = time.time()
	
	track_name = data[offset + 1]
	totalUrl = "http://" + url + "/" + movieName + "/" + track_name

	for j in range(segments_nr):

		segment = data[offset + header_size + j + 1]
		segment = segment.split(" ")

		final_bytes = str(int(segment[0]) + int(segment[1])-1)
		headers = {
    		"Range": f"bytes={segment[0]}-{final_bytes}",
		}
		r = requests.get(totalUrl, headers=headers)
		bytes += len(r.content)

	time_final = time.time()
	timeSpent = time_final - time_init
	bytesRate = bytes / (time_final - time_init)
	msg1 = str(timeSpent) + "\n"
	msg2 = str(bytesRate) + "\n"
	f.write(msg1)
	f.write(msg2)
	offset += segments_nr + header_size
f.close()
