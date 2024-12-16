extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var grid_object = preload("res://Scripts/grid.gd").new()
	var parameter = preload("res://Resources/parameters.gd").new()
	
	grid_object._init()
	self.mutation_chance = parameter.PLANT_MUTATION_CHANCE
	self.death_chance = parameter.PLANT_DEATH_CHANCE
	self.mitosis_chance = parameter.PLANT_MITOSIS_CHANCE
	
	draw_rect(Rect2())
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
