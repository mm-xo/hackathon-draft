import pygame
import random
import math
from Timer import Timer
from Level_4 import level_4_integer
from lost import you_lost_screen
#from menu import menu

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Level 3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

font = pygame.font.Font("Font/GameFont.ttf", 40)
level_completed = pygame.mixer.Sound("Sound/level_completed.wav")

def display_text(text, color, y_pos):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_pos))  # Center the text horizontally
    screen.blit(rendered_text, text_rect)

def subtraction():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} - {b} =", a - b

def addition():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} + {b} =", a + b

def multiplication():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} * {b} =", a * b

def square():
    a = random.randint(1, 5)
    return f"{a}^2 =", a**2

def get_new_question():
    choice = random.randint(1, 4)
    if choice == 1:
        return subtraction()
    elif choice == 2:
        return addition()
    elif choice == 3:
        return multiplication()
    elif choice == 4:
        return square()

def level3_start():
    time = None
    questions_wrong = 0
    questions_asnwered = 0
    running = True
    user_input = ""
    eqn, ans = get_new_question()  
    message = ""  
    message_color = BLACK  
    answer_checked = False  
    message_time = 0  # Track when the message is shown
    message_duration = 500  # Time duration for the message (in milliseconds)
    timer = Timer(10)

    while running:
        timer.update(screen)
        screen.fill((0, 0, 0))

        screen.fill(WHITE)
        display_text(eqn, BLACK, HEIGHT // 3)  # Display the question text (centered)
        display_text("Your Answer: " + user_input, BLACK, HEIGHT // 2)  # Display the user input (centered)

        if message:  # Display the message only if it exists
            display_text(message, message_color, HEIGHT // 1.5)  # Display message (centered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not answer_checked:  
                    try:
                        user_answer = float(user_input.strip())
                        if isinstance(ans, list):  
                            if user_answer in ans:
                                message = "Correct!"
                                questions_asnwered+=1
                                message_color = GREEN
                                message_time = pygame.time.get_ticks()  # Set the message time
                                answer_checked = True  # Set answer as checked
                            else:
                                message = "Wrong!"
                                questions_wrong += 1
                                message_color = RED
                                message_time = pygame.time.get_ticks()  # Set the message time
                                answer_checked = True  # Set answer as checked
                        else:
                            if user_answer == ans:
                                message = "Correct!"
                                questions_asnwered+=1
                                message_color = GREEN
                                message_time = pygame.time.get_ticks()  # Set the message time
                                answer_checked = True  # Set answer as checked
                            else:
                                message = "Wrong!"
                                questions_wrong += 1
                                message_color = RED
                                message_time = pygame.time.get_ticks()  # Set the message time
                                answer_checked = True  # Set answer as checked
                    except ValueError:
                        message = "Invalid input!"
                        message_color = RED
                        message_time = pygame.time.get_ticks()  # Set the message time
                        answer_checked = True  # Set answer as checked

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode in "-.":
                        if event.unicode == "." and "." in user_input:
                            continue  
                        if event.unicode == "-" and len(user_input) > 0:
                            continue  
                        user_input += event.unicode

        timer.update(screen)
        pygame.display.update()
        if (questions_wrong == 3):
            #you_lost_screen(menu)
            return
        
        if (timer.is_time_up()):
            if (questions_asnwered>0 and (questions_asnwered // (questions_asnwered + questions_wrong))*100 >= 50):
                #level4_start()
                #print("You got over 50%")
                level_completed.play()
                level_4_integer.run()
                running = False
                return
            else:
                #print("You lost")
                return
        # If enough time has passed since the message was shown, clear it and show the next question
        if pygame.time.get_ticks() - message_time > message_duration and answer_checked:
            message = ""  # Clear the message
            eqn, ans = get_new_question()  # Get the next question
            user_input = ""  # Clear user input
            answer_checked = False  # Allow for a new answer to be checked

        pygame.display.flip()  

    pygame.quit()  # Properly close the Pygame window after the loop ends
