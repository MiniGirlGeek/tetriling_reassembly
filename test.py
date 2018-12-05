from copy import deepcopy
import utils

tetronimos = [0] + [utils.generate_shape(x) for x in range(1, 20)]

def calc_coord_scores(target, x, y):
	neighbors = [       [-1, 0],
				 [0, -1],       [0, 1],
				         [1, 0]        ]

	score = 0

	coords_to_check = [                  (0, 0), (0, 1), (0, 2), (0, 3),
					   (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
					            (2, -1), (2, 0), (2, 1),
					                     (3, 0)]
	coord_scores = {}


	checked_coords = []
	for coord_mod in coords_to_check:
		score = 0
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
							score += 1
						'''else:
							check_valid(shapeID, y, x, check_y, check_x, tetronimos, target)'''
					except IndexError:
						score += 1
				coord_scores[coord_mod] = score
		except IndexError:
			break
	return coord_scores

test_grid = [[0, 0, 1, 1, 1, 0],
			 [1, 1, 1, 0, 0, 0],
			 [0, 0, 1, 0, 1, 0],
			 [0, 1, 1, 0, 1, 1],
			 [0, 1, 1, 1, 0, 1],
			 [0, 0, 0, 0, 1, 0]]

print(calc_coord_scores(test_grid, 2, 0))

def score_fit(shapeID, tetronimos, coord_scores):
	score = 0
	i = 0
	for coord_mod in tetronimos[shapeID]:
		i += 1
		if tuple(coord_mod) in coord_scores:
			score += coord_scores[tuple(coord_mod)]
		else:
			return 0
	return score

coord_scores = calc_coord_scores(test_grid, 2, 0)
for shapeID in range(1, 20):
	print(f'{shapeID}: {score_fit(shapeID, tetronimos, coord_scores)}')

