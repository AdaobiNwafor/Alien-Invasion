import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        # Initialise the button attributes
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # Set dimensions/properties of the button
        self.width, self.height = 200, 50
        self.button_colour = (0, 255, 0)
        self.text_colour = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        # Buttons rectangle and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # The buttons message needs to be prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # Turn the message into a rendered image and center tect on the button
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw the blank button, then draw the message
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
