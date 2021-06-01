import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # A class to manage the bullets fired from the ship
    def __init__(self, ai_game):
        # Creat a bullet at the ships current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        # create a bullet rectangle at (0,0) then set the correct position
        # using pygame.Rect, we are building a rectangle from scratch
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # the bullet will emerge from the top of the ship
        self.rect.midtop = ai_game.ship.rect.midtop
        # store bullets position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        # moving the bullet up the screen
        # updating the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # updating the rectangle position
        self.rect.y = self.y

    def draw_bullet(self):
        # draw the bullet to the screen.
        # it fills in the part of the screen that is defined by the bullets rectangle with the bullets colour
        pygame.draw.rect(self.screen, self.colour, self.rect)
