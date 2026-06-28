"""This module runs game loop for each level."""
# pylint is not able to find pygame functions
# pylint: disable=no-member

import pygame
from game_map import GameMap


def level(win, init_function):
    """This function runs game loop for each level."""
    win.fill("black")
    scr = pygame.display.Info()
    game_map = GameMap(scr.current_h, scr.current_w)

    configuration = init_function()
    objects = configuration[0]
    if len(objects) == 0:
        return -2
    for obj in objects:
        game_map.add_object(obj)

    game_map.set_player_id(objects[0].get_id())

    run = True
    while run:
        pygame.time.delay(10)
        win.blit(configuration[1], (0, 0))

        game_map.resolve_round(win)

        if pygame.mouse.get_pressed(num_buttons=3)[0] is True:
            tmp = objects[0].fire_soldier(game_map.scale_x, game_map.scale_y, 0, 0)
            if tmp is not None:
                game_map.add_object(tmp)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -2

        pygame.display.update()
        tmp = game_map.game_state()
        if tmp in (-1,  1):
            return tmp

    return -2
