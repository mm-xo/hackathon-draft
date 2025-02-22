import pygame
from button import Button
# import Level_2
from Level_2 import Level_2
from Level_3 import Level_3
from Level_4 import Level_4
# from Level_3 import level3_start
import Level_1
pygame.init()
pygame.mixer.init()

MENU_BG = pygame.image.load("Images/blue_BG.png")

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def get_font(size):
    return pygame.font.Font("Font/GameFont.ttf", size)

def menu():
    pygame.display.set_caption("Menu")

    while True:
        screen.blit(MENU_BG, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Don't Fail!", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 300))

        PLAY_BUTTON = Button(pos=(640, 400), text_input="PLAY", font=get_font(75), base_color="#c42339", hovering_color="#dcdbdb")
        QUIT_BUTTON = Button(pos=(640, 500), text_input="QUIT", font=get_font(75), base_color="#c42339", hovering_color="#dcdbdb")

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
                    level1_result = Level_1.level1_start()
                    print(level1_result)
                    if level1_result:  # If Level 1 is completed
                        level2 = Level_2(screen)  # Pass the screen object
                        level2_result = level2.level2_start()
                        
                        if level2_result:  # If Level 2 is completed
                            level3 = Level_3(screen)
                            level3_result = level3.level3_start()
                            
                            if (level3_result):
                                level4 = Level_4()
                                level4.run()
                                continue
                        
                    # if Level_1.level1_start():  # Make sure Level 1 returns True when completed
                    #     level2 = Level_2(screen)  
                    #     level2_result = level2.level2_start()
                        
                    #     if level2_result:  # Level 2 completed successfully
                    #         level3 = Level_3(screen)  # Pass screen
                    #         level3.level3_start()
                # if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     if Level_1.level1_start():
                #         level2 = Level_2(screen)  # Pass the screen object
                #         level2_result = level2.level2_start()
                #         # level2_start()
                #         if level2_result:  # If Level 2 is completed
                #             level3 = Level_3()
                #             level3.level3_start()
                #         #     print("Level 2 completed! Returning to menu.")
                #         # else:
                #         #     print("Level 2 failed! Returning to menu.")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()

menu()