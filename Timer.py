import pygame
import sys
import time
# Initialize Pygame


class Timer():

    def countdown(n):
        pygame.init()
        
        # Set up display
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Health Bar Decreasing Every Second")
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (screen_width/10, screen_height/20, screen_width*8/10, screen_height/10), border_radius=20)
        # Colors
       

        corner_radius = 20      # Radius for the curved edges

        # Timer properties
        decrease_interval = 1000  # Decrease health every 1000 milliseconds (1 second)
        last_decrease_time = 0    # Track the last time health was decreased
        
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        factor=0
        count=1
        orignal_length = n
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if(n>=0):
                # Get the current time
                current_time = pygame.time.get_ticks()
                current_length = max(screen_width*8/10-factor, 0)
                # Decrease health every second
                if current_time - last_decrease_time >= decrease_interval:  # Decrease health by 1, but don't go below 0
                    factor= count*(screen_width*8/10)/orignal_length
                    last_decrease_time = current_time  # Update the last decrease time
                    count=count+1
                    n=n-1
                
                # Clear the screen
                screen.fill(WHITE)

                # Draw the health bar background with curved edges
                pygame.draw.rect(screen, BLACK, (screen_width/10, screen_height/20, screen_width*8/10, screen_height/10), border_radius=corner_radius)


                # Draw the current health with curved edges
                if current_length > 0:
                    pygame.draw.rect(screen, RED, (screen_width/10, screen_height/20, current_length, screen_height/10), border_radius=corner_radius)

                # Update the display
                pygame.display.flip()
            
            # Control the frame rate
    pygame.quit()

Timer.countdown(10)
sys.exit()
# Quit Pygame

