import helpers
import ressurceSystem
import needSystem

isTree=False

def plantGrass():
	helpers.ensureGround()
	plant(Entities.Grass)

def plantCarrot():
	if (ressurceSystem.carrotRessurces()):
		helpers.ensureSoil()
		plant(Entities.Carrot)
	else:
		plantGrass()

def plantPumpkin():
	if (ressurceSystem.pumpkinRessurces()):
		helpers.ensureSoil()
		plant(Entities.Pumpkin)
		i = 0
		while not can_harvest():
			needSystem.needsWater()
			plant(Entities.Pumpkin)
			
			#needsFetrtilizer()
	else:
		plantGrass()

def plantTree():
	global isTree
	helpers.ensureGround()
	if (isTree):
		plant(Entities.Bush)
		isTree = False
	else:
		plant(Entities.Tree)
		isTree = True
		

def plantSunflower():
	print("TODO")