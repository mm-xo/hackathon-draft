import pygame

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 600 # change according to height and width of the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draggable Sprite")

# Colors
WHITE = (255, 255, 255) # color in RGB format

# Load Player Sprite
player_img = pygame.image.load("player.png")  # Load an image
player_img = pygame.transform.scale(player_img, (100, 100))  # Resize if needed

# Define Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False  # Dragging state

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click
            if self.rect.collidepoint(event.pos):  # Check if clicked inside sprite
                self.dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:  # Mouse release
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:  # Mouse movement
            if self.dragging:
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y

# Create Player Object
player = Player(WIDTH // 2, HEIGHT // 2)

# Game Loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_event(event)  # Handle dragging

    screen.blit(player.image, player.rect)  # Draw sprite
    pygame.display.update()  # Refresh display

pygame.quit()