def normalHarvet():
	if(get_entity_type()==Entities.Sunflower):
		return
	else:
		if (can_harvest()):
			harvest()
	