"""Initialize level 1 of the game. This includes the player, enemies, and objects."""

import pygame
from player_soldier import PlayerSoldier
import constants
from load_image import make_background
from load_image import get_image
from add_object_functions import add_soldier, add_kitchen_sink, add_kitchen_oven, get_thin_wall, \
    get_thick_wall


def get_furniture(start_coord):
    """Returns block of kitchen furniture."""
    walls = []
    walls.append(add_kitchen_sink(start_coord[0], start_coord[1]))
    walls.append(add_kitchen_oven(start_coord[0], start_coord[1] + 12))
    walls.append(add_kitchen_sink(start_coord[0], start_coord[1] + 2 * 12))
    walls.append(add_kitchen_oven(start_coord[0], start_coord[1] + 3 * 12))
    walls.append(add_kitchen_oven(start_coord[0], start_coord[1] + 4 * 12))
    return walls


# !!! first object is player, return list where first is objects and second is bg picture
# kitchen
def initialize_level_1() -> list:
    """Initialize level 1 of the game. This level is kitchen
    and initialization includes background and objects."""
    objects = [
        PlayerSoldier(10, 10,
                      constants.PLAYER_DEFAULT_SOLDIER_PATH,
                      constants.PLAYER_DEAD_SOLDIER_PATH)]
    objects.extend(initialize_enemies(10, 10))
    objects.extend(initialize_objects())

    sheet = pygame.image.load(constants.ENVIRONMENT_KITCHEN_FLOOR_PATH).convert_alpha()
    bg_pattern = get_image(sheet,
                           0,
                           constants.ENVIRONMENT_KITCHEN_FLOOR_WIDTH,
                           constants.ENVIRONMENT_KITCHEN_FLOOR_HEIGHT,
                           constants.ENVIRONMENT_KITCHEN_FLOOR_SCALE,
                           constants.BLACK)

    bg = make_background(bg_pattern, pygame.display.Info())

    return [objects, bg]


def initialize_enemies(x, y) -> list:
    """Initialize enemies of the game."""
    enemy = []
    enemy.append(add_soldier(constants.MAP_SIZE - 60, constants.MAP_SIZE - 60, x, y))
    enemy.append(add_soldier(95, 50, x, y))
    enemy.append(add_soldier(150, constants.MAP_SIZE - 15, x, y))
    enemy.append(add_soldier(10, constants.MAP_SIZE - 15, x, y))
    enemy.append(add_soldier(220, 133, x, y) )
    return enemy


def initialize_objects():
    """Initialize objects of the game."""
    walls = []

    walls.extend(get_thin_wall((0, 35),
                               (constants.MAP_SIZE - 15, 35), True))
    walls.extend(
        get_thin_wall((constants.MAP_SIZE - 18, 38),
                      (constants.MAP_SIZE - 18, constants.MAP_SIZE - 15),
                      False))
    walls.extend(get_thin_wall((35, 38), (35, constants.MAP_SIZE - 15), False))
    walls.extend(get_thin_wall((80, 0), (80, 20), False))
    walls.extend(get_thin_wall((160, 0), (160, 20), False))
    walls.extend(get_thin_wall((210, 0), (210, 20), False))
    walls.extend(get_thick_wall((160, 60), (210, constants.MAP_SIZE - 15), False))

    walls.extend(get_thin_wall((80, 150), (160, 150), True))
    walls.extend(get_thin_wall((80, 150), (80, constants.MAP_SIZE), False))

    walls.extend(get_thin_wall((200,100), (200, 175), False))
    walls.extend(get_thin_wall((200, 175), (240, 175), True))
    walls.extend(get_thin_wall((240, 150), (240, 180) , False))
    walls.extend(get_thin_wall((200, 100), (240, 100), True))
    walls.extend(get_thin_wall((240, 100), (240, 130) , False))

    walls.extend(get_furniture((10, 60)))
    walls.extend(get_furniture((40, 60)))
    walls.extend(get_furniture((40, 60 + 6 * 12)))
    walls.extend(get_furniture((150, 160)))
    walls.extend(get_furniture((275, 150)))

    walls.append(add_kitchen_sink(235, 165))
    return walls
