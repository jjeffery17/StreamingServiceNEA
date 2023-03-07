from UserInterface import UserInterface as ui
from RecommendationSystem import RecommendationSystem as rs
from StreamingSystem import StreamingSystem as st
import threading
import pygame

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

pygame.init() #start pygame for use in audio playback and handling

def audioSmoother():
    while True:
        pygame.time.wait(10)

if __name__ == "__main__":
    p1 = threading.Thread(target=ui.UIClass, args=[recommendations])
    p2 = threading.Thread(target=st.audioPlayerObj.checkPlayLoop)
    #p3 = threading.Thread(target=audioSmoother)
    p1.start()
    p2.start()
    #p3.start()
