import helpers
import ressurceSystem
import needSystem

isTree=False

def plantGrass():
	helpers.entitiyIsUnlocked(Unlocks.Grass)
	helpers.ensureGround()
	plant(Entities.Grass)

def plantCarrot():
	helpers.entitiyIsUnlocked(Unlocks.Carrots)
	if (ressurceSystem.carrotRessurces()):
		helpers.ensureSoil()
		plant(Entities.Carrot)
	else:
		plantGrass()

def plantPumpkin():
	helpers.entitiyIsUnlocked(Unlocks.Pumpkins)
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
	helpers.entitiyIsUnlocked(Unlocks.Trees)
	global isTree
	helpers.ensureGround()
	if (isTree):
		plant(Entities.Bush)
		isTree = False
	else:
		plant(Entities.Tree)
		isTree = True
		

def plantSunflower():
	helpers.entitiyIsUnlocked(Unlocks.Sunflowers)
	print("TODO")