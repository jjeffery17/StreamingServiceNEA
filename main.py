from UserInterface import UserInterface as ui
from RecommendationSystem import RecommendationSystem as rs

recommendations = rs.getRecommendations(1, [10, 10, 5])
print("- final recommendations:", recommendations)

#testing updating item
rs.updateItem(0, 0, 5, 6.88, 34, 3.5) #likes song
rs.updateItem(0, 0, 1, 0.1, 0, 0.05) #dislkies song
rs.updateItem(0, 0, 3, 1, 0, 0.05) #no interaction

ui.runUI(recommendations)