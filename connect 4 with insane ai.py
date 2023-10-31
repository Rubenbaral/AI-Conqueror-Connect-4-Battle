import numpy as np

ROWS = 6
COLS = 7

PLAYER_1 = 1
PLAYER_2 = 2

EMPTY = 0
STREAK_LENGTH = 4

def create_board():

    board = np.zeros((ROWS, COLS), dtype=int)
    return board

def display_board(board):

    for row in range(ROWS-1, -1, -1):
        print("|", end="")
        for col in range(COLS):
            if board[row][col] == 0:
                print(" ", end="|")
            elif board[row][col] == 1:
                print("O", end="|")
            else:
                print("X", end="|")
        print()
    print("-----------------")
    print(" 0 1 2 3 4 5 6")


def drop_piece(board, row, col, piece):

    row = ROWS - 1 - row  
    board[row][col] = piece

def drop_piece(board, row, col, piece):

    board[row][col] = piece

def is_valid_location(board, col):

    return board[ROWS-1][col] == EMPTY

def get_next_open_row(board, col):

    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r

def winning_move(board, piece):

    for r in range(ROWS):
        for c in range(COLS - STREAK_LENGTH + 1):
            if np.all(board[r, c:c+STREAK_LENGTH] == piece):
                return True

    for r in range(ROWS - STREAK_LENGTH + 1):
        for c in range(COLS):
            if np.all(board[r:r+STREAK_LENGTH, c] == piece):
                return True

    for r in range(ROWS - STREAK_LENGTH + 1):
        for c in range(COLS - STREAK_LENGTH + 1):
            if np.all([board[r+i, c+i] == piece for i in range(STREAK_LENGTH)]):
                return True

    for r in range(STREAK_LENGTH - 1, ROWS):
        for c in range(COLS - STREAK_LENGTH + 1):
            if np.all([board[r-i, c+i] == piece for i in range(STREAK_LENGTH)]):
                return True

    return False

def evaluate_window(window, piece):

    score = 0
    opp_piece = PLAYER_1 if piece == PLAYER_2 else PLAYER_2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):

    score = 0

    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - STREAK_LENGTH + 1):
            window = row_array[c:c+STREAK_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - STREAK_LENGTH + 1):
            window = col_array[r:r+STREAK_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROWS - STREAK_LENGTH + 1):
        for c in range(COLS - STREAK_LENGTH + 1):
            window = [board[r+i][c+i] for i in range(STREAK_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(STREAK_LENGTH - 1, ROWS):
        for c in range(COLS - STREAK_LENGTH + 1):
            window = [board[r-i][c+i] for i in range(STREAK_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):

    return (board == EMPTY).sum() == 0 or winning_move(board, PLAYER_1) or winning_move(board, PLAYER_2)

def minimax(board, depth, alpha, beta, maximizing_player):

    valid_locations = [col for col in range(COLS) if is_valid_location(board, col)]

    if depth == 0 or is_terminal_node(board):
        if winning_move(board, PLAYER_2):
            return (None, 100000000000000)
        elif winning_move(board, PLAYER_1):
            return (None, -10000000000000)
        else:
            return (None, score_position(board, PLAYER_2))

    if maximizing_player:
        value = -np.Inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_2)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (best_col, value)
    else:
        value = np.Inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_1)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (best_col, value)

def play_game():

    board = create_board()
    display_board(board)
    game_over = False
    turn = 0

    while not game_over:
        if turn == 0:
            col = int(input("Player 1, choose a column (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_1)
                if winning_move(board, PLAYER_1):
                    print("PLAYER 1 WINS!")
                    game_over = True
        else:
            col, minimax_score = minimax(board, 5, -np.Inf, np.Inf, True)
            print("Computer chose column:", col)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_2)
                if winning_move(board, PLAYER_2):
                    print("COMPUTER WINS!")
                    game_over = True

        display_board(board)
        turn += 1
        turn %= 2

        if is_terminal_node(board):
            print("GAME OVER")
            game_over = True

if __name__ == '__main__':
    play_game()

