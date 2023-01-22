import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


albumCoverPlaceholder = Image.open("AlbumCoverPlaceholder.png")
albumCoverPlaceholder = albumCoverPlaceholder.resize((100, 100), Image.ANTIALIAS)

#set colours
black05 = "#050505"
black0a = "#0a0a0a"
grey23 = "#232323"

class MainWindow():
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Streaming Service NEA")
        self.root.config(bg="black")
        self.root.geometry("852x480")

        self.initUI()

        self.root.mainloop()

    def initUI(self):
        self.initHeader()
        self.initSearch()
        self.initViewport()

    def initHeader(self):
        self.header = Frame(self.root, bg=black0a)
        self.header.pack(fill=tk.X)

        self.logo = Label(self.header, text="Logo")
        self.logo.pack(padx=5, pady=5, side=tk.LEFT)

        self.login = Button(self.header, text="Log In")
        self.login.pack(padx=5, pady=5, side=tk.RIGHT)

    def initSearch(self):
        self.search = Frame(self.root, bg=black05)
        self.search.pack(fill=tk.Y, side=tk.LEFT)

        self.searchbar = Frame(self.search, bg=black05)
        self.searchbar.pack(fill=tk.X, side=tk.TOP)

        self.searchButton = Button(self.searchbar, text="🔍")
        self.searchButton.pack(side=tk.LEFT)

        self.searchEntry = Entry(self.searchbar)
        self.searchEntry.pack(fill=tk.X, padx=5, pady=5)

        self.searchResults = Scrollbar(self.search, orient="vertical")
        self.searchResults.pack(fill=tk.BOTH)
        #self.searchResults.config(command=t.yview)

    def initViewport(self):
        self.initPlayer()

    def initPlayer(self):
        self.player = Frame(self.root, bg=black0a)
        self.player.pack(fill=tk.X, side=BOTTOM)

        albumCover = ImageTk.PhotoImage(albumCoverPlaceholder)
        self.albumCover = Label(self.player, image=albumCover)
        self.albumCover.image = albumCover
        self.albumCover.pack(side=tk.RIGHT)

        self.playerInfo = Frame(self.player, bg=black0a)
        self.playerInfo.pack(fill=tk.BOTH)

        self.playerInfoLeft = Frame(self.playerInfo)
        self.playerInfoLeft.pack(fill=tk.BOTH, side=tk.LEFT)
        self.playerInfoRight = Frame(self.playerInfo)
        self.playerInfoRight.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.playtimeContainer = Frame(self.player, padx=10, pady=10)
        self.playtimeContainer.pack(fill=tk.BOTH)
        self.playtime = ttk.Progressbar(self.playtimeContainer, orient="horizontal", mode="indeterminate", length=2500)
        self.playtime.pack(fill=tk.X, side=tk.BOTTOM)

        self.songName = Label(self.playerInfoLeft, text="SongName").grid(row=0, column=0)
        self.artistName = Label(self.playerInfoLeft, text="ArtistName").grid(row=1, column=0)
        self.albumName = Label(self.playerInfoRight, text="AlbumName").grid(row=0, column=0)

    def search(self, entry):
        pass

class SearchResultItem():
    def __init__(self):
        pass #TODO: make search result items

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