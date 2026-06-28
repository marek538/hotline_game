"""Initialize level 3 of the game. This includes the player, enemies, and objects."""

import pygame
from player_soldier import PlayerSoldier
import constants
from load_image import make_background
from load_image import get_image
from add_object_functions import add_soldier, get_thin_wall, add_piano


def initialize_enemies(x, y):
    """Initialize enemies of the game."""
    enemies = []
    enemies.append(add_soldier(240, 240, x, y))
    enemies.append(add_soldier(95, 70, x, y))
    enemies.append(add_soldier(170, 285, x, y))
    enemies.append(add_soldier(10, 285, x, y))

    return enemies


def initialize_objects():
    """Initialize objects of the game."""
    objects = []
    objects.append(add_piano(150, 150))

    objects.extend(get_thin_wall((100, 100), (100, 200), False))
    objects.extend(get_thin_wall((200, 100), (200, 180), False))
    objects.extend(get_thin_wall((100, 100), (200, 100), True))
    objects.extend(get_thin_wall((100, 200), (200, 200), True))

    objects.extend(get_thin_wall((210, 150), (300, 150), True))
    objects.extend(get_thin_wall((0, 150), (90, 150), True))

    objects.extend(get_thin_wall((150, 200), (150, 290), False))
    objects.extend(get_thin_wall((150, 0), (150, 90), False))

    return objects


# !!! first object is player, return list where first is objects and second is bg picture
# living room
def initialize_level_3():
    """Initialize level 3 of the game. This level is living room
    and initialization includes background and objects."""
    objects = [
        PlayerSoldier(120, 120, constants.PLAYER_DEFAULT_SOLDIER_PATH,
                      constants.PLAYER_DEAD_SOLDIER_PATH)]

    objects.extend(initialize_enemies(120, 120))
    objects.extend(initialize_objects())

    sheet = pygame.image.load(constants.ENVIRONMENT_CARPET_PATH).convert_alpha()
    bg_pattern = get_image(sheet,
                           0,
                           constants.ENVIRONMENT_CARPET_WIDTH,
                           constants.ENVIRONMENT_CARPET_HEIGHT,
                           constants.ENVIRONMENT_CARPET_SCALE,
                           constants.BLACK)

    bg = make_background(bg_pattern, pygame.display.Info())

    return [objects, bg]
