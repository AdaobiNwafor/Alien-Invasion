import pygame.font
from pygame.sprite import Group            # We will be making a group of ships

from ship import Ship


class Scoreboard:
    # Report the scoring information
    def __init__(self, ai_game):
        # This is specifically needed to create the ships
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for the scoring
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 40)
        # Prepare the initial score image
        self.prep_score()
        # Prepare the high score
        self.prep_high_score()
        # Prepare the current level
        self.prep_level()
        # Prepare the ships that show how many lives you have left
        self.prep_ships()

    def prep_score(self):
        # Turn the score into a rendered image
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_colour, self.settings.bg_colour)
        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        # Set the right edge of the score rect 20 pixels away from the right edge of the screen
        self.score_rect.right = self.screen_rect.right - 20
        # Set the top edge of the score rect 20 pixels down from the top of the screen
        self.score_rect.top = 20

# Turn the high score into a rendered image
    def prep_high_score(self):
        high_score_str = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, self.settings.bg_colour)
        self.high_score_rect = self.high_score_image.get_rect()
        # center the high score rectangle horizontally
        self.high_score_rect.centerx = self.screen_rect.centerx
        # Set the high score top attribute to match the top of the score image
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        # Turn the level into a rendered image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_colour, self.settings.bg_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

# Show how many ships are left
    def prep_ships(self):
        self.ships = Group()
        # For every ship the player has left
        for ship_number in range(self.stats.ships_left + 1):
            # The ship creates a ship
            ship = Ship(self.ai_game)
            # Ships appear next to each other with a 10 pixel margin on the left side of the group of ships
            ship.rect.x = 10 + ship_number * ship.rect.width
            # Ship appears 10 pixels down from the top of the screen
            ship.rect.y = 10
            # Add each new ship to the group of ships
            self.ships.add(ship)

# Check to see if there is a new high score
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

# Draw the score, high score, level and lives(ships) to the screen
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
