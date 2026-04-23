import HarvestSystem
import plantSystem
import placeSystem


def startMove():
	for i in range(get_world_size()):
		HarvestSystem.normalHarvet()

		x = get_pos_x()

		
		if (x == 0 or x == 10 or x== 13 or x==15):
			plantSystem.plantTree()
		elif (x == 1 or x == 8 or x == 9 or x==12 or x==14 ):
			plantSystem.plantCarrot()
		elif (x == 3 or x == 4 or x == 5 or x == 6 or x == 7):
			placeSystem.PumkinPlace(5)
	
		elif (x==2):
			plantSystem.plantSunflower()
		else:
			plantSystem.plantGrass()

		move(North)

	move(East)

def skipLinesForDebug(lines):
		for i in range(lines):
			move(East)