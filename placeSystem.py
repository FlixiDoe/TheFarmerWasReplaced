import plantSystem

def PumkinPlace(size):
	pumkinBlock = get_pos_y()
	maximum = get_world_size()
	block = size + 1
	numrowsgone = (maximum % block)

	if ((pumkinBlock % block == size) or pumkinBlock >= maximum - numrowsgone):
		plantSystem.plantGrass()
	else:
		plantSystem.plantPumpkin()