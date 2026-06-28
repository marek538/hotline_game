"""Tests for game_map.py"""

import sys
from unittest.mock import Mock
import pytest
import pygame

# was not able to fix those errors
# pylint: disable=E1101,C0413
sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

from ..player_soldier import PlayerSoldier
from ..constants import (MAP_SIZE,
                         BULLET_SPEED,
                         PLAYER_DEFAULT_SOLDIER_PATH,
                         PLAYER_DEAD_SOLDIER_PATH)
from ..game_map import GameMap, in_grid, find_object_by_id
from ..shot_flash import CShotFlash
from ..soldier_npc import PlayerNPC


@pytest.fixture
def mock_game_map():
    """Fixture for GameMap class."""
    return GameMap(MAP_SIZE, MAP_SIZE)


def test_in_grid():
    """Test in_grid function."""
    assert in_grid((0, 0))
    assert in_grid((MAP_SIZE - 1, MAP_SIZE - 1))
    assert not in_grid((-1, 0))
    assert not in_grid((0, -1))
    assert not in_grid((MAP_SIZE, 0))
    assert not in_grid((0, MAP_SIZE))


def test_find_object_by_id(mock_game_map):
    """Test find_object_by_id function."""
    obj1 = Mock(get_id=lambda: 1)  # lambda to mock whole object and just return its id
    obj2 = Mock(get_id=lambda: 2)
    obj3 = Mock(get_id=lambda: 3)

    mock_game_map.moving_objects = [obj1, obj2, obj3]

    assert find_object_by_id(mock_game_map.moving_objects, 2) == obj2
    assert find_object_by_id(mock_game_map.moving_objects, 4) is None


def test_add_object(mock_game_map):
    """Test add_object function."""
    element = Mock(coord_x=lambda: 0,
                   coord_y=lambda: 0,
                   get_size=lambda: 2,
                   is_movable=True,
                   passable=True,
                   is_showable=True)

    mock_game_map.add_object(element)

    assert len(mock_game_map.moving_objects) == 1
    assert len(mock_game_map.map_grid[0][0]) == 1


def test_resolve_out_of_grid(mock_game_map):
    """Test resolve_out_of_grid function for CShotFlash."""
    obj = CShotFlash(0, 0, 1, 1, 1, 1)
    prev_coord = [0, 0]

    mock_game_map.moving_objects.append(obj)
    mock_game_map.resolve_out_of_grid(obj, prev_coord)

    assert len(mock_game_map.map_grid[0][0]) == 0


def test_resolve_collision(mock_game_map):
    """Test resolve_collision function for CShotFlash."""
    obj = CShotFlash(0, 0, 1, 1, 1, 1)
    prev_coord = [0, 0]
    new_coord = [1, 1]

    other_obj = Mock(passable=lambda: False, get_hit=Mock())
    mock_game_map.map_grid[1][1].append(other_obj)

    mock_game_map.moving_objects.append(obj)
    mock_game_map.resolve_collision(obj, prev_coord, new_coord)

    assert len(mock_game_map.map_grid[1][1]) == 1


def test_move_object(mock_game_map):
    """Test move_object function."""
    obj = CShotFlash(0, 0, 1, 1, 1, 1)
    prev_coord = [0, 0]

    mock_game_map.moving_objects.append(obj)
    mock_game_map.move_object(obj, prev_coord)

    assert len(mock_game_map.map_grid[0][0]) == 0
    assert len(mock_game_map.map_grid[1][1]) == 1


def test_move_all_objects(mock_game_map):
    """Test move_all_objects function moves all objects to desired location."""
    obj = CShotFlash(0, 0, BULLET_SPEED + 1, 0, 1, 1)
    pygame.time.delay(10)
    mock_game_map.add_object(obj)
    mock_game_map.move_all_objects()

    assert len(mock_game_map.moving_objects) == 1
    assert len(mock_game_map.map_grid[0][0]) == 0
    print(mock_game_map.map_grid[7][0])
    assert len(mock_game_map.map_grid[7][0]) == 1


def test_remove_object(mock_game_map):
    """Test remove_object function."""
    obj = Mock(get_id=lambda: 1, coord_x=lambda: 0, coord_y=lambda: 0, get_size=lambda: 2)
    mock_game_map.add_object(obj)
    mock_game_map.remove_object(0, 0, 1, 2)
    assert len(mock_game_map.map_grid[0][0]) == 0


def test_game_state(mock_game_map):
    """Test game_state function."""
    player = PlayerSoldier(0, 0,
                           PLAYER_DEFAULT_SOLDIER_PATH,
                           PLAYER_DEAD_SOLDIER_PATH,
                           showable=True)

    player.alive = False
    mock_game_map.add_object(player)

    assert mock_game_map.game_state() == -1

    mock_game_map.moving_objects[0].alive = True
    player_npc = PlayerNPC(0, 0, PLAYER_DEFAULT_SOLDIER_PATH,
                           PLAYER_DEAD_SOLDIER_PATH)

    player_npc.alive = False
    mock_game_map.add_object(player_npc)
    assert mock_game_map.game_state() == 1

    mock_game_map.moving_objects[1].alive = True



def test_able_to_fire(mock_game_map):
    """Test able_to_fire function."""
    player = PlayerSoldier(15, 15,
                           PLAYER_DEFAULT_SOLDIER_PATH,
                           PLAYER_DEAD_SOLDIER_PATH,
                           showable=True)
    mock_game_map.add_object(player)
    mock_game_map.set_player_id(player.get_id())
    player_npc = PlayerNPC(30, 15, PLAYER_DEFAULT_SOLDIER_PATH,
                           PLAYER_DEAD_SOLDIER_PATH)
    mock_game_map.add_object(player_npc)

    assert mock_game_map.able_to_fire(player_npc.coord_x(),
                                      player_npc.coord_y(),
                                      player.coord_x(),
                                      player.coord_y(),
                                      player_npc.get_id())
    assert not mock_game_map.able_to_fire(player_npc.coord_x(),
                                          player_npc.coord_y(),
                                          0, 0,
                                          player_npc.get_id())
