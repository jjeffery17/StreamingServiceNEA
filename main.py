from UserInterface import UserInterface as ui
from RecommendationSystem import RecommendationSystem as rs

recommendations = rs.getRecommendations(1, [10, 10, 5])
print("- final recommendations:", recommendations)

ui.runUI(recommendations) #TODO: fix buttons and stack