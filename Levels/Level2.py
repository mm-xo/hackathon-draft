import pygame
import random
from Timer import Timer
#
#from Levels.Level_3 import level3_start

# Initialize Pygame
pygame.init()

success_sound = pygame.mixer.Sound("success.mp3")

# Set up display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 2")

# Define sprite classes
class catAsleep(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("catAsleep.png").convert_alpha()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect(center=(640, 360))

class catAwake(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("catAwake.png").convert_alpha()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect(center=(640, 360))

# Initialize instances of the sprites
catAsleepInstance = catAsleep((200, 200))
catAwakeInstance = catAwake((200, 200))

# Initialize global variables
currentCat = catAsleepInstance


# Define the game loop
def level2_start():
    global currentCat, countClicks  # Declare as global to modify the global variables

    countClicks = 0
    clickThreshold = random.randint(3, 15)

    awake_time = None
    running = True
    soundPlayed = False
    timer = Timer(10)

    while running:
        # Update the timer first
        timer.update(screen)

        # Now clear the screen
        screen.fill((0, 0, 0))

        # Draw everything else
        screen.blit(currentCat.image, currentCat.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if currentCat.rect.collidepoint(x, y):
                    countClicks += 1
                    if countClicks >= clickThreshold:
                        currentCat = catAwakeInstance
                        awake_time = pygame.time.get_ticks()

                        if not soundPlayed:
                            success_sound.play()
                            soundPlayed = True

        # Redraw the timer after everything
        timer.update(screen)

        pygame.display.update()

        if (timer.is_time_up()):
            print("time up game over")
            pygame.quit()
            return
        if awake_time is not None and pygame.time.get_ticks() - awake_time >= 3000:
            running = False
            # level3_start()
level2_start()
