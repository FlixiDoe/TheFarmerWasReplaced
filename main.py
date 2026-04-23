clear()
change_hat(Hats.Wizard_Hat)


isTree=False	
def carrotRessurces():
	if (num_items(Items.Hay) >= 32 and num_items(Items.Wood) >= 32):
		return True
	else:
		return False

def pumpkinRessurces():
	if (num_items(Items.Carrot) >= 1):
		return True
	else:
		return False

def ensureSoil():
	if (get_ground_type() != Grounds.Soil):
		till()

def ensureGround():
	if (get_ground_type() == Grounds.Soil):
		untill()

def plantGrass():
	ensureGround()
	plant(Entities.Grass)

def plantCarrot():
	if (carrotRessurces()):
		ensureSoil()
		plant(Entities.Carrot)
	else:
		plantGrass()

def plantPumpkin():
	if (pumpkinRessurces()):
		ensureSoil()
		plant(Entities.Pumpkin)
		i = 0
		while not can_harvest():

			plant(Entities.Pumpkin)
			needsWater()
			#print(i)
		#i += 1
			

	else:
		plantGrass()

def TreePflanzen():
	global isTree
	ensureGround()
	if (isTree):
		plant(Entities.Bush)
		isTree = False
	else:
		plant(Entities.Tree)
		isTree = True

def PumkinPlace(size):
	size = size +1
	pumkinBlock = get_pos_y()
	maximum = get_world_size()
	numrowsgone = (maximum % size )

	if(get_pos_y()==0):
		pumkinBlock= pumkinBlock+1
	
	#if(get_pos_y())<6:
	#	pumkinBlock= pumkinBlock-1
		#if ((pumkinBlock % size == 0 ) or pumkinBlock >= maximum - numrowsgone):
			#plantGrass()
		#else:
		#	plantPumpkin()

	#else:
	if ((pumkinBlock % size == 0 ) or pumkinBlock >= maximum - numrowsgone):
		plantGrass()
	else:
		plantPumpkin()


def needsWater():
	if (get_water() < 0.5 and num_items(Items.Water) >= 1):
		use_item(Items.Water)

def skipRows(rows):
	for i in range(rows):
		move(East)


skipRows(3)
while True:
	for i in range(get_world_size()):
		

		if (can_harvest()):
			harvest()

		x = get_pos_x()

		if (x == 0 or x == 11):
			plantGrass()
		elif (x == 1 or x == 10):
			TreePflanzen()
		elif (x == 2 or x == 8 or x == 9):
			plantCarrot()
		elif (x == 3 or x == 4 or x == 5 or x == 6 or x == 7):
			PumkinPlace(5)

		move(North)

	move(East)

#get_entity_type