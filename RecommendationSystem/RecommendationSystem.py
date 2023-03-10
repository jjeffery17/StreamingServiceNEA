import random
import numpy
import numpy as np
from RecommendationSystem import CollaborativeFiltering as CF #import as called from main.py
import math
import sqlite3

ratingWeight = 0.5 #how much does the rating from hte user effect items in the collaborative filtering matrix

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def resetMatrix(users=0, songs=0):
    '''
    :param users: amount of users
    :param songs: amount of songs
    :return:
    '''
    if users == 0 or songs == 0: #reset to same size as before
        matrix = numpy.load("Data/CF_Matrix.npy")
        size = (len(matrix), len(matrix[0]))
        matrix = np.zeros(size)
        print(matrix)
        numpy.save("Data/CF_Matrix.npy", matrix)
    else: #reset to new size
        matrix = np.zeros((users, songs))
        print(matrix)
        numpy.save("Data/CF_Matrix.npy", matrix)

def randomMatrix(users=0, songs=0):
    '''
    :param users: amount of users
    :param songs: amount of songs
    :return:
    '''
    if users == 0 or songs == 0: #reset to same size as before
        matrix = numpy.load("Data/CF_Matrix.npy")
        size = (len(matrix), len(matrix[0]))
        matrix = np.random.uniform(-1.0, 1.0, size)
        print(matrix)
        numpy.save("Data/CF_Matrix.npy", matrix)
    else: #reset to new size
        matrix = np.zeros((users, songs))
        print(matrix)
        numpy.save("Data/CF_Matrix.npy", matrix)

def resetBehaviour():
    matrix = np.zeros((0, 5))
    print(matrix)
    np.save("Data/UserBehaviour.npy", matrix)

def updateBehaviour(userID=0, songID=0, rating=None, listened=None, artist=None, album=None):
    matrix = np.load("Data/UserBehaviour.npy")
    matrix = matrix.tolist()
    print(". updating user behaviour matrix of songID:", songID)

    location = 0
    counter = 0
    for row in matrix:
        if int(row[0]) == songID:
            location = matrix.index(row)
        else:
            counter += 1

    if counter == len(matrix) and location == 0: #if song is not in matrix
        matrix.append([songID, 0.0, 0.0, 0.0, 0.0])
        location = len(matrix)-1

    if rating != None:
        matrix[location][1] = rating
    else:
        matrix[location][1] = matrix[location][1]

    if listened != None:
        matrix[location][2] = listened
    else:
        matrix[location][2] = matrix[location][2]

    if artist != None:
        matrix[location][3] = artist
    else:
        matrix[location][3] = matrix[location][3]

    if album != None:
        matrix[location][4] = album
    else:
        matrix[location][4] = matrix[location][4]

    #update CF_Matrix
    updateItem(userID, songID, matrix[location][1], matrix[location][2], matrix[location][3], matrix[location][4])

    matrix = np.array(matrix)
    np.save("Data/UserBehaviour.npy", matrix)
    print("/ updated user behaviour matrix to:", matrix)

def getRating(songID=0):
    songID = clamp(songID, 1, 8) #TODO: clamp to size of song library
    matrix = np.load("Data/UserBehaviour.npy")
    matrix = matrix.tolist()
    #print(". getting rating of SongID:", songID)

    location = 0
    counter = 0
    for row in matrix:
        if int(row[0]) == songID:
            location = matrix.index(row)
        else:
            counter += 1

    if counter == len(matrix) and location == 0: #if song is not in matrix
        matrix.append([songID, 0.0, 0.0, 0.0, 0.0])
        location = len(matrix)-1
        #print("! no rating found\n. defaulting to average rating")
        conn = sqlite3.connect("Data/Main.db")
        return conn.execute("SELECT SongAvgRating FROM Song WHERE SongID = {};".format(songID)).fetchall()[0][0] if songID != 0 else 3
    else:
        #print("/ success!")
        return int(matrix[location][1])

def updateItem(userID, songID, rating, listened, artist, album):
    '''
    :param userID: userID for collaborative filtering location
    :param songID: songID for collaborative filtering location
    :param rating: star rating (1-5) given by user (default 3)
    :param listened: % of song listed (includes multiple listens e.g. 300% = 3 complete listens)
    :param artist: amount of songs listened to by same artist
    :param album: % of album listened to (includes multiple listens)
    :return:
    '''
    rating = (rating-3)*ratingWeight
    listened = 2*(math.tanh(listened))-1
    artist = math.log(artist+1) #natural log
    album = math.tanh(album)
    value = math.tanh(rating+listened+artist+album)
    print(". updating song:", songID, "for user:", userID, "to value:", value)
    matrix = np.load("Data/CF_Matrix.npy")
    matrix[int(userID)][songID] = value
    np.save("Data/CF_Matrix.npy", matrix)

def getRecommendations(userID, amountPerType):
    recommendations = []

    #get recommendations from collaborative filtering
    recommendationIndexes = []
    CFRecommendations = CF.getRecommendationsByUser(userID)

    for i in range(amountPerType[0]): #get random recommendation indexes
        randomIndex = random.randint(0, len(CFRecommendations)-1)
        while randomIndex in recommendationIndexes: #if index is not new, keep generating new indexes until a new one is found
            randomIndex = random.randint(0, len(CFRecommendations) - 1)
        recommendationIndexes.append(randomIndex)

    for index in recommendationIndexes: #add shuffled recommendations to final array
        recommendations.append(CFRecommendations[index][1])

    #get recommendations from AI

    #get recommendations from albums/artists

    return recommendations
