import pygame
import random
from Timer import Timer
# from Level_3 import level3_start

class Level_2:
    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.font = pygame.font.Font("Font/GameFont.ttf", 40)
        
        # Load sound
        pygame.mixer.init()
        self.level_completed = pygame.mixer.Sound("Sound/level_completed.wav")
        
        # Load background image
        self.background = pygame.image.load("Images/classroom_BG.png").convert()
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        
        # Initialize sprites for students (2 boys, 2 girls)
        self.boy_asleep_1 = self.Student("sleeping_boy.png", (200, 200), 308, 405)
        self.boy_awake_1 = self.Student("awake_boy.png", (200, 200), 308, 405)
        
        self.girl_asleep_1 = self.Student("sleeping_girl.png", (200, 200), 528, 405)
        self.girl_awake_1 = self.Student("awake_girl.png", (200, 200), 528, 405)
        
        self.boy_asleep_2 = self.Student("sleeping_boy.png", (200, 200), 728, 405)
        self.boy_awake_2 = self.Student("awake_boy.png", (200, 200), 728, 405)
        
        self.girl_asleep_2 = self.Student("sleeping_girl.png", (200, 200), 988, 405)
        self.girl_awake_2 = self.Student("awake_girl.png", (200, 200), 988, 405)
        
        # Game variables
        self.click_thresholds = {
            "boy_1": random.randint(3, 10),
            "girl_1": random.randint(3, 10),
            "boy_2": random.randint(3, 10),
            "girl_2": random.randint(3, 10),
        }
        
        self.count_clicks = {
            "boy_1": 0,
            "girl_1": 0,
            "boy_2": 0,
            "girl_2": 0,
        }
        
        self.awake_time = None
        self.sound_played = False
        self.timer = Timer(15)
        
        # Set initial active students
        self.students = {
            "boy_1": {"asleep": self.boy_asleep_1, "awake": self.boy_awake_1, "current": self.boy_asleep_1},
            "girl_1": {"asleep": self.girl_asleep_1, "awake": self.girl_awake_1, "current": self.girl_asleep_1},
            "boy_2": {"asleep": self.boy_asleep_2, "awake": self.boy_awake_2, "current": self.boy_asleep_2},
            "girl_2": {"asleep": self.girl_asleep_2, "awake": self.girl_awake_2, "current": self.girl_asleep_2},
        }
    
    class Student(pygame.sprite.Sprite):
        def __init__(self, image_path, size, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
            self.rect = self.image.get_rect()  # Set the rect to match the image size
            self.rect.centerx = x
            self.rect.centery = y
    
    def level2_start(self):
        self.running = True
        
        while self.running:
            self.handle_events()
            self.update()
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
        
        # Check if any student's current sprite is clicked
        for student_key, student in self.students.items():
            if student["current"].rect.collidepoint(x, y):
                self.count_clicks[student_key] += 1
                if self.count_clicks[student_key] >= self.click_thresholds[student_key]:
                    # Change to awake state
                    student["current"] = student["awake"]
                    self.awake_time = pygame.time.get_ticks()
                    
                    # If all students are awake, stop the timer and play the sound
                    if self.check_all_awake() and not self.sound_played:
                        self.level_completed.play()
                        self.sound_played = True
                        self.timer.stop_timer()

    def check_all_awake(self):
        # Check if all students are awake
        return all(student["current"] == student["awake"] for student in self.students.values())
    
    def update(self):
        self.timer.update(self.screen)
        
        if self.timer.is_time_up():
            self.running = False
            return
        
        # If all students are awake and the awake_time has passed, complete the level
        if self.check_all_awake() and self.awake_time and pygame.time.get_ticks() - self.awake_time >= 3000:
            self.running = False
            # level3_start()  # Uncomment this to go to the next level
            return True
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))  # Draw the background
        
        # Draw all students (only awake students will be drawn)
        for student_key, student in self.students.items():
            self.screen.blit(student["current"].image, student["current"].rect)
        self.draw_text(self.screen, "Tap to wake them up", 1280 // 2, 110, self.font, (0,0,0))
        
        self.timer.update(self.screen)
        
    def draw_text(self, screen, text, x, y, font, color=(0,0,0)):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x- text_surface.get_width() // 2, y))