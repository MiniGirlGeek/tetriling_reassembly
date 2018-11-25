# ################################ #
# DE2-COM2 Computing 2             #
# Individual project               #
#                                  #
# Title: MAIN                      #
# Authors: Amy Mather              #
# Last updated: 15th November 2018 #
# ################################ #


from copy import deepcopy
import utils

def score_fit(target, x, y, shapeID, tetronimos):
	neighbors = [       [-1, 0],
				 [0, -1],       [0, 1],
				         [1, 0]        ]

	score = 0

	checked_coords = []

	for coord_mod in tetronimos[shapeID]:
		y_mod, x_mod = coord_mod
		cur_y = y + y_mod
		cur_x = x + x_mod
		try:
			if (cur_x < 0 ) or (cur_y < 0):
				raise IndexError
			if target[cur_y][cur_x]:
				for neighbor in neighbors:
					try:
						check_y, check_x = cur_y + neighbor[0], cur_x + neighbor[1]
						if not target[check_y][check_x]:
							if (check_y, check_x) not in checked_coords:
								score += 1
								checked_coords.append((check_y, check_x))
						else:
							check_valid(check_y, check_x)
					except IndexError:
						if (check_y, check_x) not in checked_coords:
							score += 1
							checked_coords.append((check_y, check_x))
			else:
				return 0
		except IndexError:
			return 0
	return score

def check_valid(y, x):
	return True

def score(result):
	return result[1]

def place(shapeID, x, y, solution_matrix, pieceID, tetronimos, target, limit_tetris):
	for coord_mod in tetronimos[shapeID]:
		cur_y = y + coord_mod[0]
		cur_x = x + coord_mod[1]
		solution_matrix[cur_y][cur_x] = (shapeID, pieceID)
		target[cur_y][cur_x] = 0
	limit_tetris[shapeID] -= 1
	return pieceID + 1


def Tetris(target, limit_tetris):
	#tetris_priority = [set(range(3, 16)), {2, 3, 16, 17, 18, 19}, {1}]
	tetronimos = [0] + [utils.generate_shape(x) for x in range(1, 20)]

	solution_matrix = deepcopy(target)

	for y in range(len(solution_matrix)):
		for x in range(len(solution_matrix[y])):
			if not solution_matrix[y][x]:
				solution_matrix[y][x] = (0, 0)
	pieceID = 1

	for y in range(len(target)):
		for x in range(len(target[y])):
			if target[y][x]:
				results = []
				for shapeID in limit_tetris:
					if limit_tetris[shapeID] > 0:
						results.append((shapeID, score_fit(target, x, y, shapeID, tetronimos)))
				results.sort(key=score)
				try:
					selected = results.pop()
					if selected[1]:
						pieceID = place(selected[0], x, y, solution_matrix, pieceID, tetronimos, target, limit_tetris)
				except IndexError:
					pass

	for y in range(len(solution_matrix)):
		for x in range(len(solution_matrix[y])):
			if solution_matrix[y][x] == 1:
				solution_matrix[y][x] = (0, 0)

	return solution_matrix
'''def find_subgraphs(target):
	graph = taget.deepcopy()
	connected = [[0, -1], [-1, 0], [1, 0], [0, 1]]
	for y in len(graph):
		for x in len(graph[y]):'''

