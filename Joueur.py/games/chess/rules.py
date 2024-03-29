#######################################################################
# Name: Hannah Reinbolt
# Date: 4-12-2020
# Class: 5400-101 - Intro to AI
# Assignment: Game Assignment #2 - Iterative Deepening Depth Limited Minimax AI
# Note: This file defines all rules for pieces.
######################################################################

# libraries
from games.chess.game_logic import *
import copy
import random


#########################################################################################
# CHECK MOVES
#########################################################################################

# check moves for collision, and valid moves.
# takes: board (list of lists), current position (list of int), color (str), history (dict of lists), 
#        generated moves (list of lists), and no hop,will/will not hop over other friends (bool)
# returns: list
def check_moves(board, curr_pos, color, history, gen_move, nohop):
    # variables
    flag = True
    computed = False
    curr_uci = coor_to_uci(curr_pos[0], curr_pos[1])

    if len(gen_move) != 0:
        pos = gen_move
        y = pos[0]
        x = pos[1]

        # check if y position is out if bounds
        if y < 0 or y > len(board)-1:
            flag = False

        # check if x position is out of bounds
        elif x < 0 or x > len(board[1])-1:
            flag = False

        # only continue if coords are in boundaries of board
        if flag: 
            new_uci = coor_to_uci(y, x)

            # check to see if the position was already computed
            if curr_uci in history:
                if history[curr_uci] != []:
                    for item in history[curr_uci]:
                        if item[0:2] == new_uci:
                            computed = True
                            break
            # pass if already computed
            if computed:
                return []

            # check if there is a peice on this spot
            elif board[y][x] is not "0":

                # if new position has a white peice
                if board[y][x][0].isupper():

                    # uppercase is white, check current peice color, if non hop then stop
                    if color == "white" and nohop == True:
                        return []

                    # if not friendly then take piece
                    elif color != "white":
                        return [new_uci, board[y][x]]

                # if new position has a black piece
                else:
                    # if friendly peice and not hopping, then stop here
                    if color == "black" and nohop == True:
                        return []

                    # not friendly then take piece
                    if color != "black":
                        return [new_uci, board[y][x]]

            # if the spot is empty, this can be a move
            else:
                return [new_uci, ""]

        # reset flags
        flag = True
        computed = False

    # if it went through all that, and no new moves, then return [], meaning no valid moves
    return []


##########################################################################
# KNIGHTS
#########################################################################

# generate all knight moves
# takes: current position (list of int)
# returns: list of lists
def move_knight(curr_pos):
    # variables
    y = curr_pos[0]
    x = curr_pos[1]
    all_pos = [[y-2, x-1], [y-2, x+1], [y-1, x-2], [y-1, x+2], [y+1, x-2], [y+1, x+2], [y+2, x-1], [y+2, x+1]]
    final_lst = []

    # check all directions
    for item in all_pos:

        # check y direction y is in range of board
        if item[0] >= 0 and item[0] <= 7:
            # check x direction is in range of board
            if item[1] >= 0 and item[1] <= 7:

                # add item to final list if in bounds
                final_lst.append(item)

    return final_lst


# find all valid knight moves of one color
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def findall_knight_moves(board, color):
    # variables
    history = {} # dictionary of past moves, this will decrease search time
    choice = ""
    
    # define choice
    if color == "black":
        choice = "n"
    else:
        choice = "N"

    # find all knight moves
    for height in range(0, len(board)):
        for width in range(0, len(board[height])):
            
            # if a rook is found
            if board[height][width] == choice:

                # generate all knight moves
                gen_lst = move_knight([height, width])

                # make sure there were moves returned
                if gen_lst != []:

                    for item in gen_lst:

                        # check each move
                        move = check_moves(board, [height, width], color, history, item, False)
                        curr_pos = coor_to_uci(height, width)

                        # check if there are no move moves possible
                        if move == []:
                            continue

                        # make sure key is added to history even as a blank
                        elif curr_pos not in history:
                            history[curr_pos] = []

                        # add to history
                        history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]

    # return all knight moves in list
    return history


#######################################################################################
# BISHOPS
#######################################################################################


# generate all bishop moves
# takes: current position (list of ints)
# returns: list of lists
def move_bishop(curr_pos):
    # variables
    height = curr_pos[0]
    width = curr_pos[1]
    count = 0
    final_lst = [[], [], [], []]
    all_pos = [
            zip(range(height+1, 8), range(width-1, -1, -1)),
            zip(range(height+1, 8), range(width+1, 8)), 
            zip(range(height-1, -1, -1), range(width-1, -1, -1)),
            zip(range(height-1, -1, -1), range(width+1, 8))
              ] # generate all diagonal moves

    # make sure they are all in bounds
    for direction in all_pos:
        for pos in direction:

            # check if y is in bounds of board
            if pos[0] >= 0 and pos[0] <= 7:
                # check if x is in bounds of board
                if pos[1] >= 0 and pos[1] <= 7:
                    
                    # add to list of valid moves
                    final_lst[count].append(pos)

        # add to count
        count = count + 1

    # return all generated moves
    return final_lst


# find all valid bishop moves of one color
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def findall_bishop_moves(board, color):
    # variables
    history = {}
    choice = ""

    # define choice
    if color == "black":
        choice = "b"
    else:
        choice = "B"

    # find all bishop moves
    for height in range(0, len(board)):
        for width in range(0, len(board[height])):

            # check choice
            if board[height][width] == choice:
                
                # generate all diagonal moves
                gen_lst = move_bishop([height, width])

                # iterate through all four diagonal directions
                for direction in gen_lst:

                    # only continue if that direction is not empty
                    if direction != []:

                        # check until end
                        for position in direction:
                            # find move but don't jump over peices
                            move = check_moves(board, [height, width], color, history, position, True)
                            curr_pos = coor_to_uci(height, width)

                            # check if there are not more moves possible
                            if move == []:
                                break

                            # check to make sure item is in history
                            if curr_pos not in history:
                                history[curr_pos] = []

                            # if taken a piece, record and break
                            if move[1] != '':
                                history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]
                                break

                            # if not blank then add to current moves
                            history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]

    # return all bishop moves
    return history


#######################################################################################
# ROOKS
#######################################################################################

# generate all valid castle moves
# takes: current position (list of ints)
# returns: list of lists
def move_castle(curr_pos):
    # variables
    y = curr_pos[0]
    x = curr_pos[1]
    count = 0
    final_lst = [[], [], [], []]

    # make single list as long as the range list
    # first direction
    x1 = range(x-1, -1, -1)
    y1 = []
    for i in x1:
        y1.append(y)

    # second direction
    x2 = range(x+1, 8)
    y2 = []
    for i in x2:
        y2.append(y)

    # third direction
    y3 = range(y-1, -1, -1)
    x3 = []
    for i in y3:
        x3.append(x)

    # fourth direction
    y4 = range(y+1, 8)
    x4 = []
    for i in y4:
        x4.append(x)

    all_pos = [
            zip(y1, x1), 
            zip(y2, x2),
            zip(y3, x3),
            zip(y4, x4)
              ] # generate all vertical and horizontal moves

    # get rid of moves not in board range
    for direction in all_pos:
        for pos in direction:

            # check y to be in board range
            if pos[0] >= 0 and pos[0] <= 7:
                # check x to be in board range
                if pos[1] >= 0 and pos[1] <= 7:

                    # add pos to valid moves
                    final_lst[count].append(pos)

        # add to count
        count = count + 1

    # return all generated moves
    return final_lst


# find all valid castle moves for one color
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def findall_castle_moves(board, color):
    # variables
    history = {}
    choice = ""

    # define choice
    if color == "black":
        choice = "r"
    else:
        choice = "R"

    # find all castle moves
    for height in range(0, len(board)):
        for width in range(0, len(board[height])):

            # check choice
            if board[height][width] == choice:
                # generate all vertical and horizontal moves
                gen_lst = move_castle([height, width])

                # itertate through all four diagonal directions
                for direction in gen_lst:

                    # only continue if there are moves in that direction
                    if direction != []:

                        # check until end
                        for position in direction:
                            # find move but don't jump over peices
                            move = check_moves(board, [height, width], color, history, position, True)
                            curr_pos = coor_to_uci(height, width)

                            # check if there are not more moves possible
                            if move == []:
                                break

                            # make sure item is in history
                            if curr_pos not in history:
                                history[curr_pos] = []

                            # if peice taken, break
                            if move[1] != '':
                                history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]
                                break

                            # if not blank then add to current moves
                            history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]

    # return all castle moves
    return history


#######################################################################################
# QUEENS
######################################################################################


# find all valid queen moves of one color
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def findall_queen_moves(board, color):
    # variables
    history = {}
    choice = ""

    # define choice
    if color == "black":
        choice = "q"
    else:
        choice = "Q"

    # find all queen moves
    for height in range(0, len(board)):
        for width in range(0, len(board[height])):

            # check choice
            if board[height][width] == choice:
                # generate all vertical and horizontal moves
                ver_moves = move_castle([height, width])
                # generate all diagonal moves
                dig_moves = move_bishop([height, width])
                # combine lists of moves
                gen_lst = ver_moves + dig_moves

                # iterate through all directions
                for direction in gen_lst:

                    # only move if direction is not empty
                    if direction != []:

                        # check all positions
                        for position in direction:

                            # find move but don't jump over pieces
                            move = check_moves(board, [height, width], color, history, position, True)
                            curr_pos = coor_to_uci(height, width)

                            # check if there are no more moves possible for this direction
                            if move == []:
                                break

                            # make sure current is in history
                            if curr_pos not in history:
                                history[curr_pos] = []

                            # if peice taken then end 
                            if move[1] != '':
                                history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]
                                break

                            # if not blank then add to current moves and continue
                            history[curr_pos] = history[curr_pos] + [curr_pos + move[0]]

    # return all queen moves
    return history


######################################################################################
# PAWNS
######################################################################################


# find enemies for both sides for black and white
# takes: board (list of lists), current position (list of int), left position (list of int),
#        right position (list of int), color (str) and pawn promotion (bool)
# returns: list of str
def find_pawn_enemies(board, curr_pos, l_pos, r_pos, color, promote):
    # variables
    # current position
    y = curr_pos[0]
    x = curr_pos[1]

    # new left position
    l_y = l_pos[0]
    l_x = l_pos[1]

    # new right position
    r_y = r_pos[0]
    r_x = r_pos[1]

    curr_uci = coor_to_uci(y, x)
    history = []
    promotion = promote_pawn(color)

    # check left side for enemies
    # make sure the left side is in bounds
    if l_y >= 0 and l_y <= len(board)-1 and l_x <= len(board[1])-1 and l_x >= 0:

        # check if there is an enemy peice there
        if board[l_y][l_x] != '0':

            # check if that piece is an enemy piece
            isenemy = amienemy(board[l_y][l_x], color)
            new_uci = coor_to_uci(l_y, l_x)

            # check if enemy
            if isenemy == True:
                # check if the pawn needs a promotion as well
                if promote == True:
                    history.append(curr_uci + new_uci + promotion)

                else:
                    history.append(curr_uci + new_uci)

        # check right side for enemies
        # make sure right side is in bounds
        elif r_y >= 0 and r_y <= len(board)-1 and r_x >= 0 and r_x <= len(board[1])-1:

            # check if there is an enemy piece there
            if board[r_y][r_x] != '0':

                # check if that piece is an enemy place
                isenemy = amienemy(board[r_y][r_x], color)
                new_uci = coor_to_uci(r_y, r_x)

                # check if enemy
                if isenemy == True:
                    # check if the pawn needs a promotion as well
                    if promote == True:
                        history.append(curr_uci + new_uci + promotion)

                    else:
                        history.append(curr_uci + new_uci)

    # return history
    return history


# promote pawn to another piece once it has reached the end of the board. 
# There is a random chance it will be a queen, rook, knight or bishop. 
# takes: color (str)
# returns: str
def promote_pawn(color):
    # variables
    black = ['q', 'r', 'b', 'n']
    white = ['Q', 'R', 'B', 'N']
    pieces = []

    # find color
    if color == "black":
        pieces = black
    else:
        pieces = white

    # random choose a promotion
    result = random.choice(pieces)

    # return promotion
    return result


# generate all valid pawn moves of one color
# takes: board (list of lists), current position (list of int) and color (str)
# returns: list of str
def generate_pawn_moves(board, curr_pos, color):
    # variables
    # current position
    y = curr_pos[0]
    x = curr_pos[1]

    # white pawn moves
    # beginning and end of board, up1, up2, left enemy, right enemy 
    white_move = [[1, 6], y+1, y+2, [y+1, x-1], [y+1, x+1]]
    # black moves
    # beginning and end of board, up1, up2, left enemy, right enemy
    black_move = [[6, 1], y-1, y-2, [y-1, x-1], [y-1, x+1]]
    
    # position and result lists
    move = []
    curr_uci = coor_to_uci(y, x)
    new_uci = ""
    history = []

    # chose color, assume same board orientation every game, black top, white bottom
    if color == "black":
        move = white_move
    else:
        move = black_move

    # check if at the end
    if y == move[0][1]:

        # check if spot right above is free
        if board[move[1]][x] == '0':
            new_uci = coor_to_uci(move[1], x)
            promotion = promote_pawn(color)
            history.append(curr_uci + new_uci + promotion)

        # if the spot is not free then pass
        # next check if there are enemies on eigher side
        enemies = find_pawn_enemies(board, curr_pos, move[3], move[4], color, True)
        history = history + enemies

    # check at the beginning
    elif y == move[0][0]:
        # check if right above is free
        if board[move[1]][x] == '0':

            # check if above that is free too
            if board[move[2]][x] == '0':
                new_uci = coor_to_uci(move[2], x)
                history.append(curr_uci + new_uci)

            # add move
            new_uci = coor_to_uci(move[1], x)
            history.append(curr_uci + new_uci)

        # check side enemies
        enemies = find_pawn_enemies(board, curr_pos, move[3], move[4], color, False)
        history = history + enemies

    # check standard move
    else:
        #print("pawn y position: "+str(move[1])+" pawn x position: "+str(x))
        # check if right above is free
        if board[move[1]][x] == '0':
            new_uci = coor_to_uci(move[1], x)
            history.append(curr_uci + new_uci)

        # check side enemies
        enemies = find_pawn_enemies(board, curr_pos, move[3], move[4], color, False)
        history = history + enemies

    # return rinal list of moves
    return history


# find all valid pawn moves for one color
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def findall_pawn_moves(board, color):
    # variables
    history = {} # dictionary of past moves this will decrease search time
    choice = ""

    # define choice
    if color == "black":
        choice = "p"
    else:
        choice = "P"

    # find all pawn moves
    for height in range(0, len(board)):
        for width in range(0, len(board[1])):
            
            # check choice
            if board[height][width] == choice:

                # genreate all moves
                moves = generate_pawn_moves(board, [height, width], color)
                curr_pos = coor_to_uci(height, width)

                # pass if no moves 
                if moves == []:
                    continue

                # make sure item is in history
                if curr_pos not in history:
                    history[curr_pos] = []

                # add to history
                history[curr_pos] = history[curr_pos] + moves

    # return all pawn moves
    return history


###################################################################################
# NONKING AND ENEMY MOVE GENERATION
###################################################################################


# generate all valid non-king moves
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def generate_all_nonking_moves(board, color):
    # variables
    all_moves = {}

    # generate all moves except kings
    knights = findall_knight_moves(board, color)
    bishops = findall_bishop_moves(board, color)
    rooks = findall_castle_moves(board, color)
    queens = findall_queen_moves(board, color)
    pawns = findall_pawn_moves(board, color)

    # add them all together
    for item in [bishops, rooks, pawns, knights, queens]:
        all_moves.update(item)

    # return all moves
    return all_moves


# generate all valid enemy moves (moves of opposite color to the player)
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def generate_all_enemy_moves(board, color):
    # variables
    all_moves = {}
    kings = {}
    enemy_color = ""
    choice = ""

    # set enemy color
    if color == "black":
        enemy_color = "white"
        choice = "K"
    else:
        enemy_color = "black"
        choice = "k"

    # generate moves
    knights = findall_knight_moves(board, enemy_color)
    bishops = findall_bishop_moves(board, enemy_color)
    rooks = findall_castle_moves(board, enemy_color)
    queens = findall_queen_moves(board, enemy_color)
    pawns = findall_pawn_moves(board, enemy_color)

    # find "fake" enemy king moves, more like a boundery
    for height in range(0, len(board)):
        for width in range(0, len(board[1])):

            # if found that king
            if board[height][width] == choice:

                # generate all moves
                king_moves = generate_king_moves([height, width])
                curr_pos = coor_to_uci(height, width)

                # if current position not in history then add it
                if curr_pos not in kings:
                    kings[curr_pos] = []

                # change these coordinates to board moves
                for move in king_moves:
                    new_pos = coor_to_uci(move[0], move[1])
                    kings[curr_pos] = kings[curr_pos] + [curr_pos + new_pos]

    # add all these moves together
    for item in [kings, knights, bishops, rooks, queens, pawns]:
        all_moves.update(item)

    # return moves
    return all_moves


####################################################################################
# KINGS
###################################################################################


# find all moves for a specific piece
# takes: board (list of lists), color (str) and piece (str)
# returns: dictionary of lists
def find_specific_moves(board, color, piece):
    # variables
    moves = {}

    # find knight moves 
    if piece == "n" or piece == "N":
        moves = findall_knight_moves(board, color)

    # find bishop moves
    elif piece == "b" or piece == "B":
        moves = findall_bishop_moves(board, color)

    # find all rook moves
    elif piece == "r" or piece == "R":
        moves = findall_castle_moves(board, color)

    # find all queen moves
    elif piece == "q" or piece == "Q":
        moves = findall_queen_moves(board, color)

    # find all pawn moves
    elif piece == "p" or piece == "P":
        moves = findall_pawn_moves(board, color)

    # return moves
    return moves


# generate all valid king moves
# takes: current position (list of int)
# returns: list of lists
def generate_king_moves(curr_pos):
    # variables
    y = curr_pos[0]
    x = curr_pos[1]
    moves = [[y+1, x-1], [y-1, x], [y-1, x+1], [y, x-1], [y, x+1], [y+1, x-1], [y+1, x], [y+1, x+1]]
    final = []

    # remove anything out of bounds
    for pos in moves:

        # check y vals to be in bounds
        if pos[0] >= 0 and pos[0] <= 7:
            # check if x val is in bounds
            if pos[1] >= 0 and pos[1] <= 7:

                # add item to valid moves
                final.append(pos)

    # return all generated moves
    return final


# check if any current moves will expose the king and put him in check
# takes:
# returns:
def will_moves_put_king_in_check(board, color, king_pos, friend_moves, enemy_moves):
    # variables
    enemy_color = find_enemy_color(color)
    history = {}

    # for each friend piece
    for friend in friend_moves:
        for move in friend_moves[friend]:

            # check to see if this move will put king in check
            # find friend coords
            friend_new_coords = uci_to_coor(move[2:4])
            friend_old_coords = uci_to_coor(move[0:2])
            friend_letter = board[friend_old_coords[0]][friend_old_coords[1]]

            # make fake board and update this move
            fake_board = copy.deepcopy(board)
            fake_board[friend_new_coords[0]][friend_new_coords[1]] = friend_letter
            fake_board[friend_old_coords[0]][friend_old_coords[1]] = "0"

            # generate new moves
            new_enemy_moves = generate_all_enemy_moves(fake_board, enemy_color)

            # do king check
            king_check = is_king_in_check(fake_board, king_pos, new_enemy_moves)

            if king_check[0] == False:
                # add this to good list

                item = move[0:2]
                if item not in history:
                    history[item] = []
                history[item] = history[item] + [move]

    # return good moves
    return history


# check if the king is in check at a current move
# takes: board (list of lists), current position (list of int) and enemy moves (dictionary of lists)
# returns: list [bool, str]
def is_king_in_check(board, curr_pos, enemy_moves):
    # variables
    curr_uci = coor_to_uci(curr_pos[0], curr_pos[1])

    # iterate through all enemy moves to see if this move is in check
    for piece in enemy_moves:
        for move in enemy_moves[piece]:

            # check each move to see if it is possible to reach from enemy pieces
            if curr_uci == move[2:4]:

                # found a move, king is in check at this move
                return [True, move]

    # if no moves are found same, then not in check
    return [False, '']


# find if a friendly peice can take out an enemy peice on the board to protect the king
# takes: board (list of lists), enemy uci (str) and friend moves (dictionary of lists)
# returns: list of str
def asassinate_for_king(board, enemy_uci, friend_moves):
    # variables
    history = []

    # iterate through friend moves to see if any are available to asassinate target
    for piece in friend_moves:
        for move in friend_moves[piece]:

            # check if any peices can take out the enemy
            if move[2:4] == enemy_uci:
                # found one that can take it out
                history.append(move)

    # return if nothing can get there this move
    if len(history) == 0:
        return [False, '']
    else:
        # insert True, to the beginning of the list to test for positive matches
        history.insert(0, True)
        return history


# friendly pieces block an oncoming check for king
# takes: board (list of lists), king position (list of int), color (str), enemy uci (str), 
#        friend moves (dictionary of lists) and enemy moves (dictionary of lists)
# returns: list of str
def block_for_king(board, king_pos, color, enemy_uci, friend_moves, enemy_moves):
    # variables
    enemy_pos = uci_to_coor(enemy_uci)  # enemy coordinate position
    enemy_letter = board[enemy_pos[0]][enemy_pos[1]]  # enemy piece letter
    enemy_moves_lst = enemy_moves[enemy_uci]  # all enemy moves that is putting king in check
    history = []
    enemy_moves_cpy = copy.deepcopy(enemy_moves)

    # find enemy color
    enemy_color = find_enemy_color(color)  # enemy color

    # find all moves from this enemy
    for enemy_move in enemy_moves_lst:

        # see if a friend can move there
        for friend_piece in friend_moves:
            for friend_move in friend_moves[friend_piece]:

                # see if a friend can move in that spot
                if friend_move[2:4] == enemy_move[2:4]:

                    # find friend coords and letter
                    friend_new_coords = uci_to_coor(friend_move[2:4])
                    friend_old_coords = uci_to_coor(friend_move[0:2])
                    friend_letter = board[friend_new_coords[0]][friend_new_coords[1]]

                    # make fake board and add friend to coords
                    fake_board = [i for i in board]
                    fake_board[friend_new_coords[0]][friend_new_coords[1]] = friend_letter
                    fake_board[friend_old_coords[0]][friend_old_coords[1]] = "0"

                    # regenerate that enemy move
                    new_enemy_moves = generate_all_enemy_moves(fake_board, enemy_color)

                    # re-check king and see if this gets him out of check
                    check_king = is_king_in_check(fake_board, king_pos, new_enemy_moves)

                    if check_king[0] == False:
                        # add this move to good moves
                        history.append(friend_move)

    # return sucessful block moves for king
    return history


# make non-check king move
# takes: board (list of lists), current position (list of int), enemy moves (dictionary of lists),
#        and king moves (dictionary of lists)
# returns: 
def make_noncheck_move(board, curr_pos, enemy_moves, king_moves):
    # variables
    history = []

    # iterate through all king moves to find the ones not in check
    for move in king_moves:

        # iterate through all enemy moves and see if the future move is in check
        check_king = is_king_in_check(board, move, enemy_moves)
        if check_king[0] == False:

            # add to valid moves
            history.append(move)

    # return good moves
    return history


# find all valid king moves for one color
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def findall_king_moves(board, color):
    # variables
    history = {}
    save_king_moves = {}
    board_copy = [i for i in board]
    choice = ""
    incheck = False

    # define choice 
    if color == "black":
        choice = "k"
    else:
        choice = "K"

    # find all king moves
    for height in range(0, len(board)):
        for width in range(0, len(board[0])):

            # check choice
            if board[height][width] == choice:
                curr_pos = coor_to_uci(height, width)

                # generate king moves
                king_moves = generate_king_moves([height, width])

                # generate all friendly moves
                friend_moves = generate_all_nonking_moves(board, color)

                # generate all enemy moves
                enemy_moves = generate_all_enemy_moves(board, color)

                # check if king is in check, if true then the saving moves will be the only moves sent
                check_king = is_king_in_check(board, [height, width], enemy_moves)
                #print("check king: "+str(check_king))
                if check_king[0] == True:
                    incheck = True

                    # find an action that gets king out of check
                    # find if anything can take that piece out
                    enemy_uci = check_king[1][0:2]
                    asassins = asassinate_for_king(board, enemy_uci, friend_moves)
                    #print("assassins: "+str(asassins))
                    if asassins[0] == True:

                        # take out piece
                        save_king_moves[asassins[1][0:2]] = asassins[1:]

                    # find if anything can get in the way
                    block_moves = block_for_king(board, [height, width], color, enemy_uci, friend_moves, enemy_moves)
                    #print("blocked: "+str(block_moves))
                    # add these moves
                    for hero in block_moves:
                        h = hero[0:2]
                        if h not in save_king_moves:
                            # add it
                            save_king_moves[h] = []

                        # add the good moves
                        save_king_moves[h] = save_king_moves[h] + [hero]
                    
                    # if the king was in check, these moves have priority, only return these
                    #print("save king moves: "+str(save_king_moves))


                # check each move king makes to make sure it isn't in check
                noncheck_king = make_noncheck_move(board, [height, width], enemy_moves, king_moves)

                # check to make sure it's not empty
                if len(noncheck_king) != 0:

                    # check each move to make sure it is valid
                    for new_move in noncheck_king:
                        checked_move = check_moves(board, [height, width], color, history, new_move, True)

                        # make sure it was valid
                        if checked_move != []:
                            
                            # make sure item is in history
                            curr_pos = coor_to_uci(height, width)
                            if curr_pos not in history:
                                history[curr_pos] = []

                            # add this move
                            history[curr_pos] = history[curr_pos] + [curr_pos + checked_move[0]]

                # return these moes if in check
                if incheck == True:
                    return history

                # make sure generated friend moves will not put king in check
                good_friend_moves = will_moves_put_king_in_check(board, color, [height, width], friend_moves, enemy_moves)

                # if moves are not empty then add them to current history
                if good_friend_moves != {}:

                    # combine
                    history.update(good_friend_moves)

    # return all king moves
    return history


####################################################################################
# ALL MOVE GENERATION
###################################################################################


# generate moves for all pieces
# takes: board (list of lists) and color (str)
# returns: dictionary of lists
def generate_all_moves(board, color):
    # generate all moves
    # the king generates all moves because they had to be generated anyway to make the check
    moves = findall_king_moves(board, color)

    return moves



