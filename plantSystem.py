import helpers
import ressurceSystem
import needSystem
import unlockSystem

isTree=False

def plantGrass():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Grass)):
		helpers.ensureGround()
		plant(Entities.Grass)

def plantCarrot():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Carrots)):
		if (ressurceSystem.carrotRessurces()):
			helpers.ensureSoil()
			plant(Entities.Carrot)
		else:
			plantGrass()

def plantPumpkin():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Pumpkins)):
		if (ressurceSystem.pumpkinRessurces()):
			helpers.ensureSoil()
			plant(Entities.Pumpkin)
			while not can_harvest():
				needSystem.needsWater()
				plant(Entities.Pumpkin)
			
			#needsFetrtilizer()
		else:
			plantGrass()

def plantTree():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Trees)):
		global isTree
		helpers.ensureGround()
		if (isTree):
			plant(Entities.Bush)
			isTree = False
		else:
			plant(Entities.Tree)
			isTree = True
		

def plantSunflower():
	if(unlockSystem.entitiyIsUnlocked):
		helpers.entitiyIsUnlocked(Unlocks.Sunflowers)
		print("TODO")