from hlt import *
from networking import *


LIMIT_TO_MOVE = 30
LIMIT_TO_FUSE = LIMIT_TO_MOVE / 2 + 1
MAX_SIZE = 255

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
            if  enemy_strength < my_strength:
                enemy_production = game_map.getSite(current_location, neighbor).production
                if best_enemy_production < enemy_production:
                    attack_direction = neighbor
                    best_enemy_production = enemy_production

    return attack_direction


def could_fuse(my_strength, my_friend_strength):
    if my_strength + my_friend_strength > MAX_SIZE:
        return False
    return True


def move_now():
    move_direction = STILL
    best_production = 0

    if my_strength < LIMIT_TO_MOVE:
        return STILL

    # for neighbor in CARDINALS:
    #     if game_map.getSite(current_location, neighbor).owner != myID:
    #         if best_production < game_map.getSite(current_location, neighbor).production:
    #             best_production = game_map.getSite(current_location, neighbor).production
    #             move_direction = neighbor

    for neighbor in CARDINALS:
        if could_fuse(my_strength, game_map.getSite(current_location, neighbor).strength) \
                and last_move[current_location.x, current_location.y] != inverse_neighbor(neighbor):
            move_direction = neighbor
            break

    return move_direction

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
                # else:
                    # fuse_with_friend_direction = fuse_with_friend()
                    # if fuse_with_friend_direction != STILL:
                    #     moves.append(Move(current_location, fuse_with_friend_direction))
                    #     move = True
                if not move:
                    move = Move(current_location, move_now())

                if move != None:
                    last_move[x,y] = move.direction
                    moves.append(move)
    sendFrame(moves)