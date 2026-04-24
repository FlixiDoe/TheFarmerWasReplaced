import costSystem
import movingSystem
import plantSystem
import placeSystem


def seedGame():
	world_size = get_world_size()

	costSystem.setCosts()

	for column in range(world_size):
		for row in range(world_size):
			seedCurrentTile()
			if (row < world_size - 1):
				move(North)

		if (column < world_size - 1):
			moveToSouthEdge()
			move(East)

	resetPosition()
	movingSystem.move_north = True


def seedCurrentTile():
	x = get_pos_x()
	if (x == 2 or x == 10 or x == 13 or x == 15):
		plantSystem.plantTree()
	elif (x == 1 or x == 8 or x == 9 or x == 12 or x == 14):
		plantSystem.plantCarrot()
	elif (x == 3 or x == 4 or x == 5 or x == 6 or x == 7):
		placeSystem.PumkinPlace(5)
	else:
		plantSystem.plantGrass()


def resetPosition():
	moveToSouthEdge()

	for i in range(get_pos_x()):
		move(West)


def moveToSouthEdge():
	while (get_pos_y() != 0):
		move(South)
