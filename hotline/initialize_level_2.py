"""Initialize level 2 of the game. This includes the player, enemies, and objects."""

import pygame
from player_soldier import PlayerSoldier
import constants
from load_image import make_background
from load_image import get_image
from add_object_functions import add_soldier, get_thin_wall, \
    get_thick_wall, add_rotten_table, add_next_to_rotten, add_car


def initialize_enemies(x, y):
    """Initialize enemies of the game."""
    enemies = []
    enemies.append(add_soldier(240, 240, x, y))
    enemies.append(add_soldier(95, 70, x, y))
    enemies.append(add_soldier(150, 285, x, y))
    enemies.append(add_soldier(10, 285, x, y))
    enemies.append(add_soldier(10, 290, x, y))
    enemies.append(add_soldier(240, 10, x, y))
    enemies.append(add_soldier(10, 240, x, y))

    return enemies


def initialize_objects():
    """Initialize objects of the game."""
    objects = []
    objects.extend(get_thick_wall((0, 25), (60, 25), True))
    objects.extend(get_thick_wall((80, 0), (80, 150), False))
    objects.extend(get_thick_wall((15, 150), (82, 150), True))
    objects.extend(get_thin_wall((15, 150), (15, 250), False))
    objects.extend(get_thin_wall((15, 250), (250, 250), True))
    objects.extend(get_thin_wall((248, 150), (248, 255), False))
    objects.extend(get_thick_wall((180, 25), (220, 25), True))
    objects.extend(get_thick_wall((180, 25), (180, 80), False))
    objects.extend(get_thick_wall((220, 25), (220, 80), False))
    objects.append(add_rotten_table(150, 150))
    objects.append(add_next_to_rotten(159, 150))
    objects.append(add_next_to_rotten(168, 150))
    objects.append(add_next_to_rotten(177, 150))
    objects.append(add_next_to_rotten(186, 150))
    objects.append(add_next_to_rotten(195, 150))

    objects.append(add_rotten_table(200, 80))
    objects.append(add_next_to_rotten(209, 80))
    objects.append(add_next_to_rotten(218, 80))
    objects.append(add_next_to_rotten(227, 80))
    objects.append(add_next_to_rotten(236, 80))
    objects.append(add_next_to_rotten(245, 80))
    objects.append(add_car(120, 15))

    objects.extend(get_thick_wall((80, 50), (180, 50), True))
    objects.extend(get_thick_wall((150, 0), (150, 50), False))

    return objects


# !!! first object is player, return list where first is objects and second is bg picture
# garage
def initialize_level_2():
    """Initialize level 2 of the game. This level is garage
    and initialization includes background and objects."""
    objects = [
        PlayerSoldier(10, 10,
                      constants.PLAYER_DEFAULT_SOLDIER_PATH,
                      constants.PLAYER_DEAD_SOLDIER_PATH)]

    objects.extend(initialize_enemies(10, 10))
    objects.extend(initialize_objects())

    sheet = pygame.image.load(constants.ENVIRONMENT_BROWN_BRICK_PATH).convert_alpha()
    bg_pattern = get_image(sheet,
                           0,
                           constants.ENVIRONMENT_BROWN_BRICK_WIDTH,
                           constants.ENVIRONMENT_BROWN_BRICK_HEIGHT,
                           constants.ENVIRONMENT_BROWN_BRICK_SCALE,
                           constants.BLACK)
    bg = make_background(bg_pattern, pygame.display.Info())

    return [objects, bg]
