import pygame
import random
from Timer import Timer
# from Level_4 import level_4_integer


pygame.init()
pygame.mixer.init()

class Level_3:
    WIDTH, HEIGHT = 1280, 720
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.font = pygame.font.Font("Font/GameFont.ttf", 40)
        self.level_completed = pygame.mixer.Sound("Sound/level_completed.wav")

        self.questions_wrong = 0
        self.questions_answered = 0
        self.user_input = ""
        self.message = ""
        self.message_color = self.BLACK
        self.message_time = 0
        self.message_duration = 500  # milliseconds

        self.timer = Timer(10)
        self.eqn, self.ans = self.get_new_question()
        self.answer_checked = False

    def display_text(self, text, color, y_pos):
        """Helper method to render text on the screen."""
        rendered_text = self.font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(self.WIDTH // 2, y_pos))
        self.screen.blit(rendered_text, text_rect)

    def get_new_question(self):
        """Randomly generates a new math question."""
        choice = random.randint(1, 4)
        a, b = random.randint(1, 10), random.randint(1, 10)
        if choice == 1:
            return f"{a} - {b} =", a - b
        elif choice == 2:
            return f"{a} + {b} =", a + b
        elif choice == 3:
            return f"{a} * {b} =", a * b
        else:
            a = random.randint(1, 5)
            return f"{a}^2 =", a**2

    def level3_start(self):
        """Starts Level 3."""
        print("Starting Level 3")
        self.running = True

        while self.running:
            self.screen.fill(self.WHITE)
            self.timer.update(self.screen)

            self.display_text(self.eqn, self.BLACK, self.HEIGHT // 3)
            self.display_text("Your Answer: " + self.user_input, self.BLACK, self.HEIGHT // 2)

            if self.message:
                self.display_text(self.message, self.message_color, self.HEIGHT // 1.5)

            self.handle_events()

            if self.questions_wrong == 3:
                print("Too many wrong answers! Returning to menu.")
                self.running = False
                return

            if self.timer.is_time_up():
                accuracy = (self.questions_answered / (self.questions_answered + self.questions_wrong)) * 100 if (self.questions_answered + self.questions_wrong) > 0 else 0
                if accuracy >= 50:
                    print("You passed Level 3! Moving to Level 4.")
                    self.level_completed.play()
                    # level_4_integer.run()
                    return True
                else:
                    print("You lost Level 3! Returning to menu.")
                self.running = False
                return

            if pygame.time.get_ticks() - self.message_time > self.message_duration and self.answer_checked:
                self.message = ""
                self.eqn, self.ans = self.get_new_question()
                self.user_input = ""
                self.answer_checked = False

            pygame.display.update()

        pygame.quit()  

    def handle_events(self):
        """Handles all user inputs."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not self.answer_checked:
                    self.check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.process_input(event)

    def check_answer(self):
        """Checks if the user's input is correct."""
        try:
            user_answer = float(self.user_input.strip())
            if user_answer == self.ans:
                self.message = "Correct!"
                self.questions_answered += 1
                self.message_color = self.GREEN
            else:
                self.message = "Wrong!"
                self.questions_wrong += 1
                self.message_color = self.RED
        except ValueError:
            self.message = "Invalid input!"
            self.message_color = self.RED

        self.message_time = pygame.time.get_ticks()
        self.answer_checked = True  

    def process_input(self, event):
        """Handles numerical input."""
        if event.unicode.isdigit() or event.unicode in "-.":
            if event.unicode == "." and "." in self.user_input:
                return
            if event.unicode == "-" and len(self.user_input) > 0:
                return
            self.user_input += event.unicode