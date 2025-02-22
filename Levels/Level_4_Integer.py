import pygame
import random
import sys
from Timer import Timer
class Level_4_Integer():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        # self.screen.fill((0, 0, 0))
        # self.font = pygame.font.SysFont("Arial", 20)
        # self.text_rect = self.text.get_rect(center=(400, 300))
        # self.integer_input = self.font.render('Enter an integer:', True, (255, 255, 255))
        # self.integer_input_rect = self.integer_input.get_rect(center=(400, 400))
        # self.integer = None
        # self.integer_entered = False

    def random(self):
        self.integer = random.randrange(1000000000, 1000000000000)
        return self.integer
    def run(self):

        return
    # def drawText(self,text, x,y):
    #     img=self.font.render(text, True, (255, 255, 255))
    #     self.screen.blit(img, (x, y))

level=Level_4_Integer()
timer=Timer(20)
# Level.drawText("hello world", 200,400)
running = True
while running:
    level.screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # level.screen.fill((0,0,0))
    timer.update(level.screen) 
    pygame.display.update()
    # Only update the screen once per frame
    if timer.is_time_up():
        print("Time's up!")
        running = False

    pygame.time.Clock().tick(60)  # Frame rate control (60 FPS)


# Quit pygame
pygame.quit()
sys.exit()
# Start timer with 10 seconds



    