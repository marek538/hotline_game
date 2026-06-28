"""This module represents all static objects on map."""

from random import randrange
import pygame
import constants
from load_image import get_image


class Terrain:
    """Class that represents all static objects on map."""

    # pylint: disable=too-many-instance-attributes, too-many-arguments
    # attributes and arguments are fine
    def __init__(self, posx, posy, path, hitbox, scale, pic_width,
                 pic_height, showable=False, rotation=0):
        self.showable = showable
        self.location_x = posx
        self.location_y = posy
        self.picture = pygame.image.load(path).convert_alpha()
        self.size_in_grid = hitbox

        self.animation = get_image(self.picture, 0, pic_width, pic_height, scale, constants.BLACK)
        self.animation = pygame.transform.rotate(self.animation, rotation)

        self.id = randrange(1000000000)

    def get_size(self):
        """Return size of object in grid."""
        return self.size_in_grid

    def get_id(self):
        """Return id of object."""
        return self.id

    def coord_x(self):
        """Return x coordinate of object."""
        return self.location_x

    def coord_y(self):
        """Return y coordinate of object."""
        return self.location_y

    def set_coords(self, x, y):
        """Set coordinates of object."""
        self.location_x = x
        self.location_y = y

    def move(self):
        """Move object. - only present for polymorphism purpose."""
        return [self.location_x, self.location_y]

    def get_hit(self):
        """This function is called when object is hit."""
        return

    def set_showable(self, showable):
        """Set showable attribute of object."""
        self.showable = showable

    @property
    def is_movable(self):
        """Return True if object can be moved on map."""
        return False

    def show_object(self, win, scale_x, scale_y):
        """Show object on the screen."""
        if not self.showable:
            return

        image_rec = self.animation.get_rect(center=(self.location_x * scale_x,
                                                    self.location_y * scale_y))
        win.blit(self.animation, image_rec)
        return

    def change_showable(self, showable):
        """Change showable attribute of object."""
        self.showable = showable

    def passable(self):
        """Return True if object can be moved through."""
        return False
