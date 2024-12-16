extends Node

func _init() -> void:
	var parameter = preload("res://Resources/parameters.gd").new()
	self.x_size = parameter.GRID_X_SIZE
	self.y_size = parameter.GRID_Y_SIZE
	self.grid = build_grid()

func build_grid() -> Array:
	var grid := []
	for y in range(self.y_size):
		var row := []
		for x in range(self.x_size):
			row.append({})  # Add an empty dictionary for each cell
			grid.append(row)  # Add the row to the grid
	return grid
	
func get_neighbors(x:int, y:int) -> Array:
	var neighbors = []
	
	#top-left
	if x==0 and y==0:
		neighbors = [[0,1],[1,0],[1,1]]
	#botton-left
	elif x==0 and y==self.y_size:
		neighbors = [[0, self.y_size - 2], [1, self.y_size - 2], [1, self.y_size - 1]]
	# Top-right corner
	elif x == self.x_size - 1 and y == 0:
		neighbors = [[self.x_size - 2, 0], [self.x_size - 2, 1], [self.x_size - 1, 1]]
	# Bottom-right corner
	elif x == self.x_size - 1 and y == self.y_size - 1:
		neighbors = [[self.x_size - 1, self.y_size - 2], [self.x_size - 2, self.y_size - 2], [self.x_size - 2, self.y_size - 1]]
	# Left edge (not corners)
	elif x == 0:
		for ix in range(0, 2):
			for iy in range(-1, 2):
				if not (ix == 0 and iy == 0):
					neighbors.append([x + ix, y + iy])
	# Top edge (not corners)
	elif y == 0:
		for ix in range(-1, 2):
			for iy in range(0, 2):
				if not (ix == 0 and iy == 0):
					neighbors.append([x + ix, y + iy])
	# Default case: all surrounding cells
	else:
		for ix in range(-1, 2):
			for iy in range(-1, 2):
				if not (ix == 0 and iy == 0):
					neighbors.append([x + ix, y + iy])            
	return neighbors
