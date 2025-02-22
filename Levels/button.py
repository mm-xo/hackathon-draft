class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        # Render the text once in the constructor
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        # Render the text on the screen
        screen.blit(self.text, self.rect)

    def checkForInput(self, pos):
        # Simplified collision check using rect.collidepoint
        if self.rect.collidepoint(pos):
            return True
        return False

    def changeColor(self, pos):
        # Change the color of the text based on mouse position
        if self.rect.collidepoint(pos):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)