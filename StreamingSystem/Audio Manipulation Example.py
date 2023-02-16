from pydub import *
from pydub.playback import play

#mp3 = lossy compressed
#flac = lossless compressed
#wav = pure data

song = AudioSegment.from_file(file="", format="wav")

print(type(song))
print(song.frame_rate)
print(song.channels)
print(song.sample_width)
print(song.max) #highest amplitude
print(len(song))

song_louder = song + 10 #in decibels (a logarithmic scale)
song_quieter = song - 10

combined = song_quieter + song_louder

print("playing sound")
play(song)