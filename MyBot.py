from hlt import *
from networking import *


LIMIT_TO_MOVE = 30
LIMIT_TO_FUSE = LIMIT_TO_MOVE / 2 + 1
LIMIT_TO_BORDER = 125
MAX_SIZE = 255
MAX_DEPTH = 20

myID, game_map = getInit()
sendInit("ElsaBot")

last_move = {}


def inverse_neighbor(neighbor):
    if neighbor == NORTH:
        return SOUTH
    elif neighbor == SOUTH:
        return NORTH
    elif neighbor == EAST:
        return WEST
    elif neighbor == WEST:
        return EAST


def attack_enemy():
    attack_direction = STILL
    best_enemy_production = 0
    for neighbor in CARDINALS:
        if game_map.getSite(current_location, neighbor).owner != myID:
            enemy_strength = game_map.getSite(current_location, neighbor).strength
            if enemy_strength < my_strength:
                enemy_production = game_map.getSite(current_location, neighbor).production
                if best_enemy_production < enemy_production:
                    attack_direction = neighbor
                    best_enemy_production = enemy_production

    return attack_direction


def could_fuse(my_strength, my_friend_strength):
    if my_strength + my_friend_strength > MAX_SIZE:
        return False
    return True


def get_direction_by_angle(l1, l2):
    dx = l2.x - l1.x
    dy = l2.y - l1.y

    if dx > game_map.width - dx:
        dx -= game_map.width
    elif -dx > game_map.width + dx:
        dx += game_map.width

    if dy > game_map.height - dy:
        dy -= game_map.height
    elif -dy > game_map.height + dy:
        dy += game_map.height

    if (math.fabs(dy) > math.fabs(x)):
        if dy > 0:
            return NORTH
        else:
            return SOUTH
    else:
        if dx > 0:
            return EAST
        else:
            return WEST


def move_to_border(my_y, my_x):
    shortest_distance = game_map.width
    my_location = Location(my_x, my_y)
    go_to = Location(0,0)
    for y_temp in range(my_y - MAX_DEPTH, my_y + MAX_DEPTH):
        for x_temp in range(my_x - MAX_DEPTH, my_x + MAX_DEPTH):
            explore_location = Location(x_temp, y_temp)
            if game_map.inBounds(explore_location):
                if game_map.getDistance(my_location, explore_location) < shortest_distance:
                    shortest_distance = game_map.getDistance(my_location, explore_location)
                    go_to = explore_location

    return get_direction_by_angle(my_location, go_to)


def move_to_fuse():
    for neighbor in CARDINALS:
        if game_map.getSite(current_location).owner == myID:
            if could_fuse(my_strength, game_map.getSite(current_location, neighbor).strength):
                return neighbor


def move_now():
    if my_strength < LIMIT_TO_MOVE:
        return STILL

    if my_strength > LIMIT_TO_BORDER:
        return move_to_border(y, x)

    return move_to_fuse()


while True:
    moves = []
    game_map = getFrame()
    for y in range(game_map.height):
        for x in range(game_map.width):
            last_move[x,y] = STILL

    for y in range(game_map.height):
        for x in range(game_map.width):
            current_location = Location(x, y)
            if game_map.getSite(current_location).owner == myID:
                my_strength = game_map.getSite(current_location).strength
                move = None
                attack_enemy_direction = attack_enemy()
                if attack_enemy_direction != STILL:
                    move = Move(current_location, attack_enemy_direction)
                if not move:
                    move = Move(current_location, move_now())
                if move != None:
                    last_move[x,y] = move.direction
                    moves.append(move)
    sendFrame(moves)