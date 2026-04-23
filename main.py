import costSystem
import movingSystem
clear()
change_hat(Hats.Wizard_Hat)

	
while True:
	movingSystem.skipLinesForDebug(2)
	costSystem.setCosts()
	movingSystem.startMove()

