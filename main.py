from UserInterface import UserInterface as UI
from RecommendationSystem import RecommendationSystem as RS

recommendations = RS.getRecommendations(1, [10, 10, 5])
print(recommendations)
UI.runUI()