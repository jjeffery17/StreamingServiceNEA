from RecommendationSystem import CollaborativeFiltering as CF

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

#print(getRecommendations(1, [10, 10, 5]))