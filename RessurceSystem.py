import costSystem

def pumpkinRessurces():
	if (num_items(Items.Carrot) >= costSystem.pumkinCosts[0]):
		return True
	else:
		return False
	

def carrotRessurces():
	if (num_items(Items.Hay) >= costSystem.carrotCosts[0] and num_items(Items.Wood) >= costSystem.carrotCosts[1]):
		return True
	else:
		return False