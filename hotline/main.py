"""This is the main file of the game.
It contains the main function, which starts main menu of the game."""
# was not able to fix those errors
# pylint: disable=E1101,C0413

import pygame
import constants

# not In pep8 format, but I tried to fix this with (if __name__ == "__main__":)
# and didn't make it work
pygame.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

from button import Button
from level import level
from initialize_level_1 import initialize_level_1
from initialize_level_2 import initialize_level_2
from initialize_level_3 import initialize_level_3
from result_screen import result_screen
from result_screen import get_font


def main():
    """This function starts the main menu of the game."""
    pygame.display.set_caption("hotline BRNO")
    while True:
        win.fill("black")

        scr = pygame.display.Info()
        width = int(scr.current_w / 2)

        level_1_button = Button(image=pygame.image.load(constants.BUTTON_RECT),
                                pos=(width, 250),
                                text_input="level 1",
                                font=get_font(75),
                                base_color=constants.BUTTON_BASE_COLOR)

        level_2_button = Button(image=pygame.image.load(constants.BUTTON_RECT),
                                pos=(width, 400),
                                text_input="level 2",
                                font=get_font(75),
                                base_color=constants.BUTTON_BASE_COLOR)

        level_3_button = Button(image=pygame.image.load(constants.BUTTON_RECT),
                                pos=(width, 550),
                                text_input="level 3",
                                font=get_font(75),
                                base_color=constants.BUTTON_BASE_COLOR)

        quit_button = Button(image=pygame.image.load(constants.BUTTON_RECT),
                             pos=(width, 700),
                             text_input="quit",
                             font=get_font(75),
                             base_color=constants.BUTTON_BASE_COLOR)

        for button in [level_1_button, level_2_button, level_3_button, quit_button]:
            button.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_1_button.check_for_input(pygame.mouse.get_pos()):
                    if result_screen(win, level(win, initialize_level_1)) == -1:
                        print("quit1")
                        pygame.quit()
                        return
                elif level_2_button.check_for_input(pygame.mouse.get_pos()):
                    if result_screen(win, level(win, initialize_level_2)) == -1:
                        print("quit2")
                        pygame.quit()
                        return
                elif level_3_button.check_for_input(pygame.mouse.get_pos()):
                    if result_screen(win, level(win, initialize_level_3)) == -1:
                        print("quit3")
                        pygame.quit()
                        return
                elif quit_button.check_for_input(pygame.mouse.get_pos()):
                    print("quit4")
                    pygame.quit()
                    return

        pygame.display.update()


# error captures if assets aren't in the right place and all possible game crashes
# which weren't found during testing
# pylint: disable=W0718
if __name__ == "__main__":
    try:
        main()
        print("exiting game")
    except Exception as e:
        print("unexpected error occurred")
        print(e)
        pygame.quit()
        raise e
