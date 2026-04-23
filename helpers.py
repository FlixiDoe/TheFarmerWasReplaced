def ensureSoil():
	if (get_ground_type() != Grounds.Soil):
		till()

def ensureGround():
	if (get_ground_type() == Grounds.Soil):
		till()

def skipRows(rows):
	for i in range(rows):
		move(East)