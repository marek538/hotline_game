"""Tests for player_soldier.py"""

import sys
from unittest.mock import Mock
import pytest
import pygame

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
pygame.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

from ..constants import PLAYER_DEFAULT_SOLDIER_PATH, PLAYER_DEAD_SOLDIER_PATH, SOLDIER_SPEED
from ..player_soldier import PlayerSoldier


@pytest.fixture
def mock_soldier():
    return PlayerSoldier(0, 0,
                         PLAYER_DEFAULT_SOLDIER_PATH,
                         PLAYER_DEAD_SOLDIER_PATH)


def test_player_soldier_move(mock_soldier):
    """Test player_soldier move function."""
    print(sys.path)

    # Initial position
    assert mock_soldier.location_x == 0
    assert mock_soldier.location_y == 0

    keys = {pygame.K_a: True,
            pygame.K_d: False,
            pygame.K_w: False,
            pygame.K_s: False}

    # Move left
    mock_soldier.move_soldier(keys)
    assert mock_soldier.location_x == -SOLDIER_SPEED
    assert mock_soldier.location_y == 0

    keys[pygame.K_a] = False
    keys[pygame.K_d] = True

    # Move right
    mock_soldier.move_soldier(keys)
    assert mock_soldier.location_x == 0
    assert mock_soldier.location_y == 0

    keys[pygame.K_d] = False
    keys[pygame.K_w] = True

    # Move up
    mock_soldier.move_soldier(keys)
    assert mock_soldier.location_x == 0
    assert mock_soldier.location_y == -SOLDIER_SPEED

    keys[pygame.K_w] = False
    keys[pygame.K_s] = True

    # Move down
    mock_soldier.move_soldier(keys)
    assert mock_soldier.location_x == 0
    assert mock_soldier.location_y == 0


def test_fire_soldier_when_not_alive(mock_soldier):
    """Test fire_soldier function when soldier is not alive."""
    mock_soldier.alive = False
    result = mock_soldier.fire_soldier(1, 1, 0, 0)
    assert result is None


def test_fire_soldier(mock_soldier, monkeypatch):
    """Test fire_soldier function when soldier is alive."""
    mock_soldier.alive = True
    mock_mouse_pos = Mock(return_value=(10, 10))
    monkeypatch.setattr(pygame.mouse, 'get_pos', mock_mouse_pos)

    shot_object = mock_soldier.fire_soldier(1, 1, 0, 0)

    assert shot_object.x_pos == mock_soldier.location_x + 1
    assert shot_object.y_pos == mock_soldier.location_y + 1
    assert shot_object.x_destination == 10  # 10 / 2
    assert shot_object.y_destination == 10  # 20 / 2
    assert shot_object.scale_x == 1
    assert shot_object.scale_y == 1
