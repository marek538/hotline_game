"""Tests for shot_flash.py"""

import sys
from unittest.mock import Mock
import pytest
import pygame

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

from ..soldier_npc import PlayerNPC
from ..constants import PLAYER_DEFAULT_SOLDIER_PATH, PLAYER_DEAD_SOLDIER_PATH, SOLDIER_BURST_LENGTH


@pytest.fixture
def mock_player_npc():
    """Mock player npc object."""
    return PlayerNPC(0, 0,
                     PLAYER_DEFAULT_SOLDIER_PATH,
                     PLAYER_DEAD_SOLDIER_PATH)


def test_fire_soldier(mock_player_npc, monkeypatch):
    """Test fire_soldier function."""
    mock_player_npc.alive = True
    mock_player_npc.burst_length = 0
    mock_player_npc.able_to_fire = False

    mock_time_get_ticks = Mock(side_effect=[100, 200, 300])
    monkeypatch.setattr(pygame.time, 'get_ticks', mock_time_get_ticks)

    x_scale, y_scale = 1, 1
    player_x, player_y = 10, 20

    # Not able to fire
    result = mock_player_npc.fire_soldier(x_scale, y_scale, player_x, player_y, able_to_fire=False)
    assert result is None
    assert mock_player_npc.able_to_fire is False

    # Able to fire, but burst length exceeds limit
    mock_player_npc.burst_length = SOLDIER_BURST_LENGTH
    result = mock_player_npc.fire_soldier(x_scale, y_scale, player_x, player_y, able_to_fire=True)
    assert result is None
    assert mock_player_npc.able_to_fire is False

    # Able to fire, burst length within limit, but delay hasn't passed
    mock_player_npc.burst_length = 0
    result = mock_player_npc.fire_soldier(x_scale, y_scale, player_x, player_y, able_to_fire=True)
    assert result is None
    assert mock_player_npc.able_to_fire is True

    # Able to fire, burst length within limit, delay passed
    mock_player_npc.time_spotted = -500
    result = mock_player_npc.fire_soldier(x_scale, y_scale, player_x, player_y, able_to_fire=True)
    assert result.x_pos == mock_player_npc.location_x + 1
    assert result.y_pos == mock_player_npc.location_y + 1
    assert result.x_destination == player_x
    assert result.y_destination == player_y
