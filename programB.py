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

for i in range(track_nr):

	time_init = time.time()

	file_track = fileName + str(i);

	f = open(file_track, "wb")

	for j in range(segments_nr):
		track_name = data[offset + 1]
		totalUrl = "http://" + url + "/" + movieName + "/" + track_name

		segment = data[offset + header_size + j + 1]
		segment = segment.split(" ")

		final_bytes = str(int(segment[0]) + int(segment[1])-1)
		headers = {"Range":"bytes="+segment[0]+"-"+final_bytes}
		r = requests.get(totalUrl, headers=headers)
		print(len(r.content))
		f.write(r.content)

	time_final = time.time()
	print(time_final - time_init)
	offset += segments_nr + header_size
	f.close()