import plantSystem
def ensureSoil():
	if (get_ground_type() != Grounds.Soil):
		till()

def ensureGround():
	if (get_ground_type() == Grounds.Soil):
		till()

def skipRows(rows):
	for i in range(rows):
		move(East)
		
def entitiyIsUnlocked(unlockedItem):
	if (num_unlocked(unlockedItem) >=1):
		return True
	else:
		print("not unlocked")
		plantSystem.plantGrass()
		return False
	
	