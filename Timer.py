import time
import datetime
import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
pygame.init()

screen = pygame.display.set_mode((400, 300))
running = True  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.display.set_caption("Countdown Timer")
screen.fill(WHITE)

def count_down(n,screen):
    while n > 0:
        timer = datetime.timedelta(seconds = n)
        print(timer,end="\r")
        time.sleep(1)
        n -= 1  
# count_down(60)


pygame.quit()