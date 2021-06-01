import pygame
from pygame.sprite import Sprite


# Represents a single alien in a fleet
class Alien(Sprite):
    def __init__(self, ai_game):
    # Aliens starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('C:\\Users\\adaob\\PycharmProjects\\pythonProject1\\projects\\alien invasion\\images\\alien.bmp')
        self.rect = self.image.get_rect()
        # New alien starting at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # store the aliens horizontal position
        self.x = float(self.rect.x)
        # store the aliens vertical position
        self.y = float(self.rect.y)

    def check_edges(self):
        # return true if alien is at the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # moving the aliens to the right
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
