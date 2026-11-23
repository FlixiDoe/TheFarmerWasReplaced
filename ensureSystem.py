def plotIsAvailable():
	entity = get_entity_type()
	return entity == None or entity == Entities.Grass or entity == Entities.Dead_Pumpkin


def ensureSoil():
	if not plotIsAvailable():
		return False
	if (get_ground_type() != Grounds.Soil):
		till()
	return True

def ensureGround():
	if not plotIsAvailable():
		return False
	if (get_ground_type() == Grounds.Soil):
		till()
	return True
