import traceback
import random
import sys

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board [i][j] == " ":
                return True
    return False

def is_sq_in_board(board, y, x):
    if (x >= len(board[0])) or (y >= len(board)):
        return False
    if (x < 0) or (y < 0):
        return False
    else:
        return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    x_prefix = x_end - (d_x * length)
    y_prefix = y_end - (d_y * length)

    x_suffix = x_end + d_x
    y_suffix = y_end + d_y

    is_start_open = is_sq_in_board(board, y_prefix, x_prefix) and board[y_prefix][x_prefix] == " "
    is_end_open = is_sq_in_board(board, y_suffix, x_suffix) and board[y_suffix][x_suffix] == " "

    if is_start_open and is_end_open:
        return "OPEN"
    elif is_start_open or is_end_open:
        # print("semiopen of length {}: {} => {}".format(length, (x_prefix, y_prefix), (x_suffix, y_suffix)))
        return "SEMIOPEN"
    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    counter = 0
    open_seq_count = 0
    semi_open_seq_count = 0
    for i in range(len(board)+1):
        current_x = x_start + i * d_x
        current_y = y_start + i * d_y

        # print("checking: {}".format((current_y, current_x)))
        # print("  counter = {}".format(counter))

        if is_sq_in_board(board, current_y, current_x) and board[current_y][current_x] == col:
            counter += 1
        else:
            if counter == length:
                num = is_bounded(board, current_y - d_y, current_x - d_x, length, d_y, d_x)
                if num == "OPEN":
                    open_seq_count +=1
                if num == "SEMIOPEN" :
                    semi_open_seq_count += 1
            counter = 0

    return (open_seq_count, semi_open_seq_count)

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0

    # Check verticals + horizontals
    for i in range(len(board)):
        (vertical_num_open, vertical_num_semi_open) = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += vertical_num_open
        semi_open_seq_count += vertical_num_semi_open

        (horizontal_num_open, horizontal_num_semi_open) = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += horizontal_num_open
        semi_open_seq_count += horizontal_num_semi_open

    # Check diagnols
    for i in range(len(board)):
        # Diagnols from top, going to the left
        (top_to_left_num_open, top_to_left_num_semi_open) = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += top_to_left_num_open
        semi_open_seq_count += top_to_left_num_semi_open

        # print("TL: detect_row(board, col, {}, {}, len, 1, -1) => {}".format(0, i, (top_to_left_num_open, top_to_left_num_semi_open)))

        # Diagnols from top, going to the right
        (top_to_right_num_open, top_to_right_num_semi_open) = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += top_to_right_num_open
        semi_open_seq_count += top_to_right_num_semi_open

        # print("TR: detect_row(board, col, {}, {}, len,  1, 1) => {}".format(0, i, (top_to_right_num_open, top_to_right_num_semi_open)))

        if i > 0:
            # Diagnols from left, going to the right
            (left_num_open, left_num_semi_open) = detect_row(board, col, i, 0, length, 1, 1)
            open_seq_count += left_num_open
            semi_open_seq_count += left_num_semi_open
            # print("L: detect_row(board, col, {}, {}, len, 1, 1) => {}".format(i, 0, (left_num_open, left_num_semi_open)))

            # Diagnols from right, going to the left
            (right_num_open, right_num_semi_open) = detect_row(board, col, i, len(board) - 1, length, 1, -1)
            open_seq_count += right_num_open
            semi_open_seq_count += right_num_semi_open
            # print("R: detect_row(board, col, {}, {}, len, 1, -1) => {}".format(i, len(board) - 1, (right_num_open, right_num_semi_open)))

    return (open_seq_count, semi_open_seq_count)

def search_max(board):
    highest_score = 0
    y = 0
    x = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board [i][j] == " ":
                board[i][j] = "b"
                current_score = score(board)

                if current_score > highest_score:
                    highest_score = current_score
                    y = i
                    x = j
                board[i][j] = " "
    # print("x = {} y = {}".format(x, y))
    # print("highest_score = {}".format(highest_score))
    return (y, x)

    # MAX_SCORE
    # return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    if score(board) == MAX_SCORE:
        return "Black won"
    if score(board) == -MAX_SCORE:
        return "White won"
    for i in range(len(board)):
        for j in range(len(board)):
            if board [i][j] == " ":
                return "Continue playing"
            else:
                return "Draw"


def print_board(board):

    s = "**"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10) + "|"
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "|*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))



def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "b"

        # print("Computer move: (%d, %d)" % (move_y, move_x))
        # board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"

        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x
