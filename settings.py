class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 600
        self.screen_height = 1200
        self.bg_colour = (230, 230, 230)
        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 2
        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 5
        # Alien settings
        self.alien_speed = 3
        self.fleet_drop_speed = 20
        self.fleet_direction = 1                # fleet direction 1 = right, -1 = left
        # Difficulty settings
        self.speedup_scale = 1.2
        self.score_scale = 1.5      # In harder levels, the alien points increase

    def initialize_dynamic_settings(self):
        # Initialise the settings that change throughout the game
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 0.5
        self.fleet_direction = 1
        # Setting up the scoring
        self.alien_points = 10

    def increase_speed(self):
        # Increasing the speed settings and alien point values
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # Increases the score by integers
        self.alien_points = int(self.alien_points * self.score_scale)
