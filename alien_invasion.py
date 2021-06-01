import sys
from time import sleep

import pygame

from settings import Settings
from gamestats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_height, self.settings.screen_width))
        pygame.display.set_caption('Alien Invasion')     # at this point the screen ahs been created

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Make the play button
        self.play_button = Button(self, 'Start')
        # needs the self argument to give the ship access to the games resources
        self.ship = Ship(self)
        # Bullets and aliens are stored as a group using sprite
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()

# separating run game and the check events, mean you can separately run the game and make changes to the events separately
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # Start a new game when the button is clicked
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            # Call prepscore after resetting the game stats. Resets the scoreboard with a score of 0
            self.sb.prep_score()
            # Call prepscore after resetting the game stats. Resets the level with 0
            self.sb.prep_level()
            # Call prepscore shows how many lives they have to start with
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

# checking if an arrow key is pressed, if it is, check if it is the right or left arrow key. If it is, the ship moves
            # left or right
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

# when the key stops being pressed, if its left/right, the ship stops moving
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            # Move the ship to the right, on the x axis

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:     # If bullets on screen is less than 3,
            new_bullet = Bullet(self)                             # then new bullets added. only allowed to shoot bullets in groups of 3
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Updating the position of bullets and getting rid of old bullets
        # updating the bullets positions
        self.bullets.update()
        # getting rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # check for any bullets that have hit aliens and if they have, get rid of it
            self._check_bullet_alien_collisions()

    def create_fleet(self):
        # Making an alien and finding out the number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (alien_width)
        # finding out how many rows of aliens fit on the screen
        ship_height = self.ship.rect.height
        available_height_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_height_y // (4 * alien_height)
        # create the full fleet of aliens
        for row_number in range(number_rows):
            # Creating the first row of aliens
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

# update the position of all aliens in the fleet
    def _update_aliens(self):
        # check if the fleet is at an edge
        self._check_fleet_edges()
        self.aliens.update()
        self._check_alien_ship_collision()
        self._check_aliens_bottom()

# what to do if the aliens have reached the edge
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # changing the direction of the fleet. Multiplying by -1 on the x axis
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        # remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                # Score increases when aliens are killed. If multiple aliens are killed by the same bullet,
                # your score increases by how many aliens killed
                self.stats.score += self.settings.alien_points * len(aliens)
            # Call prepscore to create a new image for the updated score
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy the existing bullets and create a new fleet
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()
            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_alien_ship_collision(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        # Respond to the ship being hit by an alien
        # Reduce the number of ships left by 1 and show that on the screen with the ships
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.45)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        # check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # The same thing happens when a ship gets hit
                self._ship_hit()
                break

    def _update_screen(self):
        # updates the screen and draws the new screen
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Draw the score information
        self.sb.show_score()
        # Draws the start button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # draw the final screen
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
