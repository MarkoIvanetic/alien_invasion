import sys 

import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_play_button(ai_settings, ship, screen, stats, play_button, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:

        ai_settings.initialize_dynamic_settings()
        stats.game_active = True
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, stats, screen, ship, aliens)
        ship.center_ship()

def check_events(ai_settings, screen, stats, button, aliens, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, ship, screen, stats, button, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
        if event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            # Move the ship to the right.
            ship.moving_left = True  

        elif event.key == pygame.K_SPACE:
            # Create a new bullet and add it to the bullets group.
            fire_bullets(ai_settings, screen, ship, bullets)
            
def check_keyup_events(event, ship):
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            # Move the ship to the right.
            ship.moving_left = False  

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
        bullets.update()

        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        # collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

        if collisions:
            for aliens in collisions.values():

                for alien in aliens:
                    stats.score += ai_settings.get_alien_points(stats, alien.kill_points)

                sb.prep_score(stats)

        if len(aliens) == 0:
            ai_settings.next_level(stats)
            sb.prep_score(stats)
            bullets.empty()
            create_fleet(ai_settings, stats, screen, ship, aliens)    

def fire_bullets(ai_settings, screen, ship, bullets):
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1;

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, stats, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def create_fleet(ai_settings, stats, screen, ship, aliens):
    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            aliens.add(create_alien(ai_settings, screen, alien_number, row_number))

def create_alien(ai_settings, screen, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width + (2 * alien.rect.width * alien_number)
    alien.y = alien.rect.height + (1.5 * alien.rect.height * row_number)

    alien.rect.x = alien.x
    alien.rect.y = alien.y
    return alien   

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows

def update_screen(ai_settings, stats, screen, sb, ship, aliens, bullets, button):
     # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
            