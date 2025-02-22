import pygame
import sys

# Initialize pygame
pygame.init()

# Initialize pygame mixer for sound
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Room Explorer Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)  # Darker green for outline

# Fonts
font = pygame.font.SysFont("Arial", 40)

# Bag position and dimensions
BAG_X = 1000
BAG_Y = 500
BAG_WIDTH = 200
BAG_HEIGHT = 150

# Load sound effect for successful object drop
success_sound = pygame.mixer.Sound("success.mp3")  # Make sure to provide the correct path to the sound file
failure_sound = pygame.mixer.Sound("failure.mp3")  # Failure sound for non-eligible items

# Define Object class
class Object:
    def __init__(self, name, x, y, image):
        self.name = name
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_position = (x, y)  # Store the original position
        self.dragging = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def start_drag(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.dragging = True
            self.offset_x = mouse_x - self.x
            self.offset_y = mouse_y - self.y

    def drag(self, mouse_x, mouse_y):
        if self.dragging:
            self.x = mouse_x - self.offset_x
            self.y = mouse_y - self.offset_y
            self.rect.topleft = (self.x, self.y)

    def stop_drag(self):
        self.dragging = False

    def reset_position(self):
        """Reset the object's position to its original position"""
        self.x, self.y = self.original_position
        self.rect.topleft = self.original_position

# Define Bag class
class Bag:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = []

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, 2)
        text = font.render("Bag", True, BLACK)
        screen.blit(text, (self.rect.x + 10, self.rect.y + 5))

        # Display items inside the bag
        for i, item in enumerate(self.items):
            item_x = self.rect.x + 10 + (i % 5) * 40  # Adjust item positions inside the bag
            item_y = self.rect.y + 30 + (i // 5) * 40
            screen.blit(item.image, (item_x, item_y))

    def add_item(self, obj):
        """Store an object in the bag and remove it from the room."""
        if obj not in self.items:
            self.items.append(obj)

# Define Room class
class Room:
    def __init__(self, background_image):
        self.background_image = pygame.image.load(background_image)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def draw(self):
        screen.blit(self.background_image, (0, 0))
        for obj in self.objects:
            obj.draw()

# Load images for objects
laptop_image = pygame.Surface((75, 50)) # image of an object
laptop_image.fill(WHITE)
lamp_image = pygame.Surface((50, 50))  # Placeholder lamp
lamp_image.fill(RED)
iPad_image = pygame.Surface((25, 40)) # image of an object
iPad_image.fill(BLUE)
charger_image = pygame.Surface((15, 15))  # Placeholder lamp
charger_image.fill(BLACK)
ps_image = pygame.Surface((30, 60))  # Placeholder lamp
ps_image.fill(GRAY)

# Create room and objects
room = Room("Bedroom.png")  # background image of the room
laptop = Object("Laptop", 300, 300, laptop_image)
lamp = Object("Lamp", 500, 400, lamp_image)
iPad = Object("iPad", 125, 250, iPad_image)
charger = Object("Charger", 250, 500, charger_image)
ps = Object("ps", 600, 400, ps_image)
bag = Bag(BAG_X, BAG_Y, BAG_WIDTH, BAG_HEIGHT)

# Add objects to room
room.add_object(laptop)
room.add_object(lamp)
room.add_object(ps)
room.add_object(iPad)
room.add_object(charger)

# Create lists for eligible and non-eligible items
eligible_items = [laptop, lamp, iPad, charger]  # List of eligible items
non_eligible_items = [ps]  # List of non-eligible items

# Text message variables
messageCorrect = ""
message_timer = 0  # Timer for how long to show the message
messageWrong = ""
message_timer = 0  # Timer for how long to show the message

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start dragging an object
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for obj in room.objects:
                obj.start_drag(mouse_x, mouse_y)

        # Dragging an object
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for obj in room.objects:
                obj.drag(mouse_x, mouse_y)

        # Drop object into bag
        if event.type == pygame.MOUSEBUTTONUP:
            for obj in room.objects[:]:  # Iterate over a copy to avoid issues while removing items
                if obj.dragging:
                    obj.stop_drag()

                    # Check if dropped inside the bag
                    if bag.rect.collidepoint(obj.x, obj.y):
                        # Check if item is eligible
                        if obj in eligible_items:
                            bag.add_item(obj)
                            obj.image = pygame.Surface((0, 0))  # Make object disappear from the screen
                            room.objects.remove(obj)  # Remove from room
                            # Play the success sound
                            success_sound.play()
                            messageCorrect = f"Yay!! {obj.name} added to bag"
                            message_timer = pygame.time.get_ticks()  # Start the timer
                        else:
                            # Play the failure sound for non-eligible items
                            failure_sound.play()
                            messageWrong = f"Oops!! {obj.name} shouldn't be added to bag"
                            message_timer = pygame.time.get_ticks()  # Start the timer
                            obj.reset_position()
    # Draw everything
    room.draw()
    bag.draw()

# Display the message if it's not empty and the timer is within time limit
    if messageCorrect:
        elapsed_time = pygame.time.get_ticks() - message_timer
        if elapsed_time < 2000:  # Show the message for 2 seconds
            # Render outline first
            outline_text = font.render(messageCorrect, True, BLACK)
            screen.blit(outline_text, (SCREEN_WIDTH // 2 - outline_text.get_width() // 2, 100))
            message_text = font.render(messageCorrect, True, GREEN)
            screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 100))

    if messageWrong:
        elapsed_time = pygame.time.get_ticks() - message_timer
        if elapsed_time < 2000:  # Show the message for 2 seconds
            # Render outline first
            outline_text = font.render(messageWrong, True, BLACK)
            screen.blit(outline_text, (SCREEN_WIDTH // 2 - outline_text.get_width() // 2, 100))
            message_text = font.render(messageWrong, True, RED)
            screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 100))

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
sys.exit()
