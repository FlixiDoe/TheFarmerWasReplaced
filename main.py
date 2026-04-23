clear()
change_hat(Hats.Wizard_Hat)
carrotCosts= [-1, -1]
pumkinCosts= [-1]
isTree=False	

def setCosts():
	setCarrotCosts()
	setPumkinCosts()


def setCarrotCosts():
	global carrotCosts
	costs= get_cost(Entities.Carrot)
	carrotCosts[0]= costs[Items.Hay]
	carrotCosts[1]= costs[Items.Wood]

def setPumkinCosts():
	global pumkinCosts
	costs= get_cost(Entities.Pumpkin)

	pumkinCosts[0]= costs[Items.Carrot]
isTree=False	
def carrotRessurces():
	if (num_items(Items.Hay) >= carrotCosts[0] and num_items(Items.Wood) >= carrotCosts[1]):
		return True
	else:
		return False

def pumpkinRessurces():
	if (num_items(Items.Carrot) >= pumkinCosts[0]):
		return True
	else:
		return False

def ensureSoil():
	if (get_ground_type() != Grounds.Soil):
		till()

def ensureGround():
	if (get_ground_type() == Grounds.Soil):
		till()

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
			needsWater()
			plant(Entities.Pumpkin)
			
			#needsFetrtilizer()
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
	pumkinBlock = get_pos_y()
	maximum = get_world_size()
	block = size + 1
	numrowsgone = (maximum % block)

	if ((pumkinBlock % block == size) or pumkinBlock >= maximum - numrowsgone):
		plantGrass()
	else:
		plantPumpkin()


def needsWater():
	if (get_water() < 1 and num_items(Items.Water) >= 1):
		use_item(Items.Water)

def skipRows(rows):
	for i in range(rows):
		move(East)

def needsFetrtilizer():
	if (num_items(Items.Fertilizer) >= 1):
		use_item(Items.Fertilizer)

def plantSunflower():
	print("TODO")
##skipRows(3)
while True:
	setCosts()
	for i in range(get_world_size()):
		
		if (can_harvest()):
			harvest()

		x = get_pos_x()

		if (x == 0 or x == 11):
			plantGrass()
		elif (x == 1 or x == 10 or x== 13 or x==15):
			TreePflanzen()
		elif (x == 2 or x == 8 or x == 9 or x==12 or x==14 ):
			plantCarrot()
		elif (x == 3 or x == 4 or x == 5 or x == 6 or x == 7):
			PumkinPlace(5)
	
	
		else:
			plantGrass()

		move(North)

	move(East)