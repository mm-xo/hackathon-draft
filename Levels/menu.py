import pygame
from button import Button
import Level2
import Level_1_Dragger
pygame.init()

MENU_BG = pygame.image.load("Menu_BG.png")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def get_font(size):
    return pygame.font.Font("VCR_OSD_MONO_1.001.ttf", size)

def menu():
    pygame.display.set_caption("Menu")

    while True:
        screen.blit(MENU_BG, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Don't Fail!", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(pos=(400, 250), text_input="PLAY", font=get_font(75), base_color="#c42339", hovering_color="#dcdbdb")
        QUIT_BUTTON = Button(pos=(400, 350), text_input="QUIT", font=get_font(75), base_color="#c42339", hovering_color="#dcdbdb")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Level_1_Dragger.levelStart()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()

menu()
