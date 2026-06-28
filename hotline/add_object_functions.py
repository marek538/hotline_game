"""This file contains functions that add objects to the game map."""

import constants
from soldier_npc import PlayerNPC
from terrain import Terrain


def add_soldier(x, y, x_look, y_look):
    """Return npc with location x, y looking in direction look."""
    npc = PlayerNPC(x, y, constants.NPC_RED_SOLDIER_PATH,
                    constants.NPC_RED_DEAD_SOLDIER_PATH)
    npc.set_look(x_look, y_look)
    return npc


def add_thin_wall_brick(x, y, row):
    """Add thin wall brick to the game map."""
    rotation = 90
    if row:
        rotation = 0
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_THIN_WALL_PATH,
                   constants.ENVIRONMENT_THIN_WALL_HITBOX,
                   constants.ENVIRONMENT_THIN_WALL_SCALE,
                   constants.ENVIRONMENT_THIN_WALL_WIDTH,
                   constants.ENVIRONMENT_THIN_WALL_HEIGHT,
                   rotation=rotation)


def add_kitchen_sink(x, y):
    """Add kitchen sink to the game map."""
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_KITCHEN_SINK_PATH,
                   constants.ENVIRONMENT_KITCHEN_SINK_HITBOX,
                   constants.ENVIRONMENT_KITCHEN_SINK_SCALE,
                   constants.ENVIRONMENT_KITCHEN_SINK_WIDTH,
                   constants.ENVIRONMENT_KITCHEN_SINK_HEIGHT)


def add_kitchen_oven(x, y):
    """Add kitchen oven to the game map."""
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_KITCHEN_OVEN_PATH,
                   constants.ENVIRONMENT_KITCHEN_OVEN_HITBOX,
                   constants.ENVIRONMENT_KITCHEN_OVEN_SCALE,
                   constants.ENVIRONMENT_KITCHEN_OVEN_WIDTH,
                   constants.ENVIRONMENT_KITCHEN_OVEN_HEIGHT)


def add_thick_wall_brick(x, y, row):
    """Add thick wall brick to the game map."""
    rotation = 0
    if row:
        rotation = 90
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_THICK_WALL_PATH,
                   constants.ENVIRONMENT_THICK_WALL_HITBOX,
                   constants.ENVIRONMENT_THICK_WALL_SCALE,
                   constants.ENVIRONMENT_THICK_WALL_WIDTH,
                   constants.ENVIRONMENT_THICK_WALL_HEIGHT,
                   rotation=rotation)


def add_piano(x, y):
    """Add piano to the game map."""
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_PIANO_PATH,
                   constants.ENVIRONMENT_PIANO_HITBOX,
                   constants.ENVIRONMENT_PIANO_SCALE,
                   constants.ENVIRONMENT_PIANO_WIDTH,
                   constants.ENVIRONMENT_PIANO_HEIGHT)


def add_rotten_table(x, y):
    """Add rotten table to the game map."""
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_ROTTEN_TABLE_PATH,
                   constants.ENVIRONMENT_ROTTEN_TABLE_HITBOX,
                   constants.ENVIRONMENT_ROTTEN_TABLE_SCALE,
                   constants.ENVIRONMENT_ROTTEN_TABLE_WIDTH,
                   constants.ENVIRONMENT_ROTTEN_TABLE_HEIGHT)


def add_next_to_rotten(x, y):
    """Add next part of rotten table to the game map."""
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_NEXT_TO_ROTTEN_PATH,
                   constants.ENVIRONMENT_NEXT_TO_ROTTEN_HITBOX,
                   constants.ENVIRONMENT_NEXT_TO_ROTTEN_SCALE,
                   constants.ENVIRONMENT_NEXT_TO_ROTTEN_WIDTH,
                   constants.ENVIRONMENT_NEXT_TO_ROTTEN_HEIGHT)


def get_thin_wall(start_coord, end_coord, row):
    """Return whole thin wall."""
    walls = []
    if row:
        for x in range(start_coord[0], end_coord[0], constants.ENVIRONMENT_THIN_WALL_HITBOX):
            walls.append(add_thin_wall_brick(x, end_coord[1], False))
    else:
        for y in range(start_coord[1], end_coord[1], constants.ENVIRONMENT_THIN_WALL_HITBOX):
            walls.append(add_thin_wall_brick(start_coord[0], y, True))

    return walls


def get_thick_wall(start_coord, end_coord, row):
    """Return whole thick wall."""
    walls = []
    if row:
        for x in range(start_coord[0], end_coord[0], constants.ENVIRONMENT_THICK_WALL_HITBOX):
            walls.append(add_thick_wall_brick(x, end_coord[1], False))
    else:
        for y in range(start_coord[1], end_coord[1], constants.ENVIRONMENT_THICK_WALL_HITBOX):
            walls.append(add_thick_wall_brick(start_coord[0], y, True))

    return walls


def add_car(x, y):
    """Add car to the game map."""
    return Terrain(x,
                   y,
                   constants.ENVIRONMENT_CAR_PATH,
                   constants.ENVIRONMENT_CAR_HITBOX,
                   constants.ENVIRONMENT_CAR_SCALE,
                   constants.ENVIRONMENT_CAR_WIDTH,
                   constants.ENVIRONMENT_CAR_HEIGHT)
