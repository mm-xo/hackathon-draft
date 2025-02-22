import pygame
import sys

class Level_1_Dragger:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Room Explorer Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (169, 169, 169)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.DARK_GREEN = (0, 200, 0)

        # Fonts
        self.font = pygame.font.SysFont("Arial", 40, bold=True)

        # Load sounds
        self.success_sound = pygame.mixer.Sound("success.mp3")
        self.failure_sound = pygame.mixer.Sound("failure.mp3")

        # Bag position and dimensions
        self.BAG_X = 1000
        self.BAG_Y = 500
        self.BAG_WIDTH = 200
        self.BAG_HEIGHT = 150

        # Create room and objects
        self.room = self.Room("Bedroom.png")  # Background image of the room
        self.bag = self.Bag(self.BAG_X, self.BAG_Y, self.BAG_WIDTH, self.BAG_HEIGHT)

        # Load object images
        laptop_image = pygame.Surface((75, 50))
        laptop_image.fill(self.WHITE)
        lamp_image = pygame.Surface((50, 50))
        lamp_image.fill(self.RED)
        iPad_image = pygame.Surface((25, 40))
        iPad_image.fill(self.BLUE)
        charger_image = pygame.Surface((15, 15))
        charger_image.fill(self.BLACK)
        ps_image = pygame.Surface((30, 60))
        ps_image.fill(self.GRAY)

        # Create objects
        self.laptop = self.Object("Laptop", 300, 300, laptop_image)
        self.lamp = self.Object("Lamp", 500, 400, lamp_image)
        self.iPad = self.Object("iPad", 125, 250, iPad_image)
        self.charger = self.Object("Charger", 250, 500, charger_image)
        self.ps = self.Object("PlayStation", 600, 400, ps_image)

        # Add objects to room
        self.room.add_object(self.laptop)
        self.room.add_object(self.lamp)
        self.room.add_object(self.ps)
        self.room.add_object(self.iPad)
        self.room.add_object(self.charger)

        # Define eligible and non-eligible items
        self.eligible_items = [self.laptop, self.lamp, self.iPad, self.charger]
        self.non_eligible_items = [self.ps]

        # Text message variables
        self.messageCorrect = ""
        self.messageWrong = ""
        self.message_timer = 0  # Timer for message display duration

        # Timer and game loop control
        self.timer = Timer(20)
        self.running = True

    class Object:
        def __init__(self, name, x, y, image):
            self.name = name
            self.x = x
            self.y = y
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.original_position = (x, y)
            self.dragging = False

        def draw(self, screen):
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
            self.x, self.y = self.original_position
            self.rect.topleft = self.original_position

    class Bag:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)
            self.items = []

        def draw(self, screen, font):
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)
            text = font.render("Bag", True, (0, 0, 0))
            screen.blit(text, (self.rect.x + 10, self.rect.y + 5))
            for i, item in enumerate(self.items):
                item_x = self.rect.x + 10 + (i % 5) * 40
                item_y = self.rect.y + 30 + (i // 5) * 40
                screen.blit(item.image, (item_x, item_y))

        def add_item(self, obj):
            if obj not in self.items:
                self.items.append(obj)

    class Room:
        def __init__(self, background_image):
            self.background_image = pygame.image.load(background_image)
            self.background_image = pygame.transform.scale(self.background_image, (1280, 720))
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
                        bag.add_item(obj)
                        obj.image = pygame.Surface((0, 0))
                        room.objects.remove(obj)  # Remove from room
                        # Play the success sound
                        success_sound.play()

    # Draw everything
    room.draw()
    bag.draw()

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
sys.exit()
