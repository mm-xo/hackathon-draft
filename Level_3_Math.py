import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Math Quiz")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

font = pygame.font.SysFont("Arial", 24)

button_rect = pygame.Rect(200, 350, 100, 40)  # "Next" button position & size

def display_text(text, color, y_pos):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (50, y_pos))

def subtraction():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} - {b} =", a - b

def addition():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} + {b} =", a + b

def multiplication():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} * {b} =", a * b

def division():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} / {b} =", round(a / b, 2)

def generate_quadratic():
    a, b, c = random.randint(1, 5), random.randint(-10, 10), random.randint(-20, 20)
    discriminant = b**2 - 4*a*c

    while discriminant < 0:
        a, b, c = random.randint(1, 5), random.randint(-10, 10), random.randint(-20, 20)
        discriminant = b**2 - 4*a*c

    root1, root2 = (-b + math.sqrt(discriminant)) / (2 * a), (-b - math.sqrt(discriminant)) / (2 * a)
    return f"{a}x² + {b}x + {c} = 0", sorted((round(root1, 2), round(root2, 2)))

def square():
    a = random.randint(1, 5)
    return f"{a}^2 =", a**2

def draw_button():
    pygame.draw.rect(screen, BLUE, button_rect, border_radius=8)  # Rounded edges
    text_surface = font.render("Next", True, WHITE)  
    text_rect = text_surface.get_rect(center=button_rect.center)  
    screen.blit(text_surface, text_rect)  

def get_new_question():
    choice = random.randint(1, 6)
    if choice == 1:
        return subtraction()
    elif choice == 2:
        return addition()
    elif choice == 3:
        return multiplication()
    elif choice == 4:
        return division()
    elif choice == 5:
        return generate_quadratic()
    elif choice == 6:
        return square()

def game_loop():
    running = True
    user_input = ""
    eqn, ans = get_new_question()  
    message = ""  
    message_color = BLACK  
    answer_checked = False  

    while running:
        screen.fill(WHITE)  
        draw_button()
        display_text(eqn, BLACK, 100)
        display_text("Your Answer: " + user_input, BLACK, 150)
        display_text(message, message_color, 200)  

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
                                message_color = GREEN
                            else:
                                message = "Wrong!"
                                message_color = RED
                        else:
                            if user_answer == ans:
                                message = "Correct!"
                                message_color = GREEN
                            else:
                                message = "Wrong!"
                                message_color = RED
                        answer_checked = True  
                    except ValueError:
                        message = "Invalid input!"
                        message_color = RED

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode in "-.":
                        if event.unicode == "." and "." in user_input:
                            continue  
                        if event.unicode == "-" and len(user_input) > 0:
                            continue  
                        user_input += event.unicode  

            elif event.type == pygame.MOUSEBUTTONDOWN:  
                if button_rect.collidepoint(event.pos) and user_input.strip() != "":  
                    eqn, ans = get_new_question()  
                    user_input = ""  
                    message = ""  
                    answer_checked = False  
                elif button_rect.collidepoint(event.pos) and user_input.strip() == "":  # If no input, show a message
                    message = "Please enter a valid answer before proceeding."
                    message_color = RED  

        pygame.display.flip()  

game_loop()
pygame.quit()
