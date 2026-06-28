"""This module creates object for player and from here inherits all other NPCs."""
# pylint: disable=no-member
# pygame functions are not recognized by pylint

import math
from random import randrange
import numpy as np
import pygame
from load_image import get_image
from shot_flash import CShotFlash
import constants


# attributes and arguments are fine
# pylint: disable=too-many-instance-attributes, too-many-arguments
class PlayerSoldier:
    """Class that represents every soldier."""
    size_in_grid = constants.SOLDIER_HITBOX
    soldier_frame = 0

    def __init__(self, posx, posy, path, dead_path, showable=False):
        self.showable = showable
        self.alive = True

        self.id = randrange(1000000000)

        # because of assignment, I have to use numpy array somewhere
        # - here it might not be ideal because they are primarily used for numerical calculations
        self.animation_list = np.empty(dtype=pygame.Surface, shape=0)
        self.dead_animation_list = np.empty(dtype=pygame.Surface, shape=0)

        self.location_x = posx
        self.location_y = posy

        self.walking_left = pygame.image.load(path).convert_alpha()
        self.dead = pygame.image.load(dead_path).convert_alpha()

        self.load_animations()
        self.last_update = pygame.time.get_ticks()

    def load_animations(self):
        """This function loads animations from sprite sheet."""
        for x in range(constants.SOLDIER_ANIMATION_STEPS):
            self.animation_list = np.append(self.animation_list,
                                            get_image(self.walking_left,
                                                      x,
                                                      constants.SOLDIER_PIC_WIDTH,
                                                      constants.SOLDIER_PIC_HEIGHT,
                                                      constants.SOLDIER_PIC_SCALE,
                                                      constants.BLACK))

        self.dead_animation_list = np.append(self.dead_animation_list,
                                             get_image(self.dead, 0,
                                                       constants.DEAD_SOLDIER_PIC_WIDTH,
                                                       constants.DEAD_SOLDIER_PIC_HEIGHT,
                                                       constants.DEAD_SOLDIER_PIC_SCALE,
                                                       constants.BLACK))

    def show_object(self, win, scale_x, scale_y):
        """This function is called every frame and shows object on the screen."""
        if not self.showable:
            return False

        if self.alive:
            look = self.where_to_look()

            # when I put not isinstance(self, PlayerSoldier) here, it does not work
            # pylint: disable=unidiomatic-typecheck
            if type(self) != PlayerSoldier:
                tmp = [look[0] * scale_x, look[1] * scale_y]
                look = tmp

            angle = math.degrees(math.atan2(- look[1] + self.location_y * scale_y,
                                            look[0] - self.location_x * scale_x))

            image = (pygame.transform.rotate(self.animation_list[self.soldier_frame], angle)
                     .convert_alpha())
            image_rec = image.get_rect(center=(self.location_x * scale_x,
                                               self.location_y * scale_y))
            win.blit(image, image_rec)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= constants.SOLDIER_ANIMATION_COOLDOWN:
                self.soldier_frame += 1
                self.soldier_frame = self.soldier_frame % constants.SOLDIER_ANIMATION_STEPS
                self.last_update = current_time

        else:
            image_rec = self.dead_animation_list[0].get_rect(center=(self.location_x * scale_x,
                                                                     self.location_y * scale_y))
            win.blit(self.dead_animation_list[0], image_rec)

        return True

    def move_soldier(self, button):
        """This function is called when player wants to move and sets new coordinates of object."""
        if button[pygame.K_a]:
            self.location_x -= constants.SOLDIER_SPEED
        if button[pygame.K_d]:
            self.location_x += constants.SOLDIER_SPEED
        if button[pygame.K_w]:
            self.location_y -= constants.SOLDIER_SPEED
        if button[pygame.K_s]:
            self.location_y += constants.SOLDIER_SPEED

    # pylint: disable=unused-argument
    # arguments kept here due to inheritance
    def fire_soldier(self, x_scale, y_scale, player_x, player_y, able_to_fire=True):
        """This function is called when player wants to fire and returns shot object."""
        if not self.alive:
            return None
        loc = pygame.mouse.get_pos()
        return CShotFlash(self.location_x,
                          self.location_y,
                          loc[0] / x_scale,
                          loc[1] / y_scale,
                          x_scale,
                          y_scale)

    def coord_x(self):
        """This function returns x coordinate of object."""
        return self.location_x

    def coord_y(self):
        """This function returns y coordinate of object."""
        return self.location_y

    def set_coord(self, x, y):
        """This function sets coordinates of object."""
        self.location_x = x
        self.location_y = y

    def where_to_look(self):
        """This returns coordinates that represent direction of looking."""
        return pygame.mouse.get_pos()

    def move(self):
        """This function is called every frame and returns new coordinates of object."""
        if not self.alive:
            return [self.location_x, self.location_y]
        keys = pygame.key.get_pressed()
        self.move_soldier(keys)
        return [self.location_x, self.location_y]

    def is_movable(self):
        """Returns True if object can be moved"""
        return self.alive

    def get_hit(self):
        """This function is called when object is hit by bullet."""
        self.alive = False

    def get_id(self):
        """Returns id of object"""
        return self.id

    def get_size(self):
        """Returns size of object in grid"""
        return self.size_in_grid

    def change_showable(self, showable):
        """Changes showable attribute"""""
        self.showable = showable

    def passable(self):
        """Returns True if movement can be done through this object"""
        return self.alive is False
