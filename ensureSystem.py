def ensureSoil():
	if (get_ground_type() != Grounds.Soil):
		till()

def ensureGround():
	if (get_ground_type() == Grounds.Soil):
		till()