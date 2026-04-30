def normalHarvet():
	if(get_entity_type()==Entities.Sunflower):
		return
	else:
		if (can_harvest()):
			#print("asdfvg")
			harvest()

def sunflowwerHarvest():
		if(SunnflowerIsMax):
			harvest()
		else:
			do_a_flip()


def SunnflowerIsMax():
	if(measure()==15):
		return True
	else:
		return False

