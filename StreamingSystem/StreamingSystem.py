import pydub.playback
from pydub import *

pydub.AudioSegment.ffmpeg = "C:/ffmpeg"
pydub.AudioSegment.converter = "C:/ffmpeg"


def timeToMs(mins, secs):
    return (mins*60*1000)+(secs*1000)
def msToTime(ms):
    secs = ms // 1000 #loss of accuracy
    mins = secs // 60
    secs = secs % 60
    return mins, secs


#get audio file
id = 1
song = AudioSegment.from_wav(file="../SampleAudio/wav/"+str(id)+".wav")

#cut file into chunk
chunks = []
songMins, songSecs = msToTime(len(song))

for i in range(len(song)//5000): #for every 5 seconds
    chunk = song[i*5000:(i+1)*5000]
    chunks.append(chunk)
chunks.append(song[(len(song)//5000)*5000:]) #append last chunk

#compress chunk
bitrate = "192k"
testQueue = 0
for i in range(len(chunks)):
    location = "temp/"+str(id)+"-"+str(i)+".mp3"
    print(location)
    if i >= 8:
        testQueue = testQueue + chunks[i]
    #chunks[i].export(location, format=".mp3", bitrate=bitrate) #export compressed chunk to temporary folder
#song.export("/temp/song.mp3", format=".mp3", bitrate=bitrate)

pydub.playback.play(testQueue)

#send chunk to user

#recieve chunk

#queue and play chunk

#delete played chunk
