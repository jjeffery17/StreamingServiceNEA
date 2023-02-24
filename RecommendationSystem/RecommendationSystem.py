import numpy
import numpy as np

from RecommendationSystem import CollaborativeFiltering as CF #import as called from main.py
import math

def resetMatrix(users=0, songs=0):
    '''
    :param users: amount of users
    :param songs: amount of songs
    :return:
    '''
    response = input(("Are you sure you want to reset all values in the collaborative filtering matrix? y/n"))
    if response.lower() == "y":
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
    else:
        print("/ Reset aborted!")

def resetBehaviour():
    '''
    :param users: amount of users
    :param songs: amount of songs
    :return:
    '''
    response = input(("Are you sure you want to reset all values from user interactions? y/n"))
    if response.lower() == "y":
        matrix = np.zeros((3, 5))
        print(matrix)
        numpy.save("Data/UserBehaviour.npy", matrix)
    else:
        print("/ Reset aborted!")

def updateBehaviour(songID, rating=None, listened=None, artist=None, album=None):
    matrix = np.load("Data/UserBehaviour.npy")
    print(matrix)

    location = 0
    counter = 0
    for row in matrix:
        if row[0] == songID:
            location = matrix.index(row)
        else:
            counter += 1

    if counter == len(matrix): #if song is not in matrix
        np.append(matrix, np.zeros((1, 5)))

    print(matrix)

def getRecommendations(userID, amountPerType):
    recommendations = []

    #get recommendations from Collaborative Filtering
    for recommendation in CF.getRecommendationsByUser(userID):
        if len(recommendations) >= amountPerType[0]:
            break
        recommendations.append(recommendation[1])

    #get recommendations from albums/artists

    return recommendations

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

    rating = (rating-3)*0.5
    listened = 2*(math.tanh(listened))-1
    artist = math.log(artist+1) #natural log
    album = math.tanh(album)
    value = math.tanh(rating+listened+artist+album)
    print(". updating song:", songID, "for user:", userID, "to value:", value)
    matrix = np.load("Data/CF_Matrix.npy")
    matrix[userID][songID] = value
    np.save("Data/CF_Matrix.npy", matrix)