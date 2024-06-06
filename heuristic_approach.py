
#để cài đặt các thư viện cần thiết, chạy lệnh: pip install -r requirements.txt
import pygame
import pickle
from IPython.display import clear_output
import numpy as np
import sys
import time

class TicTacToe:
    def __init__(self, size_of_board, length_to_win):
        self.size_of_board = size_of_board
        self.length_to_win = length_to_win
        self.row_count = size_of_board
        self.column_count = size_of_board
        self.action_size = self.row_count * self.column_count

    def get_initial_state(self):
        return np.zeros((self.row_count, self.column_count))

    def get_next_state(self, state, action, player):
        row = action // self.column_count
        column = action % self.column_count
        state[row, column] = player
        return state

    def get_valid_moves(self, state):
        return (state.reshape(-1) == 0).astype(np.uint8)

    def get_limited_valid_moves(self, state):
        limited_moves = (state.reshape(-1) == 0).astype(np.uint8)


        for m in range(len(limited_moves)):

            move = limited_moves[m]
            if move == 0: continue
            limited_moves[m] = 0
            r0 = m // self.size_of_board
            c0 = m % self.size_of_board
            for i in range (-2, 3, 1):
                for j in range (-2, 3, 1):
                    r1 = r0 + i
                    c1 = c0 + j
                    if r1 < 0 or r1 >= self.size_of_board or c1 < 0 or c1 >= self.size_of_board or r1 * self.size_of_board + c1 == m: continue
                    if state[r1][c1] != 0: limited_moves[m] = 1

        return limited_moves

    def get_adjacent_valid_moves(self, state, action):
        limited_moves = (state.reshape(-1) == 0).astype(np.uint8)

        for m in range(len(limited_moves)):

            move = limited_moves[m]
            if move == 0: continue
            limited_moves[m] = 0
            r0 = m // self.size_of_board
            c0 = m % self.size_of_board

            if action == None: return limited_moves
            r_act = action // self.size_of_board
            c_act = action % self.size_of_board
            for i in range (-2, 3, 1):
                for j in range (-2, 3, 1):
                    r1 = r0 + i
                    c1 = c0 + j
                    if r1 < 0 or r1 >= self.size_of_board or c1 < 0 or c1 >= self.size_of_board or r1 * self.size_of_board + c1 == m: continue
                    if not (r_act - 2 <= r1 and r1 <= r_act + 2 and c_act - 2 <= c1 and c1 <= c_act + 2): continue
                    if state[r1][c1] != 0: limited_moves[m] = 1

        return limited_moves

    def check_win(self, state, action):
        if action == None:
            return False

        row = action // self.column_count
        column = action % self.column_count
        player = state[row, column]

        row_lower_limit = - (self.length_to_win - 1) if 0 < row - (self.length_to_win - 1) else 0 - row
        row_upper_limit = (self.length_to_win - 1) if self.row_count > (row + (self.length_to_win - 1)) else (self.row_count - 1) - row

        col_lower_limit = - (self.length_to_win - 1) if 0 < column - (self.length_to_win - 1) else 0 - column
        col_upper_limit = (self.length_to_win - 1) if self.column_count > (column + (self.length_to_win - 1)) else (self.column_count - 1) - column

        count = 0
        for i in range (row_lower_limit, row_upper_limit + 1):
            if state[row + i][column] == player:
                count += 1
                if count == self.length_to_win: return True
            else: count = 0

        count = 0
        for i in range (col_lower_limit, col_upper_limit + 1):
            if state[row][column + i] == player:
                count += 1
                if count == self.length_to_win: return True
            else: count = 0

        count = 0
        for i in range (max(row_lower_limit, col_lower_limit), min(row_upper_limit, col_upper_limit) + 1):
            if state[row + i][column + i] == player:
                count += 1
                if count == self.length_to_win: return True
            else: count = 0

        count = 0
        for i in range (max(- row_upper_limit, col_lower_limit), min(- row_lower_limit, col_upper_limit) + 1):
            if state[row - i][column + i] == player:
                count += 1
                if count == self.length_to_win: return True
            else: count = 0

        return False



    def get_value_and_terminated(self, state, action):
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False

    def get_opponent(self, player):
        return -player

    def get_opponent_value(self, value):
        return -value

    def change_perspective(self, state, player):
        return state * player

def count_attack_pattern(state, action, pattern):
    row = action[0]
    col = action[1]
    state[row][col] = 'X'
    

    count = 0
    for i in range(len(pattern)):
        if pattern[i] == 'X':
            
            # direction (0, 1)
            try:
                sample = []
                for j in range(col - i, col + len(pattern) - i):
                    if j < 0 or j >= len(state[0]): break
                    sample.append(state[row][j])
                if sample == pattern: count += 1
            except:
                pass  
            
            # direction (1, 0)
            try:
                sample = []
                for j in range(row - i, row + len(pattern) - i):
                    if j < 0 or j >= len(state[0]): break
                    sample.append(state[j][col])
                if sample == pattern: count += 1
            except:
                pass 

            # direction (1, 1)
            try:
                sample = []
                for j in range(- i, len(pattern) - i):
                    if row + j < 0 or row + j >= len(state[0]): break
                    if col + j < 0 or col + j >= len(state[0]): break
                    sample.append(state[row + j][col + j])
                if sample == pattern: count += 1
            except:
                pass 

            # direction (1, -1)
            try:
                sample = []
                for j in range(- i, len(pattern) - i):
                    if row - j < 0 or row - j >= len(state[0]): break
                    if col + j < 0 or col + j >= len(state[0]): break
                    sample.append(state[row - j][col + j])
                if sample == pattern: count += 1
            except:
                pass

    return count      

def count_defense_pattern(state, action, pattern):
    row = action[0]
    col = action[1]
    state[row][col] = 'D'
    

    count = 0
    for i in range(len(pattern)):
        if pattern[i] == 'D':
            
            # direction (0, 1)
            try:
                sample = []
                for j in range(col - i, col + len(pattern) - i):
                    if j < 0 or j >= len(state[0]): break
                    sample.append(state[row][j])
                if sample == pattern: count += 1
            except:
                pass  
            
            # direction (1, 0)
            try:
                sample = []
                for j in range(row - i, row + len(pattern) - i):
                    if j < 0 or j >= len(state[0]): break
                    sample.append(state[j][col])
                if sample == pattern: count += 1
            except:
                pass 

            # direction (1, 1)
            try:
                sample = []
                for j in range(- i, len(pattern) - i):
                    if row + j < 0 or row + j >= len(state[0]): break
                    if col + j < 0 or col + j >= len(state[0]): break
                    sample.append(state[row + j][col + j])
                if sample == pattern: count += 1
            except:
                pass 

            # direction (1, -1)
            try:
                sample = []
                for j in range(- i, len(pattern) - i):
                    if row - j < 0 or row - j >= len(state[0]): break
                    if col + j < 0 or col + j >= len(state[0]): break
                    sample.append(state[row - j][col + j])
                if sample == pattern: count += 1
            except:
                pass

    return count      

ATTACK_RATE = 1
DEFENSE_RATE = 0.85


# Giải thích: 
# - thế cờ open: tất cả các nước 5 (có thể tạo từ các quân của thế) đều khả thi
# - thế cờ block 1 side: 1 trong 2 phía bị chặn do đó bị giảm bớt những nước 5 khả thi ở phía đó
# - thế cờ block 2 sides: cả 2 phía bị chặn do đó bị giảm bớt những nước 5 khả thi ở cả 2 phía
attack_position_and_score = [

#ATTACK:    

# 2 pieces:

    # open:
    (['_', '_', '_', 'X', 'X', '_', '_', '_'], 20, 0),
    (['_', '_', 'X', '_', 'X', '_', '_'], 20, 0),
    (['_', 'X', '_', '_', 'X', '_'], 20, 0),
    (['X', '_', '_', '_', 'X'], 15, 0),

    # block 1 side:
    (['O', '_', '_', 'X', 'X', '_', '_', '_'], 17, 0),
    (['O', '_', 'X', 'X', '_', '_', '_'], 14, 0),
    (['O', 'X', 'X', '_', '_', '_'], 10, 0),
    (['_', '_', '_', 'X', 'X', '_', '_', 'O'], 17, 0),
    (['_', '_', '_', 'X', 'X', '_', 'O'], 14, 0),
    (['_', '_', '_', 'X', 'X', 'O'], 10, 0),

    (['O', '_', 'X', '_', 'X', '_', '_'], 14, 0),
    (['O', 'X', '_', 'X', '_', '_'], 10, 0),
    (['_', '_', 'X', '_', 'X', '_', 'O'], 14, 0),
    (['_', '_', 'X', '_', 'X', 'O'], 10, 0),
    (['O', 'X', '_', '_', 'X', '_'], 8, 0),
    (['_', 'X', '_', '_', 'X', 'O'], 8, 0),

    (['W', '_', '_', 'X', 'X', '_', '_', '_'], 17, 0),
    (['W', '_', 'X', 'X', '_', '_', '_'], 14, 0),
    (['W', 'X', 'X', '_', '_', '_'], 10, 0),
    (['_', '_', '_', 'X', 'X', '_', '_', 'W'], 17, 0),
    (['_', '_', '_', 'X', 'X', '_', 'W'], 14, 0),
    (['_', '_', '_', 'X', 'X', 'W'], 10, 0),

    (['W', '_', 'X', '_', 'X', '_', '_'], 14, 0),
    (['W', 'X', '_', 'X', '_', '_'], 10, 0),
    (['_', '_', 'X', '_', 'X', '_', 'W'], 14, 0),
    (['_', '_', 'X', '_', 'X', 'W'], 10, 0),
    (['W', 'X', '_', '_', 'X', '_'], 8, 0),
    (['_', 'X', '_', '_', 'X', 'W'], 8, 0),


    # block 2 sides:
    (['O', '_', '_', 'X', 'X', '_', '_', 'O'], 8, 0),
    (['O', '_', '_', 'X', 'X', '_', 'O'], 7, 0),
    (['O', '_', 'X', 'X', '_', '_', 'O'], 7, 0),
    (['O', '_', 'X', '_', 'X', '_', 'O'], 7, 0),

    (['W', '_', '_', 'X', 'X', '_', '_', 'W'], 8, 0),
    (['W', '_', '_', 'X', 'X', '_', 'W'], 7, 0),
    (['W', '_', 'X', 'X', '_', '_', 'W'], 7, 0),
    (['W', '_', 'X', '_', 'X', '_', 'W'], 7, 0),

    (['O', '_', '_', 'X', 'X', '_', '_', 'W'], 8, 0),
    (['O', '_', '_', 'X', 'X', '_', 'W'], 7, 0),
    (['O', '_', 'X', 'X', '_', '_', 'W'], 7, 0),
    (['O', '_', 'X', '_', 'X', '_', 'W'], 7, 0),

    (['W', '_', '_', 'X', 'X', '_', '_', 'O'], 8, 0),
    (['W', '_', '_', 'X', 'X', '_', 'O'], 7, 0),
    (['W', '_', 'X', 'X', '_', '_', 'O'], 7, 0),
    (['W', '_', 'X', '_', 'X', '_', 'O'], 7, 0),

# 3 pieces:

    # open:
    (['_', '_', 'X', 'X', 'X', '_', '_'], 50, 1),
    (['_', 'X', 'X', '_', 'X', '_'], 50, 1),
    (['X', 'X', '_', '_', 'X'], 30, 1),
    (['_', 'X', '_', 'X', 'X', '_'], 50, 1),
    (['X', '_', 'X', '_', 'X'], 30, 0),
    (['X', '_', '_', 'X', 'X'], 30, 0),

    # block 1 side:
    (['O', '_', 'X', 'X', 'X', '_', '_'], 50, 1),
    (['O', 'X', 'X', 'X', '_', '_'], 30, 0),
    (['O', 'X', 'X', '_', 'X', '_'], 30, 0),
    (['O', 'X', '_', 'X', 'X', '_'], 30, 0),
    (['_', '_', 'X', 'X', 'X', '_', 'O'], 50, 1),
    (['_', '_', 'X', 'X', 'X', 'O'], 30, 0),
    (['_', 'X', 'X', '_', 'X', 'O'], 30, 0),
    (['_', 'X', '_', 'X', 'X', 'O'], 30, 0),

    (['W', '_', 'X', 'X', 'X', '_', '_'], 50, 1),
    (['W', 'X', 'X', 'X', '_', '_'], 30, 0),
    (['W', 'X', 'X', '_', 'X', '_'], 30, 0),
    (['W', 'X', '_', 'X', 'X', '_'], 30, 0),
    (['_', '_', 'X', 'X', 'X', '_', 'W'], 50, 1),
    (['_', '_', 'X', 'X', 'X', 'W'], 30, 0),
    (['_', 'X', 'X', '_', 'X', 'W'], 30, 0),
    (['_', 'X', '_', 'X', 'X', 'W'], 30, 0),

    # block 2 sides:
    (['O', '_', 'X', 'X', 'X', '_', 'O'], 30, 0),
    (['O', '_', 'X', 'X', 'X', '_', 'W'], 30, 0),
    (['W', '_', 'X', 'X', 'X', '_', 'O'], 30, 0),

# 4 pieces:

    # open:
    (['_', 'X', 'X', 'X', 'X', '_'], 500, 2),
    (['X', '_', 'X', 'X', 'X'], 80, 2),
    (['X', 'X', '_', 'X', 'X'], 80, 2),
    (['X', 'X', 'X', '_', 'X'], 80, 2),

    # block 1 side:
    (['O', 'X', 'X', 'X', 'X', '_'], 80, 2),
    (['_', 'X', 'X', 'X', 'X', 'O'], 80, 2),
    (['W', 'X', 'X', 'X', 'X', '_'], 80, 2),
    (['_', 'X', 'X', 'X', 'X', 'W'], 80, 2),

# 5 pieces
    (['X', 'X', 'X', 'X', 'X'], 9999, 2),
    
]

defense_position_and_score = [
#DEFENSE:

# 1 piece:
    (['D', 'O', '_'], 1, 0),
    (['_', 'O', 'D'], 1, 0),

# 2 pieces:
    # open:
    (['_', '_', 'D', 'O', 'O', '_', '_'], 50, 1),
    (['_', '_', 'O', 'D', 'O', '_', '_'], 50, 1),
    (['_', '_', 'O', 'O', 'D', '_', '_'], 50, 1),

    (['_', 'D', 'O', '_', 'O', '_'], 50, 1),
    (['_', 'O', 'D', '_', 'O', '_'], 50, 1),
    (['_', 'O', 'O', '_', 'D', '_'], 50, 1),

    (['D', 'O', '_', '_', 'O'], 30, 0),
    (['O', 'D', '_', '_', 'O'], 30, 0),
    (['O', 'O', '_', '_', 'D'], 30, 0),


    (['_', 'D', '_', 'O', 'O', '_'], 50, 1),
    (['_', 'O', '_', 'D', 'O', '_'], 50, 1),
    (['_', 'O', '_', 'O', 'D', '_'], 50, 1),

    (['D', '_', 'O', '_', 'O'], 30, 0),
    (['O', '_', 'D', '_', 'O'], 30, 0),
    (['O', '_', 'O', '_', 'D'], 30, 0),

    (['D', '_', '_', 'O', 'O'], 30, 0),
    (['O', '_', '_', 'D', 'O'], 30, 0),
    (['O', '_', '_', 'O', 'D'], 30, 0),

    # block 1 side:
    (['X', '_', 'D', 'O', 'O', '_', '_'], 50, 1),
    (['X', '_', 'O', 'D', 'O', '_', '_'], 50, 1),
    (['X', '_', 'O', 'O', 'D', '_', '_'], 50, 1),

    (['X', 'D', 'O', 'O', '_', '_'], 30, 0),
    (['X', 'O', 'D', 'O', '_', '_'], 30, 0),
    (['X', 'O', 'O', 'D', '_', '_'], 30, 0),

    (['X', 'D', 'O', '_', 'O', '_'], 30, 0),
    (['X', 'O', 'D', '_', 'O', '_'], 30, 0),
    (['X', 'O', 'O', '_', 'D', '_'], 30, 0),

    (['X', 'D', '_', 'O', 'O', '_'], 30, 0),
    (['X', 'O', '_', 'D', 'O', '_'], 30, 0),
    (['X', 'O', '_', 'O', 'D', '_'], 30, 0),

    (['_', '_', 'D', 'O', 'O', '_', 'X'], 50, 1),
    (['_', '_', 'O', 'D', 'O', '_', 'X'], 50, 1),
    (['_', '_', 'O', 'O', 'D', '_', 'X'], 50, 1),

    (['_', '_', 'D', 'O', 'O', 'X'], 30, 0),
    (['_', '_', 'O', 'D', 'O', 'X'], 30, 0),
    (['_', '_', 'O', 'O', 'D', 'X'], 30, 0),

    (['_', 'D', 'O', '_', 'O', 'X'], 30, 0),
    (['_', 'O', 'D', '_', 'O', 'X'], 30, 0),
    (['_', 'O', 'O', '_', 'D', 'X'], 30, 0),

    (['_', 'D', '_', 'O', 'O', 'X'], 30, 0),
    (['_', 'O', '_', 'D', 'O', 'X'], 30, 0),
    (['_', 'O', '_', 'O', 'D', 'X'], 30, 0),

    (['W', '_', 'D', 'O', 'O', '_', '_'], 50, 1),
    (['W', '_', 'O', 'D', 'O', '_', '_'], 50, 1),
    (['W', '_', 'O', 'O', 'D', '_', '_'], 50, 1),

    (['W', 'D', 'O', 'O', '_', '_'], 30, 0),
    (['W', 'O', 'D', 'O', '_', '_'], 30, 0),
    (['W', 'O', 'O', 'D', '_', '_'], 30, 0),

    (['W', 'D', 'O', '_', 'O', '_'], 30, 0),
    (['W', 'O', 'D', '_', 'O', '_'], 30, 0),
    (['W', 'O', 'O', '_', 'D', '_'], 30, 0),

    (['W', 'D', '_', 'O', 'O', '_'], 30, 0),
    (['W', 'O', '_', 'D', 'O', '_'], 30, 0),
    (['W', 'O', '_', 'O', 'D', '_'], 30, 0),

    (['_', '_', 'D', 'O', 'O', '_', 'W'], 50, 1),
    (['_', '_', 'O', 'D', 'O', '_', 'W'], 50, 1),
    (['_', '_', 'O', 'O', 'D', '_', 'W'], 50, 1),

    (['_', '_', 'D', 'O', 'O', 'W'], 30, 0),
    (['_', '_', 'O', 'D', 'O', 'W'], 30, 0),
    (['_', '_', 'O', 'O', 'D', 'W'], 30, 0),

    (['_', 'D', 'O', '_', 'O', 'W'], 30, 0),
    (['_', 'O', 'D', '_', 'O', 'W'], 30, 0),
    (['_', 'O', 'O', '_', 'D', 'W'], 30, 0),

    (['_', 'D', '_', 'O', 'O', 'W'], 30, 0),
    (['_', 'O', '_', 'D', 'O', 'W'], 30, 0),
    (['_', 'O', '_', 'O', 'D', 'W'], 30, 0),

    # block 2 sides:
    (['X', '_', 'D', 'O', 'O', '_', 'X'], 30, 0),
    (['X', '_', 'O', 'D', 'O', '_', 'X'], 30, 0),
    (['X', '_', 'O', 'O', 'D', '_', 'X'], 30, 0),
    
    (['X', '_', 'D', 'O', 'O', '_', 'W'], 30, 0),
    (['X', '_', 'O', 'D', 'O', '_', 'W'], 30, 0),
    (['X', '_', 'O', 'O', 'D', '_', 'W'], 30, 0),

    (['W', '_', 'D', 'O', 'O', '_', 'X'], 30, 0),
    (['W', '_', 'O', 'D', 'O', '_', 'X'], 30, 0),
    (['W', '_', 'O', 'O', 'D', '_', 'X'], 30, 0),


# 3 pieces:
    #open:
    (['_', 'D', 'O', 'O', 'O', '_'], 500, 2),
    (['_', 'O', 'O', 'O', 'D', '_'], 500, 2),
    (['_', 'O', 'D', 'O', 'O', '_'], 500, 2),
    (['_', 'O', 'O', 'D', 'O', '_'], 500, 2),

    (['D', '_', 'O', 'O', 'O'], 80, 2),
    (['O', '_', 'D', 'O', 'O'], 80, 2),
    (['O', '_', 'O', 'D', 'O'], 80, 2),
    (['O', '_', 'O', 'O', 'D'], 80, 2),

    (['D', 'O', '_', 'O', 'O'], 80, 2),
    (['O', 'D', '_', 'O', 'O'], 80, 2),
    (['O', 'O', '_', 'D', 'O'], 80, 2),
    (['O', 'O', '_', 'O', 'D'], 80, 2),

    (['D', 'O', 'O', '_', 'O'], 80, 2),
    (['O', 'D', 'O', '_', 'O'], 80, 2),
    (['O', 'O', 'D', '_', 'O'], 80, 2),
    (['O', 'O', 'O', '_', 'D'], 80, 2),

    # block 1 side
    (['X', 'D', 'O', 'O', 'O', '_'], 80, 2),
    (['X', 'O', 'D', 'O', 'O', '_'], 80, 2),
    (['X', 'O', 'O', 'D', 'O', '_'], 80, 2),
    (['X', 'O', 'O', 'O', 'D', '_'], 80, 2),

    (['_', 'D', 'O', 'O', 'O', 'X'], 80, 2),
    (['_', 'O', 'D', 'O', 'O', 'X'], 80, 2),
    (['_', 'O', 'O', 'D', 'O', 'X'], 80, 2),
    (['_', 'O', 'O', 'O', 'D', 'X'], 80, 2),

    (['W', 'D', 'O', 'O', 'O', '_'], 80, 2),
    (['W', 'O', 'D', 'O', 'O', '_'], 80, 2),
    (['W', 'O', 'O', 'D', 'O', '_'], 80, 2),
    (['W', 'O', 'O', 'O', 'D', '_'], 80, 2),

    (['_', 'D', 'O', 'O', 'O', 'W'], 80, 2),
    (['_', 'O', 'D', 'O', 'O', 'W'], 80, 2),
    (['_', 'O', 'O', 'D', 'O', 'W'], 80, 2),
    (['_', 'O', 'O', 'O', 'D', 'W'], 80, 2),
# 4 pieces:

    (['D', 'O', 'O', 'O', 'O'], 9999, 2),
    (['O', 'D', 'O', 'O', 'O'], 9999, 2),
    (['O', 'O', 'D', 'O', 'O'], 9999, 2),
    (['O', 'O', 'O', 'D', 'O'], 9999, 2),
    (['O', 'O', 'O', 'O', 'D'], 9999, 2),

]

def evaluate(state, action):
    

    # convert 1 to X, -1 to O, 0 to _
    final_state = [['_' for i in range(len(state))] for j in range(len(state))]

    for r in range(len(state)):
        for c in range(len(state[0])):
            if state[r][c] == 1: final_state[r][c] = 'X'
            elif state[r][c] == -1: final_state[r][c] = 'O'
            else: final_state[r][c] = '_'
        

    # add wall to state
    for row in final_state:
        row.insert(0, 'W')
        row.append('W')
    final_state.insert(0, ['W' for _ in range(len(final_state[0]))])
    final_state.append(['W' for _ in range(len(final_state[0]))])

    # evaluation
    act_row = action // len(state)
    act_col = action % len(state)

    total_score = 0
    attack_score = 0
    defense_score = 0
    attack_critical = 0
    defense_critical = 0
    for pattern, score, critical in attack_position_and_score:
        pattern_count = count_attack_pattern(final_state, (act_row + 1, act_col + 1), pattern)
        attack_score += pattern_count * score
        attack_critical += pattern_count * critical
    for pattern, score, critical in defense_position_and_score:
        pattern_count = count_defense_pattern(final_state, (act_row + 1, act_col + 1), pattern)
        defense_score += pattern_count * score
        defense_critical += pattern_count * critical

    if attack_critical == 2: attack_score += 100
    elif attack_critical >= 3: attack_score += 500
    if defense_critical == 2: defense_score += 100
    elif defense_critical >= 3: defense_score += 500
    
    total_score = attack_score * ATTACK_RATE + defense_score * DEFENSE_RATE

    return int(total_score)
    # print(count_pattern(final_state, (act_row + 1, act_col + 1), ['_', 'X', 'X', 'X', 'X', '_']))

def print_policy(policy):

    rows = cols = int(len(policy) ** 0.5)  # assuming policy is a square 1D array

    for i in range(rows):
        for j in range(cols):
            print("{:4.0f}".format(policy[i * cols + j]), end=' ')
        print()

def get_policy_heuristic(game, state):

    valid_moves = game.get_limited_valid_moves(state)
    policy = np.zeros(len(state) * len(state[0]))

    if np.sum(valid_moves) == len(valid_moves) or np.sum(valid_moves) == 0:
        policy[len(state) * int(len(state) / 2) + int(len(state) / 2)] = 1
        return policy
        
    for i in range(len(policy)):
        if valid_moves[i] == 1:
            policy[i] = evaluate(state, i)
    
    return policy

def print_board(state):

    clear_output()
    print("------------------------")
   
    print (end = "   ")
    for col in range (state[0].size):

        print("{0:>2}".format(col), end = "  ")
    print("")
    for row in range (state[0].size):
        print("{0:>2}".format(row), end="  ")
        for col in range (state[0].size):
            if state[row][col] == 1:
                print("\033[94mX\033[0m", end = "   ")
            elif state[row][col] == -1:
                print("\033[91mO\033[0m", end = "   ")
            else:
                print("_", end = "   ")
        print("")

def human_play(board_size, win_length):
    # Initialize Pygame (frontend)
    
    clock = pygame.time.Clock()
    global player
    font = pygame.font.Font(None, 60)
    # Game state
    board = [[None for _ in range(ROWS)] for _ in range(COLS)]


    #backend
    tictactoe = TicTacToe(board_size, win_length)
    player = 1
    state = tictactoe.get_initial_state()

    all_state = []
    act_probs = []
    z_value = []

    print_board(state)
    
    while True:
        clock.tick(60)
        if player == 1: 
            neutral_state = tictactoe.change_perspective(state, player)
            policy = get_policy_heuristic(tictactoe, neutral_state)
            action = np.argmax(policy)

            if player == 1:
                board[action % tictactoe.column_count][action // tictactoe.column_count] = 'X'
            else: 
                board[action % tictactoe.column_count][action // tictactoe.column_count] = 'O'
            #backend
            
            neutral_state = np.array(neutral_state).reshape(-1)
            all_state.append(neutral_state)
            probs = np.zeros(tictactoe.action_size)
            probs[action] = 1
            act_probs.append(probs)
            z_value.append(player)

            state = tictactoe.get_next_state(state, action, player)
            winner, is_terminal = tictactoe.get_value_and_terminated(state, action)
            
            if is_terminal:
                draw_board(board)
                pygame.display.update()
                if winner == 1:
                    print(player, "won")
                    winner_text = font.render("PLAYER " +str(player) + " WON!", True, GREEN)

                else:
                    player = 0
                    print("draw")
                    winner_text = font.render("DRAW", True, YELLOW)

                z_value = [i * player for i in z_value]
                result_tuple = (all_state, (act_probs,  z_value))

                WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(3000)
                return create_dataset(result_tuple)
            player = tictactoe.get_opponent(player)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                
                if board[col][row] != None:
                    continue

                if player == 1: board[col][row] = 'X'
                else: board[col][row] = 'O'

                #backend
                

                action = row * tictactoe.column_count + col
                neutral_state = tictactoe.change_perspective(state, player)
                #state for counting pattern
                
                neutral_state = np.array(neutral_state).reshape(-1)
                all_state.append(neutral_state)
                probs = np.zeros(tictactoe.action_size)
                probs[action] = 1
                act_probs.append(probs)
                z_value.append(player)

                state = tictactoe.get_next_state(state, action, player)
                winner, is_terminal = tictactoe.get_value_and_terminated(state, action)

                if is_terminal:
                    draw_board(board)
                    pygame.display.update()
                    if winner == 1:
                        print(player, "won")
                        winner_text = font.render("PLAYER " +str(player) + " WON!", True, GREEN)

                    else:
                        player = 0
                        print("draw")
                        winner_text = font.render("DRAW", True, YELLOW)

                    z_value = [i * player for i in z_value]
                    result_tuple = (all_state, (act_probs,  z_value))

                    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    return create_dataset(result_tuple)
                player = tictactoe.get_opponent(player)

        draw_board(board)
        pygame.display.update()

def get_human_play_examples(board_size, win_length):
    file_name = 'dataset' + str(board_size) + '_' + str(win_length) + '.pkl'
    try:
        with open(file_name, 'rb') as f:
            data_set = pickle.load(f)
    except:
        data_set = []

    pygame.init()
    while True:
        data_set.append(human_play(board_size, win_length))
        with open(file_name, 'wb') as f:
            pickle.dump(data_set, f)

# if __name__ == '__main__':

board_size = int(input("Nhập kích cỡ bàn cờ (ví dụ bàn cò 8x8 thì nhập 8): "))
win_length = int(input("Nhập độ dài chiến thắng (ví dụ nếu 5 quân cờ liên tiếp là thắng thì nhập 5): "))

# Set up some constants
WIDTH, HEIGHT = 600, 600
ROWS = board_size
COLS = board_size
SQUARE_SIZE = WIDTH // COLS

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

def draw_board(board):
    font = pygame.font.Font(None, 30)  # Increase font size
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(WIN, WHITE, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[i][j] == 'X':
                text = font.render('X', True, BLUE)
                text_rect = text.get_rect(center=(i*SQUARE_SIZE + SQUARE_SIZE // 2, j*SQUARE_SIZE + SQUARE_SIZE // 2))
                WIN.blit(text, text_rect)
            elif board[i][j] == 'O':
                text = font.render('O', True, RED)
                text_rect = text.get_rect(center=(i*SQUARE_SIZE + SQUARE_SIZE // 2, j*SQUARE_SIZE + SQUARE_SIZE // 2))
                WIN.blit(text, text_rect)

    # Draw grid lines
    for i in range(ROWS + 1):
        pygame.draw.line(WIN, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT))
    for j in range(COLS + 1):
        pygame.draw.line(WIN, BLACK, (0, j * SQUARE_SIZE), (WIDTH, j * SQUARE_SIZE))


if __name__ == "__main__":
    get_human_play_examples(board_size, win_length)



    


