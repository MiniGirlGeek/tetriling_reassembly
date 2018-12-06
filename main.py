# ################################ #
# DE2-COM2 Computing 2             #
# Individual project               #
#                                  #
# Title: MAIN                      #
# Authors: Amy Mather              #
# Last updated: 4th December 2018 #
# ################################ #


from copy import deepcopy
import utils

def calc_coord_scores(target, x, y):
	'''gives the squares that could have a tetris piece placed upon them a score
	   the score represents how many sides are adjacent to the puzzle boundary'''

	width = len(target[0]) # The width of the target matrix
	height = len(target)   # The height of the target matrix

	# The coordinates to check for adjaceny
	neighbors = [       [-1, 0],
				 [0, -1],       [0, 1],
				         [1, 0]        ]

	# How many edges are adjacent
	score = 0

	# A pictorial representation of all the tetris pieces on top of one another

	#          # # # #
	#      # # # # #
	#        # # #
	#          #

	# every possible relative coordinate a tetris piece could have - this is to save
	# calculating the score for the same coordinate multiple times which would
	# occur if cycling through the coords of each tetris shape

	# coordinates are represented (y, x)

	coords_to_check = [                  (0, 0), (0, 1), (0, 2), (0, 3),
					   (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
					            (2, -1), (2, 0), (2, 1),
					                     (3, 0)]
	
	# uses a tuple contaiing the coordiates (y, x) as a key, keeps track of each coordinates score
	coord_scores = {}

	for coord_mod in coords_to_check:
		score = 0
		y_mod, x_mod = coord_mod
		cur_y = y + y_mod
		cur_x = x + x_mod
		if (cur_x >= 0 ) and (cur_y >= 0) and (cur_x < width) and (cur_y < height):
			if target[cur_y][cur_x]:
				for neighbor in neighbors:
					check_y, check_x = cur_y + neighbor[0], cur_x + neighbor[1]
					if (check_x > 0 ) and (check_y > 0) and (check_x < width) and (check_y < height):
						if not target[check_y][check_x]:
							score += 1
					else:
						score += 1
				coord_scores[coord_mod] = score
	return coord_scores

def score_fit(shapeID, tetronimos, coord_scores):
	''' uses the coordinate scores to calculate how snugly a piece fits
	    the higher the score, the snugger the fit'''
	score = 0
	i = 0
	for coord_mod in tetronimos[shapeID]:
		i += 1
		if tuple(coord_mod) in coord_scores:
			score += coord_scores[tuple(coord_mod)]
		else:
			return 0
	return score



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
	tetronimos = [0] + [utils.generate_shape(x) for x in range(1, 20)]

	width = len(target[0]) # The width of the target matrix
	height = len(target) 

	solution_matrix = deepcopy(target)
	total_shapes = 0
	for shape in limit_tetris:
		total_shapes += limit_tetris[shape]

	for y in range(len(solution_matrix)):
		for x in range(len(solution_matrix[y])):
			if not solution_matrix[y][x]:
				solution_matrix[y][x] = (0, 0)
	pieceID = 1


	for y in range(len(target)):
		for x in range(len(target[y])):
			if target[y][x]:
				biggest_score = 0
				best_shape = 0
				coord_scores = calc_coord_scores(target, x, y)
				if coord_scores != {}:
					results = []
					for shapeID in limit_tetris:
						if limit_tetris[shapeID] > 0:
							if total_shapes > 2500:
								weighting = (limit_tetris[shapeID] / total_shapes)
							else:
								weighting = 1
							weighting = (limit_tetris[shapeID] / total_shapes)
							shape_score = weighting * score_fit(shapeID, tetronimos, coord_scores)
							if shape_score > biggest_score:
								biggest_score = shape_score
								best_shape = shapeID
					if biggest_score > 0:
						pieceID = place(best_shape, x, y, solution_matrix, pieceID, tetronimos, target, limit_tetris)
						total_shapes -= 1
					else:
						solution_matrix[y][x] = (0, 0)
				else:
					solution_matrix[y][x] = (0, 0)

	#places an block
	for y in range(len(target)):
		for x in range(len(target[y])):
			if target[y][x]:
				for shapeID in limit_tetris:
					if limit_tetris[shapeID] > 0:
						covering = 0
						for coord_mod in tetronimos[shapeID]:
							new_y = y + coord_mod[0]
							new_x = x + coord_mod[1]
							if new_y >= 0 and new_x >= 0 and new_y < height and new_x < width:
								if target[new_y][new_x] and solution_matrix[new_y][new_x] == (0, 0):
									covering += 1
								if solution_matrix[new_y][new_x] != (0, 0):
									covering = 0
									break
							else:
								covering = 0
								break
						if covering >= 3:
							pieceID = place(shapeID, x, y, solution_matrix, pieceID, tetronimos, target, limit_tetris)
							break


	#print('\n'.join([' '.join([str(char) for char in row]) for row in solution_matrix]))
	return solution_matrix

