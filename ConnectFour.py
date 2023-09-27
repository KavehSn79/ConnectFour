import numpy as np
import pygame
import sys
import math
import random

#Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (0, 255, 255)

#Get number of rows and columns
rows_num = int(input("Enter number of rows: "))
columns_num = int(input("Enter number of columns: "))

#Board Constant
SQUARESIZE = 75

width = columns_num * SQUARESIZE
height = (rows_num+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

player1 = 0
player2 = 1

empty = 0

mode = int(input("Choose Game Mode:\n1.P vs. P\n2.P vs. AI\n3.AI vs. AI\nYour choice: "))

if mode == 1:
    m1 = 0
    m2 = 0
elif mode == 2:
    m1 = 0
    m2 = 1
elif mode == 3:
    m1 = 1
    m2 = 1


player_piece1 = 1
player_piece2 = 2

WINDOW_LENGTH = 4
    
def find_next_empty_row(board, column):
    for row in range(rows_num):
        if board[row][column] == empty:
            return row

def validate_column_location(board, column):
    return board[rows_num-1][column] == 0

def make_a_move(board, row, column, piece):
    board[row][column] = piece
    
def win_conditions(board, piece):
    #Vertical win
    for c in range(columns_num):
        for r in range(rows_num - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    #Horizontal win
    for c in range(columns_num-3):
        for r in range(rows_num):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    #Positively diagonal win
    for c in range(columns_num-3):
        for r in range(rows_num-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    #Negatively diagonal win
    for c in range(columns_num-3):
        for r in range(3, rows_num):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def calc_score_for_part_of_borad(part_of_board, piece):
    score = 0
    curr_piece = player_piece1
    if piece == player_piece1:
        curr_piece = player_piece2

    if part_of_board.count(piece) == 4:
        score += 500
    elif part_of_board.count(piece) == 3 and part_of_board.count(empty) == 1:
        score += 50
    elif part_of_board.count(piece) == 2 and part_of_board.count(empty) == 2:
        score += 20
    
    if part_of_board.count(curr_piece) == 3 and part_of_board.count(empty) == 1:
        score -= 40
    return score
def Score_center_columns(board, piece):
    score = 0
    center = [int(i) for i in list(board[:, columns_num//2])]
    center_numbers = center.count(piece)
    score += center_numbers * 3
    return score

def Score_Horizontal(board, piece):
    score = 0
    for r in range(rows_num):
        row_arr = [int(i) for i in list(board[r,:])]
        for c in range(columns_num - 3):
            board_part = row_arr[c:c+WINDOW_LENGTH]
            score += calc_score_for_part_of_borad(board_part, piece)
    return score

def Score_Vertical(board, piece):
    score = 0
    for c in range(columns_num):
        column_arr = [int(i) for i in list(board[:,c])]
        for r in range(rows_num-3):
            board_part = column_arr[r:r+WINDOW_LENGTH]
            score += calc_score_for_part_of_borad(board_part, piece)
    return score

def Score_diagonal(board, piece):
    score = 0
    for r in range(rows_num-3):
        for c in range(columns_num-3):
            board_part = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += calc_score_for_part_of_borad(board_part, piece)
    for r in range(rows_num-3):
        for c in range(columns_num-3):
            board_part = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += calc_score_for_part_of_borad(board_part, piece)
    return score

def calc_score(board, piece):
    score = 0
    score += Score_center_columns(board, piece)
    score += Score_Horizontal(board, piece)
    score += Score_Vertical(board, piece)
    score += Score_diagonal(board, piece)
    return score

def find_valid_locations(board):
    valid_locations = []
    for col in range(columns_num):
        if validate_column_location(board, col):
            valid_locations.append(col)
    return valid_locations

def check_win(board):
    return win_conditions(board, player_piece1) or win_conditions(board, player_piece2) or len(find_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = find_valid_locations(board)
    is_leaf = check_win(board)
    if depth == 0 or is_leaf:
    	if is_leaf:
    		if win_conditions(board, player_piece2):
    			return (None, 100000000000000)
    		elif win_conditions(board, player_piece1):
    			return (None, -10000000000000)
    		else: 
    			return (None, 0)
    	else:
    		return (None, calc_score(board, player_piece2))
    if maximizingPlayer:
    	value = -math.inf
    	column = random.choice(valid_locations)
    	for col in valid_locations:
    		row = find_next_empty_row(board, col)
    		b_copy = board.copy()
    		make_a_move(b_copy, row, col, player_piece2)
    		new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
    		if new_score > value:
    			value = new_score
    			column = col
    		alpha = max(alpha, value)
    		if alpha >= beta:
    			break
    	return column, value    
 
    else:
    	value = math.inf
    	column = random.choice(valid_locations)
    	for col in valid_locations:
    		row = find_next_empty_row(board, col)
    		b_copy = board.copy()
    		make_a_move(b_copy, row, col, player_piece1)
    		new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
    		if new_score < value:
    			value = new_score
    			column = col
    		beta = min(beta, value)
    		if alpha >= beta:
    			break
    	return column, value

def make_board(board):
    for c in range(columns_num):
        for r in range(rows_num):
            pygame.draw.rect(screen, LIGHT_BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(columns_num):
    	for r in range(rows_num):		
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def print_board(board):
    	print(np.flip(board, 0))

board = np.zeros((rows_num, columns_num))
print_board(board)
game_over = False
turn = random.randint(player1, player2)

pygame.init()


screen = pygame.display.set_mode(size)
make_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            if turn == player1 and m1 == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                if validate_column_location(board, col):
                    row = find_next_empty_row(board, col)
                    make_a_move(board, row, col, player_piece1)
                    if win_conditions(board, player_piece1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (10,10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    make_board(board)
            elif turn == player2 and m2 == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if validate_column_location(board, col):
                    row = find_next_empty_row(board, col)
                    make_a_move(board, row, col, player_piece2)
                    if win_conditions(board, player_piece2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (10,10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    make_board(board)
    if turn == player1 and m1 == 1 and not game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if validate_column_location(board, col):
            row = find_next_empty_row(board, col)
            make_a_move(board, row, col, player_piece1)
            if win_conditions(board, player_piece1):
                label = myfont.render("Player 1 wins!!", 1, RED)
                screen.blit(label, (10,10))
                game_over = True
            print_board(board)
            make_board(board)
            turn += 1
            turn = turn % 2
    if turn == player2 and m2==1 and not game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if validate_column_location(board, col):
            row = find_next_empty_row(board, col)
            make_a_move(board, row, col, player_piece2)
            if win_conditions(board, player_piece2):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (10,10))
                game_over = True
            print_board(board)
            make_board(board)
            turn += 1
            turn = turn % 2

while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()