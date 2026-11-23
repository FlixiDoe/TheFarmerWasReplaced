carrotCosts= [-1, -1]
pumkinCosts= [-1]
sunflowerCosts = [-1]


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

def setSunflowerCosts():
	global sunflowerCosts
	costs= get_cost(Entities.Sunflower)
	sunflowerCosts[0]= costs[Items.Carrot]
