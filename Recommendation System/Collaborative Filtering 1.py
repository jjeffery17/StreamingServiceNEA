import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from time import sleep

#set album cover placeholders
albumCoverPlaceholder = Image.open("AlbumCoverPlaceholder.png")
albumCoverPlaceholderMassive = albumCoverPlaceholder.resize((350, 350), Image.ANTIALIAS)
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

    minutes = int(listToString(playtime[:splitterIndex]))
    seconds = int(listToString(playtime[splitterIndex+1:]))

    return (minutes*60)+seconds

def invertColour(colour):
    r = int(colour[1:3], 16) #get rgb values as integers
    g = int(colour[3:5], 16)
    b = int(colour[5:7], 16)
    r, g, b = 255-r, 255-g, 255-b #invert values
    return "#"+str(hex(r))[2:].zfill(2)+str(hex(g))[2:].zfill(2)+str(hex(b))[2:].zfill(2) #format and output

class Stack:
    def __init__(self, sizeLimit=-1):
        self.stack = []
        self.sizeLimit = sizeLimit
    def push(self, item):
        self.stack.append(item)
        if 0 < self.sizeLimit < len(self.stack):
            del self.stack[0]

    def pop(self):
        returnItem = self.stack[-1]
        del self.stack[-1]
        return returnItem
    def view(self):
        return self.stack[-1]
    def viewPrevious(self):
        return self.stack[-2]
    def delete(self):
        del self.stack[-1]

class Window:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Streaming Service NEA")
        self.root.config(bg=blackBackground)
        self.root.geometry("1280x720") #default screen size

        self.visitedWindows = Stack()
        self.visitedWindows.push("main")

        self.MainWindow = MainWindow(self.root, self)
        self.MainWindow.pack(fill=tk.BOTH, expand=True)

        #self.LogIn = LogIn(self.root, self)
        #self.LogIn.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Configure>", self.refresh)

        self.root.mainloop()

    def refresh(self, e):
        if e.widget == self.root:
            sleep(0.001) #lower refresh rate to decrease delay when moving window

    def getPreviousWindowName(self):
        return self.visitedWindows.viewPrevious()

    def changeWindow(self, currentWindow, newWindow="main", artistID=0, albumID=0, addToQueue=True):
        if newWindow == "main":
            currentWindow.pack_forget()
            del currentWindow
            self.MainWindow = MainWindow(self.root, self)
            self.MainWindow.pack(fill=tk.BOTH, expand=True)
            if addToQueue:
                self.visitedWindows.push("main")
            else:
                self.visitedWindows.delete()
        elif newWindow == "album":
            currentWindow.pack_forget()
            del currentWindow
            self.albumWindow = AlbumWindow(self.root, albumID, self)
            self.albumWindow.pack(fill=tk.BOTH, expand=True)
            if addToQueue:
                self.visitedWindows.push("album")
            else:
                self.visitedWindows.delete()
        elif newWindow == "artist":
            currentWindow.pack_forget()
            del currentWindow
            self.artistWindow = ArtistWindow(self.root, artistID, self)
            self.artistWindow.pack(fill=tk.BOTH, expand=True)
            if addToQueue:
                self.visitedWindows.push("artist")
            else:
                self.visitedWindows.delete()
        elif newWindow == "login":
            currentWindow.pack_forget()
            del currentWindow
            self.LogInWindow = LogInWindow(self.root, self)
            self.LogInWindow.pack(fill=tk.BOTH, expand=True)
            if addToQueue:
                self.visitedWindows.push("login")
            else:
                self.visitedWindows.delete()
        else:
            print("Error: no new window with name:", newWindow, "to change to")

class MainWindow(tk.Frame):
    def __init__(self, parent, window):
        tk.Frame.__init__(self, parent, bg=blackBackground)
        self.window = window
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

        self.login = Button(self.header, bg=blackPlayer, fg=textBrightHigh, activebackground=blackPlayer, activeforeground=textBrightHigh, font=fontMainBoldSmall, text="Log In", command=self.logIn)
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
            self.searchResultItems.append(SearchResultItem(self.searchResultItemsContainer, window=self.window, owningWidget=self, songID=i, artistID=i, albumID=i, albumCover=albumCoverSmall))
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
        self.currentSongStars = Stars(self.playerInfoRight)
        self.currentSongStars.grid(row=1, column=0, padx=10, pady=5)

        self.updatePlaytimeUI("1:10", "3:30")

    def updatePlaytimeUI(self, currentPlaytime, totalPlaytime):
        self.playtimer.set((playtimeToSeconds(currentPlaytime)/playtimeToSeconds(totalPlaytime))*1000)
        self.currentPlaytime["text"] = currentPlaytime
        self.totalPlaytime["text"] = totalPlaytime

    def updatePlaytimeStream(self, key): #key must be present as bind() passes through the keybind to the function
        print(float(self.playtimer.get()) / 10)

    def updateRecommendations(self):
        self.recommendationsHolder = Frame(self, bg=blackBackground)
        self.recommendationsHolder.pack(fill=tk.BOTH, padx=15, pady=15)

        albumCoverMed = ImageTk.PhotoImage(albumCoverPlaceholderMed)
        self.recommendationCards = []
        cardsPerRow = 3 #TODO: auto resize to screen size, make scrollable
        for i in range(6):
            self.card = RecommendationCard(self.recommendationsHolder, window=self.window, owningWidget=self, songID=i, artistID=i, albumID=i, albumCover=albumCoverMed)
            self.card.grid(row=i // cardsPerRow, column=i % cardsPerRow, padx=5, pady=5)

    def pausePlay(self):
        if self.play:
            self.play = False
            self.pause.config(text="⏵")
        else:
            self.play = True
            self.pause.config(text="⏸")

    def logIn(self):
        self.window.changeWindow(currentWindow=self, newWindow="login", addToQueue=True)

class ArtistWindow(tk.Frame):
    def __init__(self, parent, artistID, window):
        self.window = window
        tk.Frame.__init__(self, parent, bg=blackBackground)
        self.artistColour = "#01112b"
        self.artistHighlight = invertColour(self.artistColour)
        self.artistName = "Artist "+str(artistID)
        self.pinnedSongsID = [0, 0, 0, 0, 0]
        self.pinnedAlbumID = 0
        self.initHeader()
        self.initHighlightBar()

        style = ttk.Style()
        style.theme_use("clam")

        emptyList = []
        for i in range(26):
            emptyList.append(0)
        self.initMain(emptyList)

    def initHeader(self):
        self.header = Frame(self, bg=self.artistColour)
        self.header.pack(fill=tk.BOTH)

        self.backContainer = Frame(self.header, bg=self.artistColour)
        self.backContainer.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.backButton = Button(self.backContainer, text="← Back", bg=blackPlayer, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh, font=fontMainBoldSmall, command=self.back)
        self.backButton.pack(side=tk.TOP)

        self.artistContainer = Frame(self.header, bg=self.artistColour)
        self.artistContainer.pack(side=tk.RIGHT, padx=10, pady=10)

        self.name = Label(self.artistContainer, text=self.artistName, font=fontMainBoldTitle, bg=self.artistColour, fg=self.artistHighlight)
        self.name.grid(row=0, column=0)

        self.artistRating = Stars(self.artistContainer)
        self.artistRating.grid(row=1, column=0, pady=(10, 2), sticky=tk.E)

        self.artistRatingAvg = Label(self.artistContainer, text="Average rating: "+str(3)+" stars", font=fontMainBoldSmall, bg=self.artistColour, fg=self.artistHighlight)
        self.artistRatingAvg.grid(row=2, column=0, sticky=tk.E)

    def initHighlightBar(self):
        self.highlightBar = Frame(self, bg=blackSearch)
        self.highlightBar.pack(side=tk.RIGHT, fill=tk.Y)

        albumCoverLarge = ImageTk.PhotoImage(albumCoverPlaceholderLarge)
        #self.pinnedAlbumID
        self.albumCard = AlbumCard(self.highlightBar, "Artist Name", "Album Name", albumCoverLarge, [0, 0, 0])
        self.albumCard.pack(side=tk.TOP, padx=10, pady=10)

        albumCoverSmall = ImageTk.PhotoImage(albumCoverPlaceholderSmall)
        self.pinnedSongsList = []
        for songID in self.pinnedSongsID:
            self.pinnedSongsList.append(SearchResultItem(self.highlightBar, window=self.window, owningWidget=self, songID=songID, artistID=songID, albumID=songID, albumCover=albumCoverSmall))
        for pinnedSong in self.pinnedSongsList:
            pinnedSong.pack(padx=10)

    def initMain(self, artistAlbumID):
        container = Frame(self, bg=blackBackground)
        container.pack(fill=tk.BOTH, padx=10, pady=10)
        albumContainer = Canvas(container, bg=blackBackground, height=570)
        albumContainer.pack(fill=tk.BOTH)

        albumWidgetContainer = Frame(albumContainer, bg=blackBackground)
        albumContainer.create_window((0, 0), window=albumWidgetContainer, anchor="nw")

        albumCoverLarge = ImageTk.PhotoImage(albumCoverPlaceholderLarge)
        albumWidgetList = []
        for albumID in artistAlbumID:
            albumWidgetList.append(
                AlbumCard(albumWidgetContainer, artistID=albumID, albumID=albumID, albumCover=albumCoverLarge, topSongID=[0, 0, 0]))
        for i in range(len(albumWidgetList)):
            albumWidgetList[i].grid(row=i%2, column=i//2, padx=(0, 5), pady=1)

        albumScrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=albumContainer.xview)
        albumScrollbar.pack(side=tk.TOP, fill=tk.X)

        albumContainer.configure(xscrollcommand=albumScrollbar.set)
        albumContainer.bind("<Configure>", lambda e: albumContainer.configure(scrollregion=albumContainer.bbox("all")))

    def back(self):
        self.window.changeWindow(currentWindow=self, newWindow=self.window.getPreviousWindowName(), addToQueue=False)

class AlbumWindow(tk.Frame):
    def __init__(self, parent, albumID, window):
        self.window = window
        tk.Frame.__init__(self, parent, bg=blackBackground)
        self.albumColour = "#01112b"
        self.albumHighlight = invertColour(self.albumColour)
        self.albumName = "Album " + str(albumID)
        self.albumCoverMassive = ImageTk.PhotoImage(albumCoverPlaceholderMassive)
        self.initHeader()
        style = ttk.Style().theme_use("clam")
        emptyList = []
        for i in range(26):
            emptyList.append(0)
        self.initMain(emptyList)

    def initHeader(self):
        self.header = Frame(self, bg=self.albumColour)
        self.header.pack(fill=tk.Y, side=tk.LEFT)

        self.backContainer = Frame(self.header, bg=self.albumColour)
        self.backContainer.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.backButton = Button(self.backContainer, text="← Back", bg=blackPlayer, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh, font=fontMainBoldSmall, command=self.back)
        self.backButton.pack(side=tk.LEFT)

        self.albumContainer = Frame(self.header, bg=self.albumColour)
        self.albumContainer.pack(padx=10, pady=10, expand=True)

        self.albumCover = Label(self.albumContainer, image=self.albumCoverMassive)
        self.albumCover.grid(row=0, column=0, padx=25, pady=25)
        self.name = Label(self.albumContainer, text=self.albumName, font=fontMainBoldTitle, bg=self.albumColour, fg=self.albumHighlight)
        self.name.grid(row=1, column=0)
        self.albumRating = Stars(self.albumContainer)
        self.albumRating.grid(row=2, column=0, pady=(10, 2))
        self.albumRatingAvg = Label(self.albumContainer, text="Average rating: " + str(3) + " stars", font=fontMainBoldSmall, bg=self.albumColour, fg=self.albumHighlight)
        self.albumRatingAvg.grid(row=3, column=0)

    def initMain(self, songIDs):
        container = Frame(self, bg=blackBackground)
        container.pack(fill=tk.BOTH, padx=10, pady=10)
        container.columnconfigure(0, weight=1)
        songContainer = Canvas(container, bg=blackBackground, height=690)
        songContainer.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        songWidgetContainer = Frame(songContainer, bg=blackBackground)
        songContainer.create_window((0, 0), window=songWidgetContainer, anchor="n")

        albumCoverSmall = ImageTk.PhotoImage(albumCoverPlaceholderSmall)
        songWidgetList = []
        for songID in songIDs:
            songWidgetList.append(SearchResultItem(songWidgetContainer, window=self.window, owningWidget=self, songID=songID, albumID=songID, artistID=songID, albumCover=albumCoverSmall))
        for i in range(len(songWidgetList)):
            songWidgetList[i].pack(fill=tk.X, side=tk.TOP)

        albumScrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=songContainer.yview)
        albumScrollbar.pack(side=tk.LEFT, fill=tk.Y)

        songContainer.configure(yscrollcommand=albumScrollbar.set)
        songContainer.bind("<Configure>", lambda e: songContainer.configure(scrollregion=songContainer.bbox("all")))

    def back(self):
        self.window.changeWindow(currentWindow=self, newWindow=self.window.getPreviousWindowName(), addToQueue=False)

class LogInWindow(tk.Frame):
    def __init__(self, parent, window):
        self.window = window
        tk.Frame.__init__(self, parent, bg=blackBackground)

        self.backContainer = Frame(self, bg=blackBackground)
        self.backContainer.pack(side=tk.TOP, fill=tk.X)
        self.backButton = Button(self.backContainer, text="← Back", bg=blackPlayer, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh, font=fontMainBoldSmall, command=self.back)
        self.backButton.pack(side=tk.LEFT, padx=15, pady=15)

        self.box = Frame(self, bg=blackPlayer)
        self.box.pack(anchor=tk.CENTER, padx=25, pady=25)

        self.title = Label(self.box, text="Log In / Sign Up", bg=blackPlayer, fg=textBrightHigh, font=fontMainBoldTitle)
        self.title.pack(fill=tk.X, padx=10, pady=10)

        self.emailContainer = Frame(self.box, bg=blackPlayer)
        self.emailContainer.pack(fill=tk.X, padx=18, pady=5)
        self.emailTitle = Label(self.emailContainer, text="Email", bg=blackPlayer, fg=textBrightHigh, font=fontMainBoldSmall)
        self.emailTitle.pack(side=tk.LEFT, padx=2)
        self.emailEntry = Entry(self.emailContainer, width=75)
        self.emailEntry.pack(fill=tk.X, padx=2, pady=5)

        self.passwdContainer = Frame(self.box, bg=blackPlayer)
        self.passwdContainer.pack(fill=tk.X, padx=18, pady=5)
        self.passwdTitle = Label(self.passwdContainer, text="Password", bg=blackPlayer, fg=textBrightHigh, font=fontMainBoldSmall)
        self.passwdTitle.pack(side=tk.LEFT, padx=2)
        self.passwdEntry = Entry(self.passwdContainer, show="*", width=75)
        self.passwdEntry.pack(fill=tk.X, padx=2, pady=5)

        self.submit = Button(self.box, text="Submit", bg=blackPlayer, fg=textBrightHigh, activebackground=blackPlayer, activeforeground=textBrightHigh, font=fontMainBoldSmall, command=self.submit)
        self.submit.pack(side=tk.BOTTOM)

    def submit(self):
        print(self.emailEntry.get(), self.passwdEntry.get())

    def back(self):
        self.window.changeWindow(currentWindow=self, newWindow=self.window.getPreviousWindowName(), addToQueue=False)

class SearchResultItem(tk.Frame):
    def __init__(self, parent, window, owningWidget, songID, artistID, albumID, albumCover):
        self.window = window
        self.owningWidget = owningWidget
        tk.Frame.__init__(self, parent, bg=blackSearch, padx=5, pady=5)

        self.artistID = artistID
        self.albumID = albumID

        #albumCover = ImageTk.PhotoImage(albumCoverPlaceholder)
        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.LEFT, pady=5)

        self.infoContainerLeft = Frame(self, bg=blackSearch)
        self.infoContainerLeft.pack(side=tk.LEFT, fill=tk.X)
        self.infoContainerRight = Frame(self, bg=blackSearch)
        self.infoContainerRight.pack(side=tk.RIGHT, fill=tk.X, padx=5)

        self.songName = Label(self.infoContainerLeft, text=str(songID), font=fontMainBoldSmall, bg=blackSearch, fg=textBrightHigh)
        self.songName.grid(row=0, column=0, pady=1)
        self.artistName = Button(self.infoContainerLeft, text=str(artistID), font=fontMainBoldSmall, bg=blackSearch, fg=textBrightMed, activebackground=blackPlayer, activeforeground=textBrightHigh, command=self.openArtist)
        self.artistName.grid(row=1, column=0, pady=1)
        self.albumName = Button(self.infoContainerRight, text=str(albumID), font=fontMainBoldSmall, bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh, command=self.openAlbum)
        self.albumName.grid(row=0, column=0, sticky="e")
        self.currentSongStars = Stars(self.infoContainerRight)
        self.currentSongStars.grid(row=1, column=0)

    def openArtist(self):
        self.window.changeWindow(currentWindow=self.owningWidget, newWindow="artist", artistID=self.artistID)

    def openAlbum(self):
        self.window.changeWindow(currentWindow=self.owningWidget, newWindow="album", albumID=self.albumID)

class Stars(tk.Frame):
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
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.star1.grid(row=0, column=0)
        self.star2 = Button(self, text=self.starsArr[1], font=fontStars, command=lambda: self.updateStars(starCount=2)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.star2.grid(row=0, column=1)
        self.star3 = Button(self, text=self.starsArr[2], font=fontStars, command=lambda: self.updateStars(starCount=3)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.star3.grid(row=0, column=2)
        self.star4 = Button(self, text=self.starsArr[3], font=fontStars, command=lambda: self.updateStars(starCount=4)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.star4.grid(row=0, column=3)
        self.star5 = Button(self, text=self.starsArr[4], font=fontStars, command=lambda: self.updateStars(starCount=5)
                            , bg=blackSearch, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.star5.grid(row=0, column=4)

class RecommendationCard(tk.Frame):
    def __init__(self, parent, window, owningWidget, songID, artistID, albumID, albumCover):
        self.window = window
        self.owningWidget = owningWidget
        tk.Frame.__init__(self, parent, bg=blackBackground, highlightbackground=textBrightLow, highlightthickness=2)

        self.songID = songID
        self.albumID = albumID
        self.artistID = artistID

        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.LEFT, padx=5, pady=5)

        self.infoContainerLeft = Frame(self, bg=blackBackground)
        self.infoContainerLeft.pack(side=tk.LEFT, fill=tk.X)
        self.infoContainerRight = Frame(self, bg=blackBackground)
        self.infoContainerRight.pack(side=tk.RIGHT, fill=tk.X, padx=(100, 10))

        self.songName = Label(self.infoContainerLeft, text=str(songID), font=fontMainBold, bg=blackBackground, fg=textBrightHigh)
        self.songName.grid(row=0, column=0, pady=5)
        self.artistName = Button(self.infoContainerLeft, text=str(artistID), font=fontMainBoldSmall, bg=blackBackground, fg=textBrightMed, activebackground=blackPlayer, activeforeground=textBrightHigh, command=self.openArtist)
        self.artistName.grid(row=1, column=0, pady=5)
        self.albumName = Button(self.infoContainerRight, text=str(albumID), font=fontMainBoldSmall, bg=blackBackground, fg=textBrightLow, activebackground=blackPlayer, activeforeground=textBrightHigh, command=self.openAlbum)
        self.albumName.grid(row=0, column=0, pady=5, sticky="e")
        self.currentSongStars = Stars(self.infoContainerRight)
        self.currentSongStars.grid(row=1, column=0, pady=5)

    def openArtist(self):
        self.window.changeWindow(currentWindow=self.owningWidget, newWindow="artist", artistID=self.artistID)

    def openAlbum(self):
        self.window.changeWindow(currentWindow=self.owningWidget, newWindow="album", albumID=self.albumID)

class AlbumCard(tk.Frame):
    def __init__(self, parent, artistID, albumID, albumCover, topSongID):
        tk.Frame.__init__(self, parent, bg=blackPlayer, highlightbackground=textBrightLow, highlightthickness=2)

        self.albumCover = Label(self, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.TOP, padx=10, pady=10)

        self.albumRating = Stars(self)
        self.albumRating.pack()

        self.albumName = Button(self, text=str(albumID), font=fontMainBoldSmall, bg=blackBackground, fg=textBrightMed, activebackground=blackPlayer, activeforeground=textBrightHigh)
        self.albumName.pack(fill=tk.X, pady=(5, 0))

        self.topSongsContainer = Frame(self, bg=blackPlayer)
        self.topSongsContainer.pack(side=tk.TOP)

        self.topSongsList = []
        for songID in topSongID:
            self.topSongsList.append(Label(self.topSongsContainer, text="〔 "+"Top Song "+str(songID)+" 〕", bg=blackPlayer, fg=textBrightLow, font=fontMainBoldSmall))
        for topSongNum in range(len(self.topSongsList)):
            self.topSongsList[topSongNum].grid(row=topSongNum, column=1)

        self.spacer = Frame(self, width=0, height=0, bg=blackPlayer)
        self.spacer.pack(pady=3)


UserWindow = Window()
