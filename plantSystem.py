import helpers
import ressurceSystem
import needSystem
import unlockSystem
import ensureSystem

isTree=False

def plantGrass():
		ensureSystem.ensureGround()
		plant(Entities.Grass)

def plantCarrot():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Carrots)):
		if (ressurceSystem.carrotRessurces()):
			ensureSystem.ensureSoil()
			plant(Entities.Carrot)
		else:
			plantGrass()

def plantPumpkin():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Pumpkins)):
		if (ressurceSystem.pumpkinRessurces()):
			ensureSystem.ensureSoil()
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
		ensureSystem.ensureGround()
		if (isTree):
			plant(Entities.Bush)
			isTree = False
		else:
			plant(Entities.Tree)
			isTree = True
		

def plantSunflower():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Sunflowers)):
		if (ressurceSystem.SunflowerRessurces()):
			#change_hat(Hats.Brown_Hat)
			ensureSystem.ensureSoil()
			plant(Entities.Sunflower)
		else:
			plantGrass()
			