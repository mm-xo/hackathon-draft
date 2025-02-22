import pygame
import random
from Timer import Timer
# from Level_3 import level3_start

class Level_2:
    def __init__(self, screen):
        self.screen = screen
        self.running = False
        
        # Load sound
        pygame.mixer.init()
        self.level_completed = pygame.mixer.Sound("Sound/level_completed.wav")
        
        # Initialize sprites
        self.cat_asleep = self.Cat("Images/catAsleep.png", (200, 200))
        self.cat_awake = self.Cat("Images/catAwake.png", (200, 200))
        self.current_cat = self.cat_asleep
        
        # Game variables
        self.count_clicks = 0
        self.click_threshold = random.randint(3, 15)
        self.awake_time = None
        self.sound_played = False
        self.timer = Timer(10)
    
    class Cat(pygame.sprite.Sprite):
        def __init__(self, image_path, size):
            super().__init__()
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(image, size)
            self.rect = self.image.get_rect(center=(640, 360))
    
    def level2_start(self):
        print("Starting Level 2")
        self.running = True
        # sukh = False
        
        while self.running:
            self.handle_events()
            # self.update()
            # sukh = self.update()
            self.draw()
            pygame.display.update()
        
        # Return True if level completed, False if failed
        return self.awake_time is not None  

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()
    
    def handle_mouse_click(self):
        x, y = pygame.mouse.get_pos()
        if self.current_cat.rect.collidepoint(x, y):
            self.count_clicks += 1
            if self.count_clicks >= self.click_threshold:
                self.current_cat = self.cat_awake
                self.awake_time = pygame.time.get_ticks()
                
                if not self.sound_played:
                    self.level_completed.play()
                    self.sound_played = True
                    self.timer.stop_timer()
    
    def update(self):
        self.timer.update(self.screen)
        
        if self.timer.is_time_up():
            print("Time is up! Returning to menu.")
            self.running = False
            return
        
        if self.awake_time and pygame.time.get_ticks() - self.awake_time >= 3000:
            print("Level 2 completed! Starting Level 3...")
            self.running = False
            # level3_start()
            return True
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.current_cat.image, self.current_cat.rect)
        self.timer.update(self.screen)