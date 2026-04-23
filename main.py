clear()
change_hat(Hats.Wizard_Hat)

isTree = False

def carrotRessurces():
	if (num_items(Items.Hay) >= 16 and num_items(Items.Wood) >= 16):
		return True
	else:
		return False

def pumpkinRessurces():
	if (num_items(Items.Carrot) >= 1):
		return True
	else:
		return False

def plantWithTill(entity):
	if (get_ground_type() != Grounds.Soil):
		till()
	plant(entity)

def plantGrassWithTill():
	if (get_ground_type() != Grounds.Soil):
		till()
		#
	plant(Entities.Carrot)

def plantCarrot():
	if (carrotRessurces()):
		if (get_ground_type() != Grounds.Soil):
			till()
		plant(Entities.Carrot)
	else:
		if (get_ground_type() != Grounds.Soil):
			till()
			#tmp
		plant(Entities.Carrot)

def plantPumpkin():
	if (pumpkinRessurces()):
		if (get_ground_type() != Grounds.Soil):
			till()
		plant(Entities.Pumpkin)
	else:
		if (get_ground_type() != Grounds.Soil):
			till()
		plant(Entities.Grass)

def TreePflanzen():
	global isTree
	if (isTree):
		plant(Entities.Bush)
		isTree = False
	else:
		plant(Entities.Tree)
		isTree = True

def PumkinPlace():
	pumkinBlock = get_pos_y()
	maximum = get_world_size()
	numrowsgone = maximum % 5

	if ((pumkinBlock % 5 == 0 and pumkinBlock != 0) or pumkinBlock > maximum - numrowsgone):
		plantGrassWithTill()
	else:
		plantPumpkin()

while True:
	for i in range(get_world_size()):
		if (get_water() < 0.5 and num_items(Items.Water) >= 1):
			use_item(Items.Water)

		if (can_harvest()):
			harvest()

		x = get_pos_x()

		if (x == 0 or x == 11):
			plantGrassWithTill()
		elif (x == 1 or x == 10):
			TreePflanzen()
		elif (x == 2 or x == 8 or x == 9):
			plantCarrot()
		elif (x == 3 or x == 4 or x == 5 or x == 6 or x == 7):
			PumkinPlace()

		move(North)

	move(East)