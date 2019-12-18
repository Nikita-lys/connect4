"""
Лысенко Н. С. 4.8

Интеллектуальные системы.
Игра 4 в ряд.
"""

import numpy as np
import random
import math


ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def build_board(rows=ROW_COUNT, columns=COLUMN_COUNT) -> np.array:
    """
    Create empty board on start of the game.

    :param rows: count of rows in game
    :param columns: count of columns in game
    :return:
    """
    ROW_COUNT = rows
    COLUMN_COUNT = columns
    board = []
    for i in range(ROW_COUNT):
        row = []
        board.append(row)
        for j in range(COLUMN_COUNT):
            board[i].append(0)
    return np.array(board)


def visualisation_board(board: np.array) -> None:
    """
    Using on each step to visualise board.

    :param board: list of lists
    :return: nice board
    """
    board = np.array(board)[::-1, :]

    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            print('|', end='')
            if board[i][j] != 0:
                if board[i][j] == 1:
                    print('x', end='')
                elif board[i][j] == 2:
                    print('0', end='')
                else:
                    print('+', end='')
            else:
                print(' ', end='')
        print('|', end='\n')
    print(' 0 1 2 3 4 5 6')


def check_win(board: np.array, who: int) -> (bool, list):
    """
    Is win position on the board?

    :param board: list of lists
    :param who: who are playing now
    :return: True and list of winning positions IF win
             ELSE False and None
    """
    # horizontally
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT - 3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] and board[i][j] == who:
                return True, [(i, j), (i, j+1), (i, j+2), (i, j+3)]    # i, j -- j+3

    # vertically
    for i in range(ROW_COUNT - 3):
        for j in range(COLUMN_COUNT):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] and board[i][j] == who:
                return True, [(i, j), (i+1, j), (i+2, j), (i+3, j)]     # i -- i+3, j

    # diagonal \
    for i in range(ROW_COUNT - 3):
        for j in range(COLUMN_COUNT - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] and board[i][j] == who:
                return True, [(i, j), (i+1, j+1), (i+2, j+2), (i+3, j+3)]   # i -- i+3, j -- j+3

    # diagonal /
    for i in range(ROW_COUNT - 3):
        for j in range(COLUMN_COUNT - 4, COLUMN_COUNT):
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] and board[i][j] == who:
                return True, [(i, j), (i+1, j-1), (i+2, j-2), (i+3, j-3)]  # i -- i+3, j -- j+3

    return False, None


def visualisation_win_move(board: np.array, where_won: list) -> np.array:
    """
    To visualise win position on the board.

    :param board: lists of list
    :param where_won: list of winning positions
    :return: new board
    """
    for point in where_won:
        board[point[0]][point[1]] = 8
    return np.array(board)


def evaluate_four(four: list, who: int) -> int:
    """
    how much four array

    :param four: array of 4 elements
    :param who: who are playing now
    :return: score
    """
    score = 0

    opponent = PLAYER_PIECE if who != PLAYER_PIECE else AI_PIECE

    if four.count(who) == 4:
        score += 100
    elif four.count(who) == 3 and four.count(EMPTY) == 1:
        score += 5
    elif four.count(who) == 2 and four.count(EMPTY) == 2:
        score += 2

    if four.count(opponent) == 3 and four.count(EMPTY) == 1:
        score -= 4

    return score


def heuristic(board: np.array, who: int) -> int:
    """
    Calculate heuristic

    :param board: list of lists
    :param who: who are playing now
    :return: score
    """
    score = 0

    # score in center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(who)
    score += center_count * 3

    #   Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):   # [0 ... 4)
            four = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_four(four, who)

    #   Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            four = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_four(four, who)

    #   Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            four = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_four(four, who)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            four = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_four(four, who)

    return score


def lets_move(board: np.array, col: int, who: int, used_cols=[False] * 7) -> (np.array or None, bool):
    """
    Pick new move.
    If moves are out, return None.

    :param board: our play board
    :param col: number of column to pick move
    :param turn: who plays now
    :param used_cols: list of used columns
    :return: new board or None
    """
    used_cols[col] = True
    for i in range(ROW_COUNT - 1, -1, -1):
        if board[i][col] == 0:
            board[i][col] = who
            return np.array(board), False
        elif i == 0:
            if False in used_cols:
                col = int(input('Choose another move: '))
                lets_move(board=board, col=col, who=who)
            else:
                print("You are out of moves.")
            return None, True     # end of game
    return np.array(board), False


def is_terminal_board(board: np.array) -> bool:
    """
    Is final situation?

    :param board: list of lists
    :return: True if final or False
    """
    return check_win(board, PLAYER_PIECE)[0] or check_win(board, AI_PIECE)[0] or len(get_valid_locations(board)) == 0


def drop_piece(board: np.array, row: int, col: int, who: int) -> np.array:
    """
    Do move

    :param board: list of lists
    :param row: number of row
    :param col: number of column
    :param who: who are playing now
    :return: new board
    """
    board[row][col] = who
    return board


def is_valid_location(board: np.array, col: int) -> bool:
    """
    Look at element in last row in col

    :param board: list of lists
    :param col: number of column
    :return:
    """
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board: np.array, col: int) -> int:
    """
    Find free row for col

    :param board: list of lists
    :param col: number of column
    :return: number of row
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def get_valid_locations(board: np.array) -> list:
    """
    List of numbers of columns where 0 in the last row

    :param board: list of lists
    :return: list of numbers of columns
    """
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def minimax(board: np.array, depth=5, alpha=-math.inf, beta=math.inf, maximizing_player=True) -> (int or None, int):
    """
    MINIMAX algorithm

    :param board: list of lists
    :return: score
    """
    is_terminal = is_terminal_board(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI_PIECE)[0]:
                return None, 100000000000000  # math.inf
            elif check_win(board, PLAYER_PIECE)[0]:
                return None, -10000000000000  # -math.inf
            else:  # game is over, no more valid moves
                return None, 0
        else:  # depth is zero
            return None, heuristic(board, AI_PIECE)

    valid_locations = get_valid_locations(board)
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()

            row = get_next_open_row(board, col)
            b_copy = drop_piece(b_copy, row, col, AI_PIECE)

            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player  AI now
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()

            row = get_next_open_row(board, col)
            b_copy = drop_piece(b_copy, row, col, PLAYER_PIECE)

            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def start() -> None:
    """
    Choose mode of game

    :return: game
    """
    mode = -1231231423
    print('Choose play mode:\n 1 - PvE (first move)\n 2 - PvE (second move)')   # \n 3 - PvP
    while mode not in [1, 2]:
        try:
            mode = int(input('Your mode: '))
        except True:
            pass
        game(mode)
        break


def game(mode: int) -> None:
    """
    Main function

    :param mode: PvE. You first move or second
    :return: None
    """
    board = build_board()
    visualisation_board(board)

    PLAYER = 0
    AI = 1

    turn = 0
    if mode == 2:
        turn = 1    # ходят 'О' AI
    elif mode == 1:
        turn = 0    # ходят 'Х' PLAYER

    game_over = False

    while not game_over:
        # PLAYER move
        if turn == PLAYER:
            while 2 * 2 == 4:
                try:
                    col = int(input('Choose column [0-6]: '))
                    break
                except ValueError:
                    continue

            row = get_next_open_row(board, col)
            board = drop_piece(board, row, col, PLAYER_PIECE)

            if check_win(board=board, who=PLAYER_PIECE)[0]:
                print("You are wins!")
                game_over = True

            turn += 1
            turn = turn % 2
            visualisation_board(board)

        # AI move
        elif turn == AI and not game_over:
            col, minimax_score = minimax(board)

            row = get_next_open_row(board, col)
            board = drop_piece(board, row, col, AI_PIECE)

            if check_win(board=board, who=AI_PIECE)[0]:
                print("\n====================\n"
                      "=======AI won=======\n"
                      "====================")
                visualisation_win_move(board=board, where_won=check_win(board=board, who=AI_PIECE)[1])
                game_over = True
            turn += 1
            turn = turn % 2
            visualisation_board(board)

        else:
            print('Nobody won')
            break


if __name__ == '__main__':
    start()
