import math

class Settings():

    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 640
        self.bg_color = (230, 230, 230)

        # Ship settings
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3
        self.ship_speedup = 1.05

        # Bullet settings
        # self.bullet_speed_factor = 3
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 10
        # self.alien_speed_factor = 1
        # self.fleet_direction = 1

        # Level settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5


        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def next_level(self, stats):
        """Increase speed settings."""
        self.ship_speed_factor *= self.ship_speedup
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        stats.level += 1

    def get_alien_points(self, stats, original_points):
        """Increase speed settings."""
        float_points = original_points * math.pow(self.score_scale, stats.level)
        return int(float_points + (float_points % 25))