"""Tests for add_object_functions.py"""

import sys
import pytest
import pygame

# was not able to fix those errors
# pylint: disable=E1101,C0413
sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
pygame.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

from ..add_object_functions import (get_thin_wall,
                                    get_thick_wall,
                                    add_thin_wall_brick,
                                    add_thick_wall_brick)


def equals(a, b):
    """Operator overloading for comparing two terrain objects."""
    return a.location_x == b.location_x and a.location_y == b.location_y


@pytest.mark.parametrize("start_coord, end_coord, row, expected_result", [
    ((0, 0), (10, 0), True, [add_thin_wall_brick(0, 0, False), add_thin_wall_brick(5, 0, False)]),
    ((0, 0), (0, 10), False, [add_thin_wall_brick(0, 0, True), add_thin_wall_brick(0, 5, True)]),
    ((0, 0), (100, 0), False, []),
    ((0, 0), (0, 100), True, []),
])
def test_get_thin_wall(start_coord, end_coord, row, expected_result):
    """Test test_get_thin_wall function returns desired number of bricks in correct order."""
    result = get_thin_wall(start_coord, end_coord, row)
    print(result)
    # pylint: disable=consider-using-enumerate
    # enumerate is not needed here
    for i in range(len(result)):
        assert equals(result[i], expected_result[i])


@pytest.mark.parametrize("start_coord, end_coord, row, expected_result", [
    ((0, 0), (10, 0), True, [add_thick_wall_brick(0, 0, False), add_thick_wall_brick(6, 0, False)]),
    ((0, 0), (0, 10), False, [add_thick_wall_brick(0, 0, True), add_thick_wall_brick(0, 6, True)]),
    ((0, 0), (100, 0), False, []),
    ((0, 0), (0, 100), True, []),
])
def test_get_thick_wall(start_coord, end_coord, row, expected_result):
    """Test get_thick_wall function returns desired number of bricks in correct order."""
    result = get_thick_wall(start_coord, end_coord, row)
    # pylint: disable=consider-using-enumerate
    # enumerate is not needed here
    for i in range(len(result)):
        assert equals(result[i], expected_result[i])
