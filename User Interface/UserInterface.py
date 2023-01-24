import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


albumCoverPlaceholder = Image.open("AlbumCoverPlaceholder.png")
albumCoverPlaceholder = albumCoverPlaceholder.resize((100, 100), Image.ANTIALIAS)
albumCoverPlaceholderSmall = albumCoverPlaceholder.resize((25, 25), Image.ANTIALIAS)

#set appearance variables
blackSearch = "#0a0a0a"
blackPlayer = "#0f0f0f"
blackBackground = "#050505"
textBrightHigh = "#ffffff"
textBrightMed = "#e8e8e8"
textBrightLow = "#c0c0c0"

fontMainBold = ("Bierstadt", "12", "bold")
fontMainBoldSmall = ("Bierstadt", "10", "bold")
fontMainNorm = ("Bierstadt", "12")

#set playtime variables
currentPlaytime = "0:00"
totalPlaytime = "0:00"

def listToString(list):
    string = ""
    for letter in list:
        string += letter
    return string

def playtimeToSeconds(playtime):
    playtime = list(playtime)
    splitterIndex = 0

    for i in range(len(playtime)):
        if playtime[i] == ":":
            splitterIndex = i

    mins = int(listToString(playtime[:splitterIndex]))
    secs = int(listToString(playtime[splitterIndex+1:]))

    return (mins*60)+secs



class MainWindow():
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Streaming Service NEA")
        self.root.config(bg=blackBackground)
        self.root.geometry("1280x720") #default screen size

        self.initUI()

        self.root.mainloop()

    def initUI(self):
        self.initHeader()
        self.initSearch()
        self.initViewport()

    def initHeader(self):
        self.header = Frame(self.root, bg=blackPlayer)
        self.header.pack(fill=tk.X)

        self.logo = Label(self.header, text="LOGO")
        self.logo.pack(padx=15, pady=15, side=tk.LEFT)

        self.login = Button(self.header, font=fontMainBoldSmall, text="Log In")
        self.login.pack(padx=15, pady=15, side=tk.RIGHT)

    def initSearch(self):
        self.search = Frame(self.root, bg=blackSearch)
        self.search.pack(fill=tk.Y, side=tk.LEFT)

        self.searchbar = Frame(self.search, bg=blackSearch)
        self.searchbar.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.searchButton = Button(self.searchbar, text="🔍")
        self.searchButton.pack(side=tk.LEFT)

        self.searchEntry = Entry(self.searchbar, width=30)
        self.searchEntry.pack(fill=tk.X, padx=5, pady=5)

        self.searchResults = Scrollbar(self.search, orient="vertical")
        self.searchResults.pack(fill=tk.BOTH, padx=10, pady=10)
        #self.searchResults.config(command=t.yview)

    def initViewport(self):
        self.initPlayer()

    def initPlayer(self):
        self.player = Frame(self.root, bg=blackPlayer)
        self.player.pack(fill=tk.X, side=BOTTOM)

        albumCover = ImageTk.PhotoImage(albumCoverPlaceholder)
        albumCoverSmall = ImageTk.PhotoImage(albumCoverPlaceholderSmall)
        self.albumCover = Label(self.player, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.RIGHT, padx=10, pady=5)

        self.playerInfo = Frame(self.player, bg=blackPlayer)
        self.playerInfo.pack(fill=tk.BOTH)

        self.playerInfoLeft = Frame(self.playerInfo, bg=blackPlayer)
        self.playerInfoLeft.pack(fill=tk.BOTH, side=tk.LEFT)
        self.playerInfoRight = Frame(self.playerInfo, bg=blackPlayer)
        self.playerInfoRight.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.playtimer = ttk.Progressbar(self.player, orient="horizontal", mode="determinate")
        self.playtimer.pack(fill=tk.X, padx=8, pady=(10, 0))

        self.playtimeInfoContainer = Frame(self.player, bg=blackPlayer)
        self.playtimeInfoContainer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.currentPlaytime = Label(self.playtimeInfoContainer, text="0:00", font=fontMainNorm, bg=blackPlayer, fg=textBrightMed)
        self.currentPlaytime.pack(side=tk.LEFT, padx=5, pady=(0, 10))
        self.totalPlaytime = Label(self.playtimeInfoContainer, text="0:00", font=fontMainNorm, bg=blackPlayer, fg=textBrightMed)
        self.totalPlaytime.pack(side=tk.RIGHT, padx=5, pady=(0, 10))

        self.songName = Label(self.playerInfoLeft, text="SongName", font=fontMainBold, bg=blackPlayer, fg=textBrightHigh)
        self.songName.grid(row=0, column=0, padx=8, pady=10)
        self.artistName = Label(self.playerInfoLeft, text="ArtistName", font=fontMainBold, bg=blackPlayer, fg=textBrightMed)
        self.artistName.grid(row=1, column=0, padx=10, pady=5)
        self.albumName = Label(self.playerInfoRight, text="AlbumName", font=fontMainBold, bg=blackPlayer, fg=textBrightLow)
        self.albumName.grid(row=0, column=0, padx=8, pady=15)

        self.updatePlaytime("1:10", "3:30")

        self.searchResultItem = SearchResultItem(self.searchResults, songName="Song", artistName="Artist", albumName="Album", albumCover=albumCoverSmall)
        self.searchResultItem.pack()

    def search(self, entry):
        pass

    def updatePlaytime(self, currentPlaytime, totalPlaytime):
        self.playtimer["value"] = (playtimeToSeconds(currentPlaytime)/playtimeToSeconds(totalPlaytime))*100
        self.currentPlaytime["text"] = currentPlaytime
        self.totalPlaytime["text"] = totalPlaytime

class SearchResultItem(tk.Frame):
    def __init__(self, parent, songName, artistName, albumName, albumCover):
        tk.Frame.__init__(self, parent)

        #albumCover = ImageTk.PhotoImage(albumCoverPlaceholder)
        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.LEFT, padx=10, pady=5)

        self.infoContainer = Frame(self, bg=blackPlayer)
        self.infoContainer.pack(side=tk.LEFT, fill=tk.X)

        self.songName = Label(self.infoContainer, text=songName, font=fontMainBoldSmall, bg=blackPlayer, fg=textBrightHigh)
        self.songName.grid(row=0, column=0, padx=8, pady=15)
        self.artistName = Label(self.infoContainer, text=artistName, font=fontMainBoldSmall, bg=blackPlayer, fg=textBrightMed)
        self.artistName.grid(row=1, column=0, padx=8, pady=15)
        self.albumName = Label(self, text=albumName, font=fontMainBoldSmall, bg=blackPlayer, fg=textBrightLow)
        self.albumName.pack(side=tk.RIGHT, padx=8, pady=15)

class stars():
    def __init__(self):
        pass #TODO: make stars
        '''
        self.root = tk.Tk()
        self.star1 = Button(self.root, text="1").grid(row=0, column=0)
        self.star2 = Button(self.root, text="2").grid(row=0, column=1)
        self.star3 = Button(self.root, text="3").grid(row=0, column=2)
        self.star4 = Button(self.root, text="4").grid(row=0, column=3)
        self.star5 = Button(self.root, text="5").grid(row=0, column=4)
        '''

MainWindow()
#SearchResultItem()