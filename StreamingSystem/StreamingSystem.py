import time
import threading
import pygame

class Preferences:
    def __init__(self, fileName):
        self.fileName = fileName
        self.updatePreferencesVar()

    def getPreference(self, preferenceName=""):
        self.updatePreferencesVar()
        for preference in self.preferences:
            if preference[0] == preferenceName:
                return preference[1]

    def setPreference(self, preferenceName="", preferenceSet=""):
        self.updatePreferencesVar()
        for preference in self.preferences:
            if preference[0] == preferenceName:
                preference[1] = preferenceSet
        self.updatePreferencesFile()

    def updatePreferencesFile(self):
        self.lock = threading.Lock()
        self.lock.acquire()
        with open(self.fileName, "w") as preferencesFile:
            formattedPreferences = ""
            for line in self.preferences:
                formattedPreferences += line[0]
                formattedPreferences += " = "
                formattedPreferences += line[1]
                formattedPreferences += "\n"
            preferencesFile.write(formattedPreferences)
        self.lock.release()

    def updatePreferencesVar(self):
        self.lock = threading.Lock()
        self.lock.acquire()
        with open(self.fileName, "r") as preferencesFile:
            self.preferences = []
            for line in preferencesFile:
                line = line.split("=")
                for elem in line:
                    line[line.index(elem)] = elem.strip()
                self.preferences.append(line)
        self.lock.release()

preferencesObj = Preferences("preferences.set")

def timeToMs(mins, secs):
    return (mins*60*1000)+(secs*1000)
def msToTime(ms):
    secs = ms // 1000 #loss of accuracy
    mins = secs // 60
    secs = secs % 60
    return mins, secs

def timecodeToS(timecode="0:00"):
    timecode = timecode.split(":")
    seconds = (int(timecode[0])*60)+int(timecode[1])
    return seconds

class audioPlayer():
    def __init__(self):
        self.isPlaying = False
        self.previouslyPlaying = False

    def playAudio(self, timecode="0:00"):
        pygame.mixer.music.load("SampleAudio/mp3/Ancient-music.mp3")
        pygame.mixer.music.play(start=timecodeToS(timecode))

    def stopAudio(self):
        pygame.mixer.music.stop()

    def checkPlayLoop(self):
        while True:
            time.sleep(0.5)
            previouslyPlaying = self.isPlaying
            if preferencesObj.getPreference("isPlaying") == "True":
                self.isPlaying = True
                if previouslyPlaying == False:
                    print("playing from playtime", preferencesObj.getPreference("currentPlaytime"))
                    self.playAudio(preferencesObj.getPreference("currentPlaytime"))
            else:
                self.isPlaying = False
                if previouslyPlaying == True:
                    self.stopAudio()

audioPlayerObj = audioPlayer()

'''
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
'''
