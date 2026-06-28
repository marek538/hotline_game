"""This module handles when player either wins or loses the game."""

# pylint: disable=no-member
# pygame functions are not recognized by pylint

import pygame

import constants
from button import Button


def get_font(size):
    """Return font with size."""
    return pygame.font.Font(constants.BUTTON_FONT, size)


def result_screen(win, result):
    """This function handles when player either wins or loses the game."""
    if result == -2:
        return -1

    scr = pygame.display.Info()
    width = int(scr.current_w / 2)

    victory_button = Button(image=pygame.image.load(constants.BUTTON_RECT),
                            pos=(width, 700),
                            text_input="victory",
                            font=get_font(75),
                            base_color=constants.BUTTON_BASE_COLOR)

    defeat_button = Button(image=pygame.image.load(constants.BUTTON_RECT),
                           pos=(width, 700),
                           text_input="defeat",
                           font=get_font(75),
                           base_color=constants.BUTTON_BASE_COLOR)

    if result == 1:
        victory_button.update(win)
    else:
        defeat_button.update(win)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
