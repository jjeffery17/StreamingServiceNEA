from UserInterface import UserInterface as ui
from RecommendationSystem import RecommendationSystem as rs

"""
output code key:

---    start new function
.      start new (time consuming) process
/      process complete
-      information
!      warning
?      query
"""

recommendations = rs.getRecommendations(1, [10, 10, 5])
print("- final recommendations:", recommendations)

ui.runUI(recommendations)