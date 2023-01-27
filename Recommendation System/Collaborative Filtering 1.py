import numpy as np
import time


class collaborativeFiltering():
    def __init__(self, size=(100, 100)):
        #creating example array
        #array = np.zeros((5,10)) #empty array
        start = time.time()
        self.array = np.random.uniform(low=-1.0, high=1.0, size=size) #random array
        end = time.time()
        print("Time to create:", end - start, "s for", self.array.size, "items\n")


    def cosine_similarity(self, a, b, output_degrees=False): #TODO: make much more efficient
        dot = np.dot(a, b)
        mag_a = np.sqrt(a.dot(a)) #magnitude of a
        mag_b = np.sqrt(b.dot(b)) #magnitude of b
        reciprocal = 1.0/(mag_a*mag_b) #using the reciprocal and multiplying instead of dividing to increase efficiency
        if output_degrees:
            return np.degrees(np.arccos(dot*reciprocal))
        else:
            return dot*reciprocal

    def find_recommendations(self):
        TotalTimer = time
        startTotal = TotalTimer.time() #measure efficiency
        recommendations = []
        for user_index in range(len(self.array)): #iterating through users
            self.__startPartner = time.time()
            similarity = []
            for partner in self.array:
                #comparing user with partner
                if not np.array_equal(partner, self.array[user_index]): #don't compare with itself
                    similarity.append(self.cosine_similarity(self.array[user_index], partner, output_degrees=False))
                else:
                    similarity.append(-1.0)
            most_similar_partner_index = similarity.index(max(similarity)) #find best partner
            self.__endPartner = time.time()

            #finding items to recommend
            self.__startMovement = time.time()
            for item_index in range(len(self.array[user_index])):
                if self.array[user_index][item_index] > -0.1 and self.array[user_index][item_index] < 0.1: #find undiscorvered items
                    if self.array[most_similar_partner_index][item_index] > 0.8: #find if partner likes undiscovered item
                        recommendations.append([user_index, item_index])
            self.__endMovement = time.time()
        endTotal = TotalTimer.time()
        print("Time to find partner:", (self.__endPartner - self.__startPartner)*self.array.shape[0], "s for", self.array.size, "items\n")
        print("Time to move:", self.__endMovement - self.__startMovement, "s for", self.array.size, "items\n")
        print("Time to recommend:", endTotal-startTotal, "s for", self.array.size, "items\n")
        return recommendations

def testModelEfficiency():
    for x in range(4):
        for y in range(4):
            size = (10**x, 10**y)
            model = collaborativeFiltering(size=size)
            model.find_recommendations()
            print(size)

testModelEfficiency()

def testCosSimEfficiency():
    model = collaborativeFiltering(size=(1, 1))

    array = np.random.uniform(low=-1.0, high=1.0, size=(2, 100000000))
    start = time.time()
    model.cosine_similarity(array[0], array[1])
    end = time.time()
    print("Time for cosine similarity =", end-start)

#testCosSimEfficiency()




'''
#outputing recommendations
try:
    recommendations = find_recommendations(array)
    for i in recommendations:
        print("user:", i[0], "should be recommended:", i[1])
    print(recommendations)
except TypeError:
    print("No recommendations available in dataset")
'''

'''
#testing algorithm for many iterations
for iterations in range(100):
    try:
        recommendations = find_recommendations(array)
        for i in recommendations:
            user_index = i[0]
            item_index = i[1]
            original = array[user_index, item_index]
            array[user_index, item_index] = random.uniform(-0.2, 0.9)
            print(original, "is now", array[user_index, item_index])

    except TypeError:
        print("No more recommendations available")
'''

'''
#finding how many iterations to run out of recommendations
iterations = 0
while True:
    iterations += 1
    if iterations % 100 == 0:
        print(iterations)
    try:
        recommendations = find_recommendations(array)
        if iterations % 100 == 0:
            print("recommendations:", len(recommendations))
        for i in recommendations:
            user_index = i[0]
            item_index = i[1]
            original = array[user_index, item_index]
            array[user_index, item_index] = random.uniform(0.7, 0.9)
            #print(original, "is now", array[user_index, item_index])
    except TypeError:
        print("No more recommendations available")
        print(iterations)
        break
'''