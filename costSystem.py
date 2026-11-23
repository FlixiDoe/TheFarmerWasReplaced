carrotCosts= [-1, -1]
pumkinCosts= [-1]
sunflowerCosts = None


def setCosts():
	if num_unlocked(Unlocks.Carrots) > 0:
		setCarrotCosts()
	if num_unlocked(Unlocks.Pumpkins) > 0:
		setPumkinCosts()
	if num_unlocked(Unlocks.Sunflowers) > 0:
		setSunflowerCosts()

def setCarrotCosts():
	global carrotCosts
	costs= get_cost(Entities.Carrot)
	carrotCosts[0]= costs[Items.Hay]
	carrotCosts[1]= costs[Items.Wood]
	

def setPumkinCosts():
	global pumkinCosts
	costs= get_cost(Entities.Pumpkin)

	pumkinCosts[0]= costs[Items.Carrot]

def setSunflowerCosts():
	global sunflowerCosts
	sunflowerCosts = get_cost(Entities.Sunflower)
