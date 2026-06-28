"""This module handles non player characters."""

from random import randrange
import pygame
from player_soldier import PlayerSoldier
import constants

from shot_flash import CShotFlash


# pylint: disable=too-many-instance-attributes, too-many-arguments
# attributes and arguments are fine
class PlayerNPC(PlayerSoldier):
    """Class that represents every non-player soldier."""
    horizontal_random = randrange(3)
    vertical_random = randrange(3)

    def __init__(self, posx, posy, path, dead_path):
        super().__init__(posx, posy, path, dead_path)
        self.look = [0, 0]
        self.npc_last_move = pygame.time.get_ticks()
        self.time_spotted = None
        self.fired = False
        self.able_to_fire = False
        self.burst_length = 0

    def move_npc(self) -> tuple:
        """This function moves non-player character."""
        current = pygame.time.get_ticks()
        if current - self.npc_last_move > constants.SOLDIER_NPC_MOVE_FREQUENCY:
            self.horizontal_random = randrange(3)
            self.vertical_random = randrange(3)
            self.npc_last_move = current

        looking = [self.location_x, self.location_y]

        if self.horizontal_random == 0:
            self.location_y -= constants.SOLDIER_NPC_SPEED
            if not self.able_to_fire:
                looking[1] = 0
        elif self.horizontal_random == 1:
            self.location_y += constants.SOLDIER_NPC_SPEED
            if not self.able_to_fire:
                looking[1] = 50000

        if self.vertical_random == 0:
            self.location_x -= constants.SOLDIER_NPC_SPEED
            if not self.able_to_fire:
                looking[0] = 0
        elif self.vertical_random == 1:
            self.location_x += constants.SOLDIER_NPC_SPEED
            if not self.able_to_fire:
                looking[0] = 50000

        return tuple(looking)

    def fire_soldier(self, x_scale, y_scale, player_x, player_y, able_to_fire=False):
        """This function makes this soldier fire a bullet."""
        if self.alive is False:
            return None

        if self.burst_length >= constants.SOLDIER_BURST_LENGTH:
            self.burst_length = 0
            self.able_to_fire = False
            return None

        if able_to_fire is False:
            self.able_to_fire = False
            return None

        if able_to_fire is True:
            if self.able_to_fire is False:
                self.time_spotted = pygame.time.get_ticks()
                self.able_to_fire = True
                return None

            delay = pygame.time.get_ticks() - self.time_spotted
            if delay < constants.SOLDIER_NPC_FIRE_DELAY:
                return None

        self.look = [player_x, player_y]
        self.burst_length += 1
        return CShotFlash(self.location_x,
                          self.location_y,
                          player_x,
                          player_y,
                          x_scale,
                          y_scale)

    def move(self):
        if self.alive and self.able_to_fire is False:
            self.look = self.move_npc()
        elif self.alive and self.able_to_fire is True:
            self.move_npc()
        return [self.location_x, self.location_y]

    def where_to_look(self):
        """This function returns coordinates that represent direction of looking."""
        return self.look

    def set_look(self, x, y):
        """This function sets coordinates that represent direction of looking."""
        self.look = [x, y]
