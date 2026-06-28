"""Tests for shot_flash.py"""

import sys
from unittest.mock import Mock
import pygame
import pytest

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

from ..constants import BULLET_ANIMATION_COOLDOWN
from ..shot_flash import CShotFlash


@pytest.fixture
def mock_shot_flash():
    """Mock shot flash object."""
    return CShotFlash(0, 0, 1, 1, 1, 1)


def test_move(mock_shot_flash, monkeypatch):
    """Test move function."""
    mock_shot_flash.last_update = 0

    monkeypatch.setattr(pygame.time, 'get_ticks', Mock(return_value=BULLET_ANIMATION_COOLDOWN - 1))
    result = mock_shot_flash.move()
    assert result == [1, 1]

    monkeypatch.setattr(pygame.time, 'get_ticks', Mock(return_value=BULLET_ANIMATION_COOLDOWN + 1))
    mock_shot_flash.new_coordinates = Mock()
    result = mock_shot_flash.move()
    assert mock_shot_flash.new_coordinates.called
    assert result == [mock_shot_flash.x_pos, mock_shot_flash.y_pos]


def test_new_coordinates(mock_shot_flash):
    """Test new_coordinates function."""
    mock_shot_flash.reached = False
    mock_shot_flash.x_increment = 1
    mock_shot_flash.y_increment = 1

    # Not reached, decrement
    mock_shot_flash.new_coordinates()
    assert mock_shot_flash.x_pos == 0
    assert mock_shot_flash.y_pos == 0

    # Reached, increment in opposite direction
    mock_shot_flash.reached = True
    mock_shot_flash.new_coordinates()
    assert mock_shot_flash.x_pos == 1
    assert mock_shot_flash.y_pos == 1
