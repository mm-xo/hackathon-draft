import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 2")

# Define sprite classes
class catAsleep(pygame.sprite.Sprite):
    def __init__(self, location, size):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("catAsleep.png").convert_alpha()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class catAwake(pygame.sprite.Sprite):
    def __init__(self, location, size):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("catAwake.png").convert_alpha()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# Initialize instances of the sprites
catAsleepInstance = catAsleep([370, 430], (200, 100))
catAwakeInstance = catAwake([370, 430], (200, 100))

# Initialize global variables
currentCat = catAsleepInstance
countClicks = 0

# Define the game loop
def levelStart():
    global currentCat, countClicks  # Declare as global to modify the global variables

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(currentCat.image, currentCat.rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                countClicks += 1
                if countClicks >= random.randint(5, 20):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if currentCat.rect.collidepoint(mouse_x, mouse_y):
                        # Change to awake cat
                        currentCat = catAwakeInstance

    pygame.quit()
