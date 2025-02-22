import pygame
import random
import sys
from Timer import Timer

pygame.init()
pygame.mixer.init()
level_completed = pygame.mixer.Sound("Sound/level_completed.wav")

class Level_4():
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Level 4 - Integer Challenge")

        # Colors
        self.BG_COLOR = (30, 30, 30)  # Dark background
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        self.LIGHT_GRAY = (180, 180, 180)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 50, 50)
        self.BLACK = (0, 0, 0)
        self.BLUE = (70, 130, 180)

        # Fonts
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 28)

        # Button
        self.button_rect = pygame.Rect(self.screen_width // 2 - 75, self.screen_height * 3/4, 150, 50)

        # Input Box
        self.input_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height / 2, 200, 50)

    def random_integer(self):
        """Generate a random large integer."""
        return random.randint(100000,99999999)

    def draw_text(self, text, x, y, color=(255, 255, 255), font=None, center=True):
        """Draws text on the screen."""
        if font is None:
            font = self.font
        img = font.render(text, True, color)
        if center:
            x = x - img.get_width() // 2
        self.screen.blit(img, (x, y))

    def draw_button(self, hover=False):
        """Draws a Next button with hover effect."""
        pygame.draw.rect(self.screen, self.LIGHT_GRAY if hover else self.GRAY, self.button_rect, border_radius=8)
        self.draw_text("Next", self.button_rect.centerx, self.button_rect.centery-10, self.BLACK, self.small_font)

    def draw_input_box(self, text):
        """Draws an input box for user entry."""
        pygame.draw.rect(self.screen, self.WHITE, self.input_rect, border_radius=5)
        self.draw_text(text, self.input_rect.centerx, self.input_rect.centery - 10, self.BLACK, self.small_font)

    def run(self):
        # Initialize Level
        level = Level_4()
        timer = Timer(5)

        # Generate a random number
        num = level.random_integer()
        running = True

        # **FIRST SCREEN (Display Random Number)**
        while running:
            level.screen.fill(level.BG_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            timer.update(level.screen)
            level.draw_text("Remember this number:", level.screen_width /2, level.screen_height/3)
            level.draw_text(str(num), level.screen_width/2, level.screen_height/2, level.BLUE, font=level.font)

            pygame.display.update()

            if timer.is_time_up():
                running = False

            pygame.time.Clock().tick(60)

        # **SECOND SCREEN (User Input)**
        running2 = True
        timer2 = Timer(10)  # Timer starts
        user_input = ""
        message = ""  # Message to display (Correct/Incorrect)
        message_color = level.WHITE  # Default text color
        answer_checked = False  # Track if the answer was checked
        timer_running = True  # Timer runs until correct answer is given

        while running2:
            level.screen.fill(level.BG_COLOR)

            # Display input prompt and box
            level.draw_text("Enter the number:", level.screen_width / 2, level.screen_height / 3)
            level.draw_input_box(user_input)

            if answer_checked:  
                level.draw_button(level.button_rect.collidepoint(pygame.mouse.get_pos()))  # Show button after checking

            # Display message if an answer is checked
            if message:
                level.draw_text(message, level.screen_width / 2, level.screen_height / 2 + 70, message_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not answer_checked:
                        try:
                            user_number = int(user_input.strip())
                            if user_number == num:
                                message = "Correct!"
                                message_color = level.GREEN
                                answer_checked = True  # Mark answer as checked
                                timer_running = False  # Stop the timer
                                return True
                            else:
                                message = "Incorrect! Try again."
                                message_color = level.RED
                            user_input = ""  # Reset input
                        except ValueError:
                            message = "Please enter a valid integer."
                            message_color = level.RED
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]  # Remove last character
                    else:
                        user_input += event.unicode  # Add typed character
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if level.button_rect.collidepoint(event.pos) and answer_checked:
                        running2 = False  # Move to the next screen

            if timer_running:  
                timer2.update(level.screen)  # Only update timer if still running

            pygame.display.update()
            pygame.time.Clock().tick(60)

        # Quit pygame
        pygame.quit()
        sys.exit()

# level_4_integer = Level_4()


    