import helpers
import ressurceSystem
import needSystem
import unlockSystem
import ensureSystem

isTree=False

def plantGrass():
	if ensureSystem.ensureGround():
		plant(Entities.Grass)

def plantCarrot():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Carrots)):
		if (ressurceSystem.carrotRessurces()):
			if ensureSystem.ensureSoil():
				plant(Entities.Carrot)
		else:
			plantGrass()

def plantPumpkin():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Pumpkins)):
		if get_entity_type() == Entities.Pumpkin:
			if not can_harvest():
				needSystem.needsWater()
		elif (ressurceSystem.pumpkinRessurces()):
			if ensureSystem.ensureSoil() and plant(Entities.Pumpkin):
				needSystem.needsWater()
		else:
			plantGrass()

def plantTree():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Trees)):
		global isTree
		if ensureSystem.ensureGround():
			if isTree:
				plant(Entities.Bush)
			else:
				plant(Entities.Tree)
		isTree = not isTree
		

def plantSunflower():
	if(unlockSystem.entitiyIsUnlocked(Unlocks.Sunflowers)):
		if (ressurceSystem.SunflowerRessurces()):
			if ensureSystem.ensureSoil():
				#change_hat(Hats.Brown_Hat)
				plant(Entities.Sunflower)
				## messung welche energie es hat muss hier rein
		else:
			plantGrass()
