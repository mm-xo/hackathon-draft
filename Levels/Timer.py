import pygame # type: ignore
import sys

class Timer:
    def __init__(self, duration):
        self.duration = duration  # Timer duration (in seconds)
        self.time_left = duration  # Time left on the timer
        self.last_decrease_time = 0  # Last time the timer decreased
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # pygame.display.set_caption("Countdown Timer")
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.corner_radius = 20
        self.decrease_interval = 1000  # Decrease every 1000 milliseconds (1 second)
        
    def update(self, screen):
        """Update the timer and redraw it on the provided screen."""
        # Update the time left based on elapsed time
        current_time = pygame.time.get_ticks()
        if current_time - self.last_decrease_time >= self.decrease_interval and self.time_left > 0:
            self.time_left -= 1
            self.last_decrease_time = current_time  # Update last decrease time
        screen.fill(self.white)
        # Draw the timer background with curved edges
        pygame.draw.rect(screen, self.black, (self.screen_width / 10, self.screen_height / 20, self.screen_width * 8 / 10, self.screen_height / 10), border_radius=self.corner_radius)

        # Draw the current time (health) with curved edges
        current_length = (self.screen_width * 8 / 10) * (self.time_left / self.duration)
        if current_length > 0:
            pygame.draw.rect(screen, self.red, (self.screen_width / 10, self.screen_height / 20, current_length, self.screen_height / 10), border_radius=self.corner_radius)
        pygame.display.flip()
    # def update(self):
    #     """Update the timer and redraw the screen every frame."""
    #     # Handle events
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()

    #     # Update the time left based on elapsed time
    #     current_time = pygame.time.get_ticks()
    #     if current_time - self.last_decrease_time >= self.decrease_interval and self.time_left > 0:
    #         self.time_left -= 1
    #         self.last_decrease_time = current_time  # Update the last decrease time
        
    #     # Clear the screen
    #     self.screen.fill(self.white)

    #     # Draw the timer background with curved edges
    #     pygame.draw.rect(self.screen, self.black, (self.screen_width / 10, self.screen_height / 20, self.screen_width * 8 / 10, self.screen_height / 10), border_radius=self.corner_radius)

    #     # Draw the current time (health) with curved edges
    #     current_length = (self.screen_width * 8 / 10) * (self.time_left / self.duration)
    #     if current_length > 0:
    #         pygame.draw.rect(self.screen, self.red, (self.screen_width / 10, self.screen_height / 20, current_length, self.screen_height / 10), border_radius=self.corner_radius)

    #     # Update the display
    #     pygame.display.flip()

    def is_time_up(self):
        """Returns True if the time is up."""
        return self.time_left <= 0


# Main function to run the timer
def run_timer(duration,screen):
    pygame.init()
    timer = Timer(duration)
    running=True
    while running:
        timer.update(screen)
        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running=False
        if timer.is_time_up():
            print("Time's up!")
            break

        pygame.time.Clock().tick(60)  # Frame rate control (60 FPS)
    
    pygame.quit()
    sys.exit()

# if __name__ == "__main__":
#     run_timer(30)  # Start timer with 10 seconds
