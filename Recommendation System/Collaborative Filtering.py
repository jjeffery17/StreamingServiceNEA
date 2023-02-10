import numpy as np
import time

"""
output code key:

---    start new function
.      start new process (time consuming)
/      process complete
-      information
!      warning
?      query
"""

def findClosest(list, value):
    closest = [list[0]]
    for item in list:
        if abs(item-value) < abs(closest[-1]-value):
            closest.append(item)
    return closest[-1]

class collaborativeFiltering():
    def __init__(self, size=(100, 100)):
        #creating example array
        #array = np.zeros((5,10)) #empty array
        print("\n\n--- Creating Collaborative Filtering Array ---")

        print(". creating random array of size:", size)
        self.array = np.random.uniform(low=-1.0, high=1.0, size=size)
        print("/ random array created!")


    def cosineSimilarity(self, a, b, output_degrees=False):
        dot = np.dot(a, b)
        mag_a = np.sqrt(a.dot(a)) #magnitude of a
        mag_b = np.sqrt(b.dot(b)) #magnitude of b
        reciprocal = 1.0/(mag_a*mag_b) #using the reciprocal and multiplying instead of dividing to increase efficiency
        if not output_degrees:
            return dot*reciprocal
        else:
            return np.degrees(np.arccos(dot*reciprocal))

    def findRecommendations(self):
        recommendations = []
        for user_index in range(len(self.array)): #iterating through users
            self.findUserRecommendations(user_index)
        return recommendations

    def findUserRecommendations(self, userID):
        similarity = []
        recommendations = []
        for partner in self.array:
            # comparing user with partner
            if not np.array_equal(partner, self.array[userID]):  # don't compare with itself
                similarity.append(self.cosineSimilarity(self.array[userID], partner))
            else:
                similarity.append(-1.0)
        most_similar_partner_index = similarity.index(findClosest(similarity, 0))  # find best partner

        # finding items to recommend
        for item_index in range(len(self.array[userID])):
            if -0.1 < self.array[userID][item_index] < 0.1:  # find undiscovered items
                if self.array[most_similar_partner_index][item_index] > 0.8:  # find if partner likes undiscovered item
                    recommendations.append([userID, item_index])
        return recommendations


def testModelEfficiency():
    for x in range(4):
        for y in range(4):
            start = time.time()
            size = (10**x, 10**y)
            model = collaborativeFiltering(size=size)
            model.findRecommendations()
            end = time.time()
            print("- time to create:", end-start, "s for", size, "items")

#testModelEfficiency()

def testCosSimEfficiency():
    model = collaborativeFiltering(size=(1, 1))

    array = np.random.uniform(low=-1.0, high=1.0, size=(2, 100000000))
    start = time.time()
    model.cosineSimilarity(array[0], array[1])
    end = time.time()
    print("- time to complete cosine similarity calculation:", end-start, "s for", array.size, "items")

#testCosSimEfficiency()

model = collaborativeFiltering(size=(1000, 1000))
testUserID = 1
print("- partners for user", testUserID, ":", model.findUserRecommendations(testUserID))