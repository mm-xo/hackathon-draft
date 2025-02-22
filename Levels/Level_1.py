import pygame
import sys
from Timer import Timer
from Level_2 import level2_start

pygame.init()
pygame.mixer.init()

class Bag:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.items = []

    def draw(self, screen, font):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for i, item in enumerate(self.items):
            item_x = self.rect.x + 10 + (i % 5) * 40
            item_y = self.rect.y + 30 + (i // 5) * 40
            screen.blit(item.image, (item_x, item_y))

    def add_item(self, obj):
        if obj not in self.items:
            self.items.append(obj)

class DraggableObject:
    def __init__(self, name, x, y, image_path):
        self.name = name
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def start_drag(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.dragging = True
            self.offset_x = self.x - mouse_x
            self.offset_y = self.y - mouse_y

    def drag(self, mouse_x, mouse_y):
        if self.dragging:
            self.x = mouse_x + self.offset_x
            self.y = mouse_y + self.offset_y
            self.rect.topleft = (self.x, self.y)

    def stop_drag(self):
        self.dragging = False

    def reset_position(self):
        self.x, self.y = self.rect.centerx - self.rect.width // 2, self.rect.centery - self.rect.height // 2
        self.rect.topright = (self.x, self.y)

def draw_room(screen, background_image, objects):
    screen.blit(background_image, (0, 0))
    for obj in objects:
        obj.draw(screen)

def add_item_to_bag(obj, bag, eligible_items, success_sound, failure_sound):
    if obj in eligible_items:
        bag.add_item(obj)
        obj.image = pygame.Surface((0, 0))
        success_sound.play()
        return f"Yay!! {obj.name} added to bag", ""
    else:
        failure_sound.play()
        obj.reset_position()
        return "", f"Oops!! {obj.name} shouldn't be added"

def level1_start():
    pygame.init()
    pygame.mixer.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level 1")
    font = pygame.font.Font("Font/GameFont.ttf", 40)

    success_sound = pygame.mixer.Sound("Sound/success.wav")
    failure_sound = pygame.mixer.Sound("Sound/failure.wav")
    level_completed =pygame.mixer.Sound("Sound/level_completed.wav")
    timer = Timer(20)

    room_bg = pygame.image.load("Images/bedroom_bg.png")
    room_bg = pygame.transform.scale(room_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bag = Bag(1000, 500, 200, 200, "Images/bag.png")

    # Define objects
    obj1 = DraggableObject("Books", 250, 350, "Images/books.png")
    obj2 = DraggableObject("Laptop", 950, 500, "Images/laptop.png")
    obj3 = DraggableObject("Bottle", 550, 550, "Images/bottle.png")
    #obj4 = DraggableObject("Elon", 800, 500, "Images/elon.png")
    obj5 = DraggableObject("Socks", 500, 650, "Images/socks.png")
    obj6 = DraggableObject("PlayStation", 100, 600, "Images/ps.png")
    obj7 = DraggableObject("Charger", 850, 670, "Images/charger.png")
    objects = [obj1, obj2, obj3, obj5, obj6, obj7]

    eligible_items = [obj1, obj2, obj3, obj7]  # Only book and pencil should be added

    messageCorrect, messageWrong = "", ""
    message_timer = 0

    running = True
    awake_time = None
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    obj.start_drag(*pygame.mouse.get_pos())
            if event.type == pygame.MOUSEMOTION:
                for obj in objects:
                    obj.drag(*pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                for obj in objects[:]:
                    if obj.dragging:
                        obj.stop_drag()
                        if bag.rect.collidepoint(obj.x, obj.y):
                            messageCorrect, messageWrong = add_item_to_bag(obj, bag, eligible_items, success_sound, failure_sound)
                            message_timer = pygame.time.get_ticks()

        draw_room(screen, room_bg, objects)
        bag.draw(screen, font)
        timer.update(screen)
        

        # x,y = pygame.mouse.get_pos()
        # print(x, y)

        if pygame.time.get_ticks() - message_timer < 2000:
            message = messageCorrect if messageCorrect else messageWrong
            if message:
                text_surface = font.render(message, True, (0, 200, 0) if messageCorrect else (255, 0, 0))
                screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 140))
        
        pygame.display.update()

        if len(bag.items) == len(eligible_items):
            if awake_time is None:
                timer.stop_timer()
                level_completed.play()
                awake_time = pygame.time.get_ticks()
        if awake_time is not None and pygame.time.get_ticks() - awake_time >= 3000:
            running = False
            level2_start()
