#!/usr/bin/python

import random
import math

Optimal_depth = 3
DEPTH = 4
dp = {}
best_depth = 10
MAX_CELLS_NO = 10
worst_depth = 0
block_dp={}
"""
	related to heuristic
"""
freemove = False
Three_in_a_Row = [
  [ 0, 1, 2 ],
  [ 3, 4, 5 ],
  [ 6, 7, 8 ],
  [ 0, 3, 6 ],
  [ 1, 4, 7 ],
  [ 2, 5, 8 ],
  [ 0, 4, 8 ],
  [ 2, 4, 6 ]
]

Cell_Heuristic = [
	[0, -10, -100, -1000],
	[10, 0, 50, 0],
	[100, -50, 0, 0],
	[1000, 0, 0, 0]
]

Block_Heuristic = [
	[0, -1000, -2000, -100000000],
	[1000, 0, 800, 0],
	[2000, -800, 0, 0],
	[100000000, 0, 0, 0]
]

def getOpponent(player):
	if player=='x':
		return 'o'
	else:
		return 'x'

def forking(line1,line2,block_status,player):
	opp = getOpponent(player)
	pl1 = 0
	ot1 = 0
	for e in Three_in_a_Row[line1]:
		if block_status[e] == player:
			pl1+=1
		elif block_status[e] == opp:
			ot1 += 1
	pl2 = 0
	ot2 = 0
	for e in Three_in_a_Row[line1]:
		if block_status[e] == player:
			pl2 += 1
		elif block_status[e] == opp:
			ot2 += 1

	if pl1 == 2 and ot1 == 0:
		if pl2 == 2 and ot2 == 0:
			return 1800
	if pl1 == 0 and ot1 == 2:
		if pl2 == 0 and ot2 == 2:
			return -1800
	return 0


#explicitly check if the player has won the entire board
def checkWin(block_status, player):
	
	opp = getOpponent(player)
	
	for i in range(8):
		score = 0
		pl = 0
		ot = 0
		for j in range(3):
			if block_status[Three_in_a_Row[i][j]] == player:
				pl += 1
			elif block_status[Three_in_a_Row[i][j]] == opp:
				ot += 1

		score += Block_Heuristic[pl][ot]

		if abs(score) >= 100000000:
			return score

	return score

def getBlockString(game_board,block):
	start_row = 3*(block/3);
	start_column = 3*(block%3);
	small_board = ""
	for row in range( start_row, start_row + 3 ):
		for col in range(start_column, start_column + 3):
			small_board += game_board[row][col]
	return small_board


def blockUtility(game_board,block,player):
	score = 0
	opp = getOpponent(player)
	key = getBlockString(game_board,block)
	if key in block_dp:
		return block_dp[key]

	for i in range(8):
		pl = 0
		ot = 0
		for j in range(3):
			if game_board[3*(block/3) + Three_in_a_Row[i][j]/3 ][3*(block%3) + Three_in_a_Row[i][j]%3] == player:
				pl += 1
			elif game_board[3*(block/3) + Three_in_a_Row[i][j]/3 ][3*(block%3) + Three_in_a_Row[i][j]%3] == opp:
				ot += 1

		score += Cell_Heuristic[pl][ot]
	block_dp[key] = score
	return score

def boardUtility(game_board,player,block_status):

	score = 0
	opp = getOpponent(player)
	
	for block in range(9):
		score += blockUtility(game_board,block,player)

	#for board
	for i in range(8):
		ot = 0
		pl = 0
		for j in range(3):
			if block_status[Three_in_a_Row[i][j]] == player:
				pl+=1
			elif block_status[Three_in_a_Row[i][j]] == opp:
				ot+=1

		score += Block_Heuristic[pl][ot]

	#forking board
	row = [0,1,2]
	col = [3,4,5]
	dia = [6,7]
	for r in row:
		for c in col:
			score += forking(r,c,block_status,player)
		for d in dia:
			score+= forking(r,d,block_status,player)

	for c in col:
		for d in dia:
			score+= forking(c,d,block_status,player)

	#non centre
	for i in range(3):
		for j in range(3):
			if game_board[3+i][3+j] == opp:
				score -= 50
	
	row = [1,4,7]
	for i in row:
		for j in row:
			if game_board[i][j] == player:
				score -= 20

	#centre block
	if block_status[4] == player:
		score += 500
	elif block_status[4] == opp:
		score -= 500

	return score

def getString(game_board):
	key = ""
	for i in range(9):
		for j in range(9):
			key += game_board[i][j] 

	return key

def get_valid_moves(prev_move, game_board, block_status,player,main_player):
	opp = getOpponent(player)
	blocks_allowed = get_blocks_allowed(prev_move, block_status,game_board,player);
	possible_moves = get_emtpy_cells(game_board,blocks_allowed )

	free_list=[]
	max_cells_allowed = []

	return possible_moves


def get_emtpy_cells(game_board, blocks_allowed):
	cells = []  
	
	for status in blocks_allowed:
		index1 = status/3
		index2 = status%3
		for i in range(index1*3,index1*3+3):
			for j in range(index2*3,index2*3+3):
				if game_board[i][j] == '-':
					cells.append((i,j))

	return cells


def free_move(block_status,game_board,player):
	freemove = True
	blocks_allowed=[]
	free_list = []
	for i in range(9):
		if block_status[i]=='-':
			blocks_allowed.append(i)
	
	return blocks_allowed


def get_blocks_allowed(prev_move, block_status,game_board,player):

	blocks_allowed = []
	if prev_move[0] < 0 or prev_move[1] <0:
		blocks_allowed = [4]
	elif prev_move[0] % 3 == 0 and prev_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif prev_move[0] % 3 == 1 and prev_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif prev_move[0] % 3 == 0 and prev_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif prev_move[0] % 3 == 2 and prev_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif prev_move[0] % 3 == 1 and prev_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif prev_move[0] % 3 == 1 and prev_move[1] % 3 == 1:
		blocks_allowed = [4]
	elif prev_move[0] % 3 == 2 and prev_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif prev_move[0] % 3 == 0 and prev_move[1] % 3 == 1:
		blocks_allowed = [0,2]	
	elif prev_move[0] % 3 == 2 and prev_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	else:
		sys.exit(1)

	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_status[i] == '-':
			final_blocks_allowed.append(i)


	if len(final_blocks_allowed)==0:
		return free_move(block_status,game_board,player)
	else:
		return final_blocks_allowed


def update_lists(game_board, block_stat, move_ret, fl):

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0

	flag = 0
	for i in range(id1*3,id1*3+3):
		for j in range(id2*3,id2*3+3):
			if game_board[i][j] == '-':
				flag = 1


	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if flag == 0:
		block_stat[block_no] = 'D'
	if mflg == 1:
		block_stat[block_no] = fl
	

	return block_stat


def max_play(prev_move, game_board, depth, block_status, playerFlag,alpha,beta, DEPTH_CONST):

	opp = getOpponent(playerFlag)
	bs = update_lists(game_board, block_status[:], prev_move, opp)
	global best_depth
	
	win_score = checkWin(bs, playerFlag)
	if abs(win_score) >= 100000000:
		return win_score

	if depth == DEPTH_CONST:
		uti = boardUtility(game_board,playerFlag,bs)
		return uti

	moves = get_valid_moves(prev_move, game_board, bs,playerFlag,playerFlag)
	for move in moves:
		game_board[move[0]][move[1]]=playerFlag
		score= min_play(move, game_board[:], depth+1, bs[:], playerFlag,alpha,beta, DEPTH)
		game_board[move[0]][move[1]]="-"
		if alpha > beta:
			return alpha
		if score > alpha:
			best_move = move
			best_depth = depth
			alpha = score
		elif score == alpha:
			if depth < best_depth:
				best_depth = depth
				best_move = move
				alpha = score
	return alpha



def min_play(prev_move, game_board, depth, block_status, playerFlag,alpha,beta, DEPTH_CONST):
	opp = getOpponent(playerFlag)
	bs = update_lists(game_board, block_status[:], prev_move, playerFlag)

	global worst_depth
	win_score = checkWin(bs, playerFlag)
	if abs(win_score) >= 100000000:
		return win_score

	if depth == DEPTH_CONST:
		uti = boardUtility(game_board,playerFlag,bs)
		return uti

	moves = get_valid_moves(prev_move, game_board, bs,opp,playerFlag) 
	for move in moves:
		game_board[move[0]][move[1]]=opp
		score = max_play(move, game_board[:], depth+1, bs[:], playerFlag,alpha,beta, DEPTH)
		game_board[move[0]][move[1]]="-"
		if alpha > beta:
			return beta
		if score < beta:
			best_move = move
			worst_depth = depth
			beta = score
		elif score == beta:
			if depth > worst_depth:
				worst_depth = depth
				best_move = move
				beta = score

	return beta

def minimax(prev_move, game_board, depth, block_status, playerFlag):
	moves = get_valid_moves( prev_move, game_board, block_status,playerFlag,playerFlag)
	global worst_depth 
	global best_depth 
	worst_depth = 0
	best_depth = 10
	best_move = moves[0]
	best_score = float('-inf')
	
	for move in moves:
		game_board[move[0]][move[1]]=playerFlag
		score = min_play(move, game_board[:], depth+1, block_status[:], playerFlag,float('-inf'),float('inf'), DEPTH)
		
		if score > best_score:
			best_move = move

			best_score = score
	
		game_board[move[0]][move[1]]="-"
	return best_move

def update_block_status(game_board):
		block_status = ['-','-','-','-','-','-','-','-','-']
		for i in range(9):
			for j in range(9):
				if game_board[i][j]!='-':
					block_status = update_lists(game_board, block_status, (i,j), game_board[i][j])
		return block_status

class Player49:

	def __init__(self):
		"""
		Return best move 
		"""
		pass

	def getInput(self):
		b = []
		for i in range(0,9):
			l = []
			a = raw_input()
			for j in a:
				if j == '-' or j == 'x' or j == 'o':
					l.append(j)
			
			b.append(l)

		return b;

	def move(self, game_board, block_status, prev_move, playerFlag):
		
		if prev_move[0] < 0 or prev_move[1] < 0:
			return (3,3)
		mov = minimax(prev_move, game_board[:], 0, block_status, playerFlag)
		
		return mov
"""
Trace of the game against random bot

Random plays x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (8, 5) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (3, 6) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  o - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (1, 4) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - - -  o - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (3, 4) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 6) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (4, 0) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
o - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (6, 2) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
o - -  - - -  - - -
- - -  - - -  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (4, 7) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
o - -  - - -  - o -
- - -  - - -  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (5, 4) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
o - -  - - -  - o -
- - -  - x -  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (8, 6) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

- - -  - o -  o - -
o - -  - - -  - o -
- - -  - x -  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (3, 0) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  - o -  o - -
o - -  - - -  - o -
- - -  - x -  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (4, 1) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  - o -  o - -
o o -  - - -  - o -
- - -  - x -  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (5, 5) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  - o -  o - -
o o -  - - -  - o -
- - -  - x x  - - -

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (5, 8) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  - o -  o - -
o o -  - - -  - o -
- - -  - x x  - - o

- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 1 made the move: (7, 4) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  - o -  o - -
o o -  - - -  - o -
- - -  - x x  - - o

- - x  - - -  - - -
- - -  - x -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 2 made the move: (3, 3) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- - -  - x x  - - o

- - x  - - -  - - -
- - -  - x -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 1 made the move: (5, 1) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x -  - x x  - - o

- - x  - - -  - - -
- - -  - x -  - - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 2 made the move: (7, 6) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - -  - - -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x -  - x x  - - o

- - x  - - -  - - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 1 made the move: (2, 2) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - x  - - -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x -  - x x  - - o

- - x  - - -  - - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 2 made the move: (6, 3) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - x  - - -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x -  - x x  - - o

- - x  o - -  - - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 1 made the move: (2, 4) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x -  - x x  - - o

- - x  o - -  - - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - -
==================================

Player 2 made the move: (6, 6) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x -  - x x  - - o

- - x  o - -  o - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (5, 2) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o - -  o - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 2 made the move: (6, 4) with o
=========== Game Board ===========
- - -  - - -  x - -
- - -  - x -  - - -
- - x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (0, 1) with x
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  - - -
- - x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 2 made the move: (2, 1) with o
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  - - -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
- - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (7, 0) with x
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  - - -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
x - -  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 2 made the move: (7, 2) with o
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  - - -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
x - o  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (1, 6) with x
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  x - -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
x - o  - x -  o - -
- - -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 2 made the move: (8, 1) with o
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  x - -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- - x  o o -  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (6, 1) with x
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  x - -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- x x  o o -  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 2 made the move: (1, 7) with o
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  x o -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  - - -  - o -
- x x  - x x  - - o

- x x  o o -  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (4, 3) with x
=========== Game Board ===========
- x -  - - -  x - -
- - -  - x -  x o -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  x - -  - o -
- x x  - x x  - - o

- x x  o o -  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 2 made the move: (1, 1) with o
=========== Game Board ===========
- x -  - - -  x - -
- o -  - x -  x o -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  x - -  - o -
- x x  - x x  - - o

- x x  o o -  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- - o
- - o
==================================

Player 1 made the move: (5, 3) with x
=========== Game Board ===========
- x -  - - -  x - -
- o -  - x -  x o -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  x - -  - o -
- x x  x x x  - - o

- x x  o o -  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- x o
- - o
==================================

Player 2 made the move: (6, 5) with o
=========== Game Board ===========
- x -  - - -  x - -
- o -  - x -  x o -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  x - -  - o -
- x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- x o
- o o
==================================

Player 1 made the move: (0, 5) with x
=========== Game Board ===========
- x -  - - x  x - -
- o -  - x -  x o -
- o x  - x -  - - -

x - -  o o -  o - -
o o -  x - -  - o -
- x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- x o
- o o
==================================

Player 2 made the move: (2, 3) with o
=========== Game Board ===========
- x -  - - x  x - -
- o -  - x -  x o -
- o x  o x -  - - -

x - -  o o -  o - -
o o -  x - -  - o -
- x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- x o
- o o
==================================

Player 1 made the move: (4, 2) with x
=========== Game Board ===========
- x -  - - x  x - -
- o -  - x -  x o -
- o x  o x -  - - -

x - -  o o -  o - -
o o x  x - -  - o -
- x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- x o
- o o
==================================

Player 2 made the move: (2, 6) with o
=========== Game Board ===========
- x -  - - x  x - -
- o -  - x -  x o -
- o x  o x -  o - -

x - -  o o -  o - -
o o x  x - -  - o -
- x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
- x o
- o o
==================================

Player 1 made the move: (5, 0) with x
=========== Game Board ===========
- x -  - - x  x - -
- o -  - x -  x o -
- o x  o x -  o - -

x - -  o o -  o - -
o o x  x - -  - o -
x x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - -
x x o
- o o
==================================

Player 2 made the move: (0, 8) with o
=========== Game Board ===========
- x -  - - x  x - o
- o -  - x -  x o -
- o x  o x -  o - -

x - -  o o -  o - -
o o x  x - -  - o -
x x x  x x x  - - o

- x x  o o o  o - -
x - o  - x -  o - -
- o -  - - x  o - -
==================================
=========== Block Status =========
- - o
x x o
- o o
==================================

P2
COMPLETE

"""