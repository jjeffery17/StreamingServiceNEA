from RecommendationSystem import CollaborativeFiltering as CF #import as called from main.py
import math
def getRecommendations(userID, amountPerType):
    recommendations = []

    #get recommendations from Collaborative Filtering
    for recommendation in CF.getRecommendationsByUser(userID):
        if len(recommendations) >= amountPerType[0]:
            break
        recommendations.append(recommendation[1])

    #get recommendations from AI

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