import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard

from ship import Ship
from alien import Alien
from button import Button

import game_functions as gf
from pygame.sprite import Group

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.play_button = Button(self.settings, self.screen, "Play")
        self.stats = GameStats(self.settings)

        self.sb = Scoreboard(self.settings, self.screen, self.stats)

        self.ship = Ship(self.settings, self.screen)

        # Make a group to store bullets in.
        self.bullets = Group()

        self.aliens = Group()
        gf.create_fleet(self.settings, self.stats, self.screen, self.ship, self.aliens)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            gf.check_events(self.settings, self.screen, self.stats, self.play_button, self.aliens, self.ship, self.bullets)

            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self.settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets)
                gf.update_aliens(self.settings, self.stats, self.screen, self.ship, self.aliens, self.bullets)
            
            gf.update_screen(self.settings, self.stats, self.screen, self.sb, self.ship, self.aliens, self.bullets, self.play_button)



if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()