import numpy as np
import time

#creating example array
'array = np.zeros((5,10)) #empty array'
array = np.random.uniform(low=-1.0, high=1.0, size=(50, 100)) #random array


def cosine_similarity(a, b, output_degrees=False):
    dot = np.dot(a, b)
    mag_a = np.sqrt(a.dot(a)) #magnitude of a
    mag_b = np.sqrt(b.dot(b)) #magnitude of b
    reciprocal = 1.0/(mag_a*mag_b) #using the reciprocal and multiplying instead of dividing to increase efficiency
    if output_degrees:
        return np.degrees(np.arccos(dot*reciprocal))
    else:
        return dot*reciprocal


def find_recommendations(array):
    start = time.time() #measure efficiency
    recommendations = []
    for user_index in range(len(array)): #iterating through users
        similarity = []
        for partner in array:
            #comparing user with partner
            if not np.array_equal(partner, array[user_index]): #don't compare with itself
                similarity.append(cosine_similarity(array[user_index], partner, output_degrees=False))
            else:
                similarity.append(-1.0)
        most_similar_partner_index = similarity.index(max(similarity)) #find best partner

        #finding items to recommend
        for item_index in range(len(array[user_index])):
            if array[user_index][item_index] > -0.1 and array[user_index][item_index] < 0.1: #find undiscorvered items
                if array[most_similar_partner_index][item_index] > 0.8: #find if partner likes undiscovered item
                    recommendations.append([user_index, item_index])
    end = time.time()
    #print("Time to complete:", end-start, "s for", array.size, "items\n")
    return recommendations

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