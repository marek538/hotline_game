"""This file contains the class for bullet animation and movement direction."""

from random import randrange

import math
import pygame
import constants
from load_image import get_image


# pylint: disable=too-many-instance-attributes, too-many-arguments
# attributes and arguments are fine
class CShotFlash:
    """Class that represents bullet animation and movement direction."""
    fire_flash = pygame.image.load(constants.BULLET_LOCATION).convert_alpha()

    def __init__(self, x, y, xd, yd, sc_x, sc_y, showable=False):
        self.showable = showable
        self.id = randrange(1000000000)
        self.x_pos = x
        self.y_pos = y
        self.x_destination = xd
        self.y_destination = yd

        self.size_in_grid = constants.BULLET_HITBOX

        self.load_animation()
        self.scale_x = sc_x
        self.scale_y = sc_y

        x_diff = abs(self.x_pos - self.x_destination)
        y_diff = abs(self.y_pos - self.y_destination)

        if x_diff == 0:
            x_dir = 0
        else:
            x_dir = (self.x_destination - self.x_pos) / x_diff

        if y_diff == 0:
            y_dir = 0
        else:
            y_dir = (self.y_destination - self.y_pos) / y_diff

        self.x_pos += (int(x_dir * constants.SOLDIER_HITBOX / 2))
        self.y_pos += (int(y_dir * constants.SOLDIER_HITBOX / 2))
        dist = math.sqrt((self.x_pos - self.x_destination) ** 2 +
                         (self.y_pos - self.y_destination) ** 2)
        if dist == 0:
            self.exists = False
        else:
            scale = constants.BULLET_SPEED / dist
            self.x_increment = scale * (self.x_pos - self.x_destination)
            self.y_increment = scale * (self.y_pos - self.y_destination)

        self.angle = math.degrees(math.atan2(x - xd, y - yd))
        self.animation_fire = pygame.transform.rotate(self.animation_fire, self.angle - 90)

        self.last_update = pygame.time.get_ticks()

        self.reached = False
        self.exists = True

    def load_animation(self):
        """This function loads animations from sprite sheet."""
        self.animation_fire = get_image(self.fire_flash, 0, 3, 1, 2, constants.BLACK)

    def show_object(self, win, scale_x, scale_y):
        """This function is called every frame and shows object on the screen."""
        if not self.showable:
            return None
        shot_rec = self.animation_fire.get_rect(center=(self.x_pos * scale_x, self.y_pos * scale_y))

        win.blit(self.animation_fire, shot_rec)
        return self.exists

    def move(self):
        """This function is called every frame and moves object on the screen."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= constants.BULLET_ANIMATION_COOLDOWN:
            self.new_coordinates()
            self.last_update = current_time

        return [self.x_pos, self.y_pos]

    def new_coordinates(self):
        """This function changes coordinates and thus moves the object."""
        if self.reached is False:
            self.x_pos = int(self.x_pos - self.x_increment)
            self.y_pos = int(self.y_pos - self.y_increment)
        else:
            self.x_pos = int(self.x_pos + self.x_increment)
            self.y_pos = int(self.y_pos + self.y_increment)

    def coord_x(self):
        """This function returns x coordinate of object."""
        return self.x_pos

    def coord_y(self):
        """This function returns y coordinate of object."""
        return self.y_pos

    def set_coord(self, x, y):
        """This function sets new coordinates of object."""
        self.x_pos = x
        self.y_pos = y

    @property
    def is_movable(self):
        """This function returns True if object is movable."""
        return True

    def get_hit(self):
        """This function is called when object is hit by bullet."""
        return

    def get_id(self):
        """This function returns id of object."""
        return self.id

    def get_size(self):
        """This function returns size of object."""
        return self.size_in_grid

    def change_showable(self, showable):
        """This function changes showable attribute."""
        self.showable = showable

    def passable(self):
        """This function returns True if object can be moved through."""
        return True
