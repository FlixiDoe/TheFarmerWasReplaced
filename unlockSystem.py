import plantSystem

def ItemIsUnlocked(unlockedItem):
	if (num_unlocked(unlockedItem) >=1):
		return True
	else:
		return False
	

def entitiyIsUnlocked(unlockedItem):
	if (num_unlocked(unlockedItem) >=1):
		return True
	else:
		plantSystem.plantGrass()
		return False
	
	