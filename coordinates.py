X = 0
Y = 1

def invalid_coordinates(coordinates, upper_bound):
	return coordinates[X] < 0 or coordinates[X] >= upper_bound or coordinates[Y] < 0 or coordinates[Y] >= upper_bound