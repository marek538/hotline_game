"""This module handles movement on the game map
 and game map representation itself."""
import constants
from shot_flash import CShotFlash
from soldier_npc import PlayerNPC


def in_grid(coord):
    """Return True if coord is in the grid, False otherwise."""
    num1, num2 = coord
    # Check if both numbers are greater than or equal to zero and less than map_size
    return 0 <= num1 < constants.MAP_SIZE and 0 <= num2 < constants.MAP_SIZE


def find_object_by_id(moving_objects, id_obj):
    """Return object with id id_obj from moving_objects list."""
    for obj in moving_objects:
        if obj.get_id() == id_obj:
            return obj
    return None


class GameMap:
    """Class that represents game map and handles movement on it."""
    scale_x: float
    scale_y: float

    moving_objects = []

    def __init__(self, height, length):
        self.moving_objects = []
        self.scale_x = length / constants.MAP_SIZE
        self.scale_y = height / constants.MAP_SIZE
        self.map_grid = [[[] for _ in range(constants.MAP_SIZE)] for _ in range(constants.MAP_SIZE)]
        self.player_id = 0

    def add_object(self, element, is_in_movable=False):
        """Add object to the game map."""
        if element is None:
            return

        size_side = int(element.get_size() / 2)

        for i in range(-size_side, size_side + 1, 1):
            for j in range(-size_side, size_side + 1, 1):
                if in_grid((element.coord_x() + i, element.coord_y() + j)):
                    self.map_grid[element.coord_x() + i][element.coord_y() + j].append(element)

        if in_grid((element.coord_x(), element.coord_y())):
            self.map_grid[element.coord_x()][element.coord_y()][-1].change_showable(True)
            if element.is_movable and not is_in_movable:
                self.moving_objects.append(element)

    def resolve_out_of_grid(self, obj, prev_coord):
        """Resolve situation when object is moved out of the grid."""
        if isinstance(obj, CShotFlash):
            self.moving_objects.remove(obj)
            self.remove_object(prev_coord[0], prev_coord[1], obj.get_id(), obj.get_size())
        else:
            obj.set_coord(prev_coord[0], prev_coord[1])

    def resolve_collision(self, obj, prev_coord, new_coord):
        """Resolve situation when object is moved to occupied space."""
        if isinstance(obj, CShotFlash):
            for element in self.map_grid[new_coord[0]][new_coord[1]]:
                element.get_hit()

            self.moving_objects.remove(find_object_by_id(self.moving_objects, obj.get_id()))
            self.remove_object(prev_coord[0], prev_coord[1], obj.get_id(), obj.get_size())
        else:
            obj.set_coord(prev_coord[0], prev_coord[1])

    def move_object(self, obj, prev_coord):
        """Move object to new coord and remove it from last coord."""
        self.remove_object(prev_coord[0], prev_coord[1], obj.get_id(), obj.get_size())

        self.add_object(obj, is_in_movable=True)

    def move_all_objects(self):
        """Move all objects movable on the game map."""
        for obj in reversed(self.moving_objects):
            prev_coord = [obj.coord_x(), obj.coord_y()]
            new_coord = obj.move()

            # object actually moved
            if new_coord != prev_coord:
                # getting out of grid
                if not in_grid(new_coord):
                    self.resolve_out_of_grid(obj, prev_coord)
                    continue

                # [-1, -1] if space is not occupied - else [x, y]
                tmp = self.check_collision(new_coord, prev_coord, obj.get_id(), obj.get_size())

                if tmp != [-1, -1]:
                    self.resolve_collision(obj, prev_coord, tmp)

                # move character to new coord and remove it from last coord
                else:
                    self.move_object(obj, prev_coord)

            if isinstance(obj, PlayerNPC):
                if self.able_to_fire(obj.coord_x(),
                                     obj.coord_y(),
                                     self.moving_objects[0].coord_x(),
                                     self.moving_objects[0].coord_y(),
                                     obj.get_id()):
                    obj.set_look(self.moving_objects[0].coord_x(), self.moving_objects[0].coord_y())
                    self.add_object(obj.fire_soldier(x_scale=self.scale_x,
                                                     y_scale=self.scale_y,
                                                     player_x=self.moving_objects[0].coord_x(),
                                                     player_y=self.moving_objects[0].coord_y(),
                                                     able_to_fire=True))
                else:
                    obj.able_to_fire = False

    def resolve_round(self, win):
        """Resolve one cycle of the game."""
        self.move_all_objects()

        # show objects - might be better to print only moving objects
        # pylint: disable=C0200
        # seems less readable with enumerate
        for i in range(len(self.map_grid)):
            for j in range(len(self.map_grid[i])):
                for element in self.map_grid[i][j]:
                    element.show_object(win, scale_x=self.scale_x, scale_y=self.scale_y)

    def count_increment(self, x_diff, y_diff):
        """Return [x, y] which is increment of movement."""
        if x_diff == 0:
            tmp_x = 0
        else:
            if abs(x_diff) > abs(y_diff):
                tmp_x = x_diff / abs(x_diff)
            else:
                tmp_x = x_diff / abs(y_diff)
        if y_diff == 0:
            tmp_y = 0
        else:
            if abs(y_diff) > abs(x_diff):
                tmp_y = y_diff / abs(y_diff)
            else:
                tmp_y = y_diff / abs(x_diff)

        return [tmp_x, tmp_y]

    def check_collision(self, new_coordinates, coordinates_old, id_obj: int, obj_size: int):
        """Return [-1, -1] if space is not occupied - else [x, y] which is fist collision."""
        x_diff = new_coordinates[0] - coordinates_old[0]
        y_diff = new_coordinates[1] - coordinates_old[1]

        obj_size = int(obj_size / 2)

        tmp = self.count_increment(x_diff, y_diff)
        tmp_x = tmp[0]
        tmp_y = tmp[1]

        for i in range(1, max(abs(x_diff), abs(y_diff)) + 1):

            if len(self.map_grid[coordinates_old[0] + int(i * tmp_x)]
                   [coordinates_old[1] + int(i * tmp_y)]) != 0:
                for obj in self.map_grid[coordinates_old[0]
                                         + int(i * tmp_x)][coordinates_old[1]
                                                           + int(i * tmp_y)]:
                    if obj.get_id() != id_obj and not obj.passable():
                        return [coordinates_old[0] + int(i * tmp_x),
                                coordinates_old[1] + int(i * tmp_y)]

        for x in range(-obj_size, obj_size + 1, 1):
            for y in range(-obj_size, obj_size + 1, 1):
                if not in_grid((new_coordinates[0] + x, new_coordinates[1] + y)):
                    continue
                if len(self.map_grid[new_coordinates[0] + x][new_coordinates[1] + y]) != 0:
                    for obj in self.map_grid[new_coordinates[0] + x][new_coordinates[1] + y]:
                        if obj.get_id() != id_obj and not obj.passable():
                            return [new_coordinates[0] + x, new_coordinates[1] + y]

        return [-1, -1]

    # pylint: disable=R0913
    # arguments are fine here
    def able_to_fire(self, first_x: int,
                     first_y: int,
                     second_x: int,
                     second_y: int,
                     id_obj: int,
                     obj_size=1):
        """Return True if object with id id_obj can fire
        from [first_x, first_y] to [second_x, second_y]."""
        tmp = self.check_collision([second_x, second_y], [first_x, first_y], id_obj, obj_size)
        if (self.map_grid[tmp[0]][tmp[1]] != []
                and self.map_grid[tmp[0]][tmp[1]][0].get_id() == self.player_id):
            return True

        return False

    def set_player_id(self, id_obj: int):
        """Set player id."""
        self.player_id = id_obj

    def remove_object(self, x_coord, y_coord, id_obj: int, size_side):
        """Remove object from the game map."""
        size_side = int(size_side / 2)
        for i in range(-size_side, size_side + 1, 1):
            for j in range(-size_side, size_side + 1, 1):
                if in_grid((x_coord + i, y_coord + j)):
                    for obj in self.map_grid[x_coord + i][y_coord + j]:
                        if obj.get_id() == id_obj:
                            self.map_grid[x_coord + i][y_coord + j].remove(obj)

    def game_state(self):
        """Return -1 if player lost, 1 if player won, 0 otherwise."""
        if self.moving_objects[0].alive is False:
            return -1

        enemy_alive = False
        for obj in self.moving_objects:
            if isinstance(obj, PlayerNPC) and obj.alive:
                enemy_alive = True
                break

        if enemy_alive is False:
            return 1
        return 0
