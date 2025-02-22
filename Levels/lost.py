# lost.py
import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def you_lost_screen(menu):
    #from menu import menu  # Import menu function inside the function to avoid circular imports

    pygame.display.set_caption("You Lost")
    font = pygame.font.Font("Font/GameFont.ttf", 60)
    button_font = pygame.font.Font("Font/GameFont.ttf", 40)

    bg_color = (30, 30, 30)
    text_color = (255, 0, 0)
    button_color = (100, 100, 255)
    button_hover_color = (150, 150, 255)

    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 80)
    running = True

    while running:
        screen.fill(bg_color)

        # "You Lost" text
        text_surface = font.render("YOU LOST!", True, text_color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 200))

        # Button hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_color_current = button_hover_color if button_rect.collidepoint(mouse_x, mouse_y) else button_color

        # Draw button
        pygame.draw.rect(screen, button_color_current, button_rect, border_radius=15)
        button_text = button_font.render("Main Menu", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 30, button_rect.y + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse_x, mouse_y):
                menu()  # Call menu function after the import
                running = False  # Close the screen after clicking

        pygame.display.update()