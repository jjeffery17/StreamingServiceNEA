import wave

#mp3 = lossy compressed
#flac = lossless compressed
#wav = pure data

obj = wave.open("Ancient-music.wav", "rb")

print("No of channels:", obj.getnchannels())
print("Sample width:", obj.getsampwidth())
print("Sample rate:", obj.getframerate())
print("Number of samples:", obj.getnframes())


obj.close()