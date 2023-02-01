import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

#set album cover placeholders
albumCoverPlaceholder = Image.open("AlbumCoverPlaceholder.png")
albumCoverPlaceholderLarge = albumCoverPlaceholder.resize((125, 125), Image.ANTIALIAS)
albumCoverPlaceholderMed = albumCoverPlaceholder.resize((75, 75), Image.ANTIALIAS)
albumCoverPlaceholderSmall = albumCoverPlaceholder.resize((50, 50), Image.ANTIALIAS)

#set appearance variables
blackSearch = "#0a0a0a"
blackPlayer = "#0f0f0f"
blackBackground = "#050505"
textBrightHigh = "#ffffff"
textBrightMed = "#e8e8e8"
textBrightLow = "#c0c0c0"

fontMainBold = ("Bierstadt", "12", "bold")
fontMainBoldTitle = ("Bierstadt", "24", "bold")
fontMainBoldSmall = ("Bierstadt", "10", "bold")
fontMainNorm = ("Bierstadt", "12")
fontStars = ("Arial", "10")
fontHidden = ("Arial", "1")

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

def invertColour(colour):
    r = int(colour[1:3], 16) #get rgb values as integers
    g = int(colour[3:5], 16)
    b = int(colour[5:7], 16)
    r, g, b = 255-r, 255-g, 255-b #invert values
    return "#"+str(hex(r))[2:].zfill(2)+str(hex(g))[2:].zfill(2)+str(hex(b))[2:].zfill(2) #format and output

class window():
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Streaming Service NEA")
        self.root.config(bg=blackBackground)
        self.root.geometry("1280x720") #default screen size

        #self.MainWindow = MainWindow(self.root)
        #self.MainWindow.pack(fill=tk.BOTH, expand=True)
        self.artistWindow = artistWindow(self.root)
        self.artistWindow.pack(fill=tk.BOTH, expand=True)
        self.root.mainloop()

class artistWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=blackBackground)
        self.artistColour = "#01112b"
        self.artistHighlight = invertColour(self.artistColour)
        self.artistName = "Artist Name"
        self.pinnedSongsID = [0, 0, 0, 0, 0]
        self.pinnedAlbumID = 0
        self.initHeader()
        self.initHighlightBar()

        emptyList = []
        for i in range(26):
            emptyList.append(0)
        self.initMain(emptyList)

    def initHeader(self):
        self.header = Frame(self, bg=self.artistColour)
        self.header.pack(fill=tk.BOTH)

        self.backContainer = Frame(self.header, bg=self.artistColour)
        self.backContainer.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.back = Button(self.backContainer, text="← Back", bg=blackPlayer, fg=textBrightLow, font=fontMainBoldSmall)
        self.back.pack(side=tk.TOP)

        self.name = Label(self.header, text=self.artistName, font=fontMainBoldTitle, bg=self.artistColour, fg=self.artistHighlight)
        self.name.pack(side=tk.RIGHT, padx=10, pady=10)

    def initHighlightBar(self):
        self.highlightBar = Frame(self, bg=blackSearch)
        self.highlightBar.pack(side=tk.RIGHT, fill=tk.Y)

        albumCoverLarge = ImageTk.PhotoImage(albumCoverPlaceholderLarge)
        #self.pinnedAlbumID
        self.albumCard = albumCard(self.highlightBar, "Artist Name", "Album Name", albumCoverLarge, [0, 0, 0])
        self.albumCard.pack(side=tk.TOP, padx=10, pady=10)

        albumCoverSmall = ImageTk.PhotoImage(albumCoverPlaceholderSmall)
        self.pinnedSongsList = []
        for songID in self.pinnedSongsID:
            self.pinnedSongsList.append(SearchResultItem(self.highlightBar, "Song Name", "Artist Name", "Album Name", albumCoverSmall))
        for pinnedSong in self.pinnedSongsList:
            pinnedSong.pack(padx=10)

    def initMain(self, artistAlbumID):
        container = Frame(self, bg=blackBackground)
        container.pack(fill=tk.BOTH, padx=10, pady=10)
        albumContainer = Canvas(container, bg=blackBackground, height=175)
        albumContainer.pack(fill=tk.BOTH)

        albumWidgetContainer = Frame(albumContainer, bg=blackBackground)
        albumContainer.create_window((0, 0), window=albumWidgetContainer, anchor="nw")

        albumCoverSmall = ImageTk.PhotoImage(albumCoverPlaceholderSmall)
        albumWidgetList = []
        for albumID in artistAlbumID:
            albumWidgetList.append(
                albumCard(albumWidgetContainer, "Artist Name", "Album Name", albumCoverSmall, [0, 0, 0]))
        for i in range(len(albumWidgetList)):
            albumWidgetList[i].grid(row=0, column=i, padx=(0, 5))

        albumScrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=albumContainer.xview)
        albumScrollbar.pack(side=tk.TOP, fill=tk.X)

        albumContainer.configure(xscrollcommand=albumScrollbar.set)
        albumContainer.bind("<Configure>", lambda e: albumContainer.configure(scrollregion=albumContainer.bbox("all")))

class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=blackBackground)
        self.initUI()

        self.play = False

    def initUI(self):
        self.initHeader()
        self.initSearch()
        self.initViewport()

    def initHeader(self):
        self.header = Frame(self, bg=blackPlayer)
        self.header.pack(fill=tk.X)

        self.logo = Label(self.header, text="LOGO")
        self.logo.pack(padx=15, pady=15, side=tk.LEFT)

        self.login = Button(self.header, font=fontMainBoldSmall, text="Log In")
        self.login.pack(padx=15, pady=15, side=tk.RIGHT)

    def initSearch(self):
        self.search = Frame(self, bg=blackSearch)
        self.search.pack(fill=tk.Y, side=tk.LEFT)

        self.searchbar = Frame(self.search, bg=blackSearch)
        self.searchbar.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.searchTitle = Label(self.searchbar, text="Search", bg=blackSearch, fg=textBrightHigh, font=fontMainBold)
        self.searchTitle.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.searchButton = Button(self.searchbar, text="🔍")
        self.searchButton.pack(side=tk.LEFT)

        self.searchEntry = Entry(self.searchbar, width=40)
        self.searchEntry.pack(fill=tk.X, padx=5, pady=5)

        self.searchResults = Frame(self.search, bg=blackSearch)
        self.searchResults.pack(fill=tk.BOTH, padx=15, pady=15)


        self.searchResultItemsContainer = Canvas(self.searchResults)
        self.searchResultItemsContainer.pack(fill=tk.BOTH)

        self.searchResultItems = []

        #creating empty search results for testing
        albumCoverSmall = ImageTk.PhotoImage(albumCoverPlaceholderSmall)
        for i in range(5):
            self.searchResultItems.append(SearchResultItem(self.searchResultItemsContainer, songName="Song", artistName="Artist", albumName="Album", albumCover=albumCoverSmall))
            self.searchResultItems[i].pack(fill=tk.X)

    def search(self, entry):
        pass

    def initViewport(self):
        self.initPlayer()
        self.updateRecommendations()

    def initPlayer(self):
        self.player = Frame(self, bg=blackPlayer)
        self.player.pack(fill=tk.X, side=BOTTOM)

        albumCover = ImageTk.PhotoImage(albumCoverPlaceholderLarge)
        self.albumCover = Label(self.player, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.RIGHT, padx=10, pady=5)

        self.playerInfo = Frame(self.player, bg=blackPlayer)
        self.playerInfo.pack(fill=tk.BOTH)

        self.playerInfoLeft = Frame(self.playerInfo, bg=blackPlayer)
        self.playerInfoLeft.pack(fill=tk.BOTH, side=tk.LEFT)
        self.playerInfoRight = Frame(self.playerInfo, bg=blackPlayer)
        self.playerInfoRight.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.controls = Frame(self.playerInfo, bg=blackPlayer)
        self.controls.pack(side=tk.BOTTOM)
        self.prev = Button(self.controls, text="⏪"
                           , font=fontStars, bg=blackSearch, fg=textBrightHigh, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.prev.grid(row=0, column=0, padx=5)
        self.pause = Button(self.controls, text="⏵", command=self.pausePlay
                            , font=fontStars, bg=blackSearch, fg=textBrightHigh, activebackground=blackPlayer, activeforeground=textBrightHigh) #play: ⏸
        self.pause.grid(row=0, column=1, padx=5)
        self.next = Button(self.controls, text="⏩"
                           , font=fontStars, bg=blackSearch, fg=textBrightHigh, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.next.grid(row=0, column=2, padx=5)

        self.playtimer = Scale(self.player, from_=0, to=1000, orient=HORIZONTAL, bg=blackPlayer, highlightbackground=blackPlayer, fg=blackPlayer, troughcolor=textBrightLow, font=fontHidden)
        self.playtimer.bind("<ButtonRelease-1>", func=self.updatePlaytimeStream)
        self.playtimer.pack(fill=tk.X, padx=8, pady=(2, 0))

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
        self.albumName.grid(row=0, column=0, padx=8, pady=10)
        self.currentSongStars = stars(self.playerInfoRight)
        self.currentSongStars.grid(row=1, column=0, padx=10, pady=5)

        self.updatePlaytimeUI("1:10", "3:30")

    def updatePlaytimeUI(self, currentPlaytime, totalPlaytime):
        self.playtimer.set((playtimeToSeconds(currentPlaytime)/playtimeToSeconds(totalPlaytime))*1000)
        self.currentPlaytime["text"] = currentPlaytime
        self.totalPlaytime["text"] = totalPlaytime

    def updatePlaytimeStream(self, key): #val must be present as bind() passes through the keybind to the function
        print(float(self.playtimer.get()) / 10)

    def updateRecommendations(self):
        self.recommendationsHolder = Frame(self, bg=blackBackground)
        self.recommendationsHolder.pack(fill=tk.BOTH, padx=15, pady=15)

        albumCoverMed = ImageTk.PhotoImage(albumCoverPlaceholderMed)
        self.recommendationCards = []
        cardsPerRow = 3 #TODO: auto resize to screen size
        for i in range(6):
            self.card1 = recommendationCard(self.recommendationsHolder, songName="Song", artistName="Artist", albumName="Album", albumCover=albumCoverMed)
            self.card1.grid(row=i // cardsPerRow, column=i % cardsPerRow, padx=5, pady=5)

    def pausePlay(self):
        if self.play:
            self.play = False
            self.pause.config(text="⏵")
        else:
            self.play = True
            self.pause.config(text="⏸")

class SearchResultItem(tk.Frame):
    def __init__(self, parent, songName, artistName, albumName, albumCover):
        tk.Frame.__init__(self, parent, bg=blackSearch, padx=5, pady=5)

        #albumCover = ImageTk.PhotoImage(albumCoverPlaceholder)
        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.LEFT, pady=5)

        self.infoContainerLeft = Frame(self, bg=blackSearch)
        self.infoContainerLeft.pack(side=tk.LEFT, fill=tk.X)
        self.infoContainerRight = Frame(self, bg=blackSearch)
        self.infoContainerRight.pack(side=tk.RIGHT, fill=tk.X, padx=5)

        self.songName = Label(self.infoContainerLeft, text=songName, font=fontMainBoldSmall, bg=blackSearch, fg=textBrightHigh)
        self.songName.grid(row=0, column=0, pady=1)
        self.artistName = Label(self.infoContainerLeft, text=artistName, font=fontMainBoldSmall, bg=blackSearch, fg=textBrightMed)
        self.artistName.grid(row=1, column=0, pady=1)
        self.albumName = Label(self.infoContainerRight, text=albumName, font=fontMainBoldSmall, bg=blackSearch, fg=textBrightLow)
        self.albumName.grid(row=0, column=0)
        self.currentSongStars = stars(self.infoContainerRight)
        self.currentSongStars.grid(row=1, column=0)

class stars(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.starsArr = ["★", "★", "★", "☆", "☆"]
        self.updateButtons()

    def updateStars(self, starCount):
        self.starsArr = ["☆", "☆", "☆", "☆", "☆"]
        for i in range(starCount):
            self.starsArr[i] = "★"
        self.updateButtons()

    def updateButtons(self):
        try:
            del self.star1, self.star2, self.star3, self.star4, self.star5 #deleting stars if they already exist
        except AttributeError:
            pass
        self.star1 = Button(self, text=self.starsArr[0], font=fontStars, command=lambda: self.updateStars(starCount=1)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh).grid(row=0, column=0)
        self.star2 = Button(self, text=self.starsArr[1], font=fontStars, command=lambda: self.updateStars(starCount=2)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh).grid(row=0, column=1)
        self.star3 = Button(self, text=self.starsArr[2], font=fontStars, command=lambda: self.updateStars(starCount=3)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh).grid(row=0, column=2)
        self.star4 = Button(self, text=self.starsArr[3], font=fontStars, command=lambda: self.updateStars(starCount=4)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh).grid(row=0, column=3)
        self.star5 = Button(self, text=self.starsArr[4], font=fontStars, command=lambda: self.updateStars(starCount=5)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh).grid(row=0, column=4)

class recommendationCard(tk.Frame):
    def __init__(self, parent, songName, artistName, albumName, albumCover):
        tk.Frame.__init__(self, parent, bg=blackBackground, highlightbackground=textBrightLow, highlightthickness=2)

        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.LEFT, padx=5, pady=5)

        self.infoContainerLeft = Frame(self, bg=blackBackground)
        self.infoContainerLeft.pack(side=tk.LEFT, fill=tk.X)
        self.infoContainerRight = Frame(self, bg=blackBackground)
        self.infoContainerRight.pack(side=tk.RIGHT, fill=tk.X, padx=(100, 10))

        self.songName = Label(self.infoContainerLeft, text=songName, font=fontMainBold, bg=blackBackground, fg=textBrightHigh)
        self.songName.grid(row=0, column=0, pady=5)
        self.artistName = Label(self.infoContainerLeft, text=artistName, font=fontMainBoldSmall, bg=blackBackground, fg=textBrightMed)
        self.artistName.grid(row=1, column=0, pady=5)
        self.albumName = Label(self.infoContainerRight, text=albumName, font=fontMainBoldSmall, bg=blackBackground, fg=textBrightLow)
        self.albumName.grid(row=0, column=0, pady=5)
        self.currentSongStars = stars(self.infoContainerRight)
        self.currentSongStars.grid(row=1, column=0, pady=5)

class albumCard(tk.Frame):
    def __init__(self, parent, artistName, albumName, albumCover, topSongID):
        tk.Frame.__init__(self, parent, bg=blackPlayer, highlightbackground=textBrightLow, highlightthickness=2)

        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.TOP, padx=10, pady=10)

        self.albumName = Label(self, text=albumName, bg=blackPlayer, fg=textBrightHigh, font=fontMainBold)
        self.albumName.pack(fill=tk.X, pady=(0, 2))

        self.topSongsContainer = Frame(self, bg=blackPlayer)
        self.topSongsContainer.pack(side=tk.TOP)

        self.topSongsList = []
        for songID in topSongID:
            self.topSongsList.append(Label(self.topSongsContainer, text="〔 "+"Top Song "+str(songID)+" 〕", bg=blackPlayer, fg=textBrightLow, font=fontMainBoldSmall))
        for topSongNum in range(len(self.topSongsList)):
            self.topSongsList[topSongNum].grid(row=topSongNum, column=1)

        self.spacer = Frame(self, width=0, height=0, bg=blackPlayer)
        self.spacer.pack(pady=3)


window()