import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        # initialise ship starting position
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # load ship image and get its rect
        self.image = pygame.image.load('C:\\Users\\adaob\\PycharmProjects\\pythonProject1\\projects\\alien invasion\\images\\ship.bmp')
        self.rect = self.image.get_rect()
        # start new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # store a decimal for the ships horizontal position
        self.x = float(self.rect.x)

    # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # updating the ships position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        # center the ship on the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        # draw ship at its current location
        self.screen.blit(self.image, self.rect)

