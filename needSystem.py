import unlockSystem

def needsWater():
	if (unlockSystem.ItemIsUnlocked(Unlocks.Watering)):
		if (get_water() < 1 and num_items(Items.Water) >= 1):
			use_item(Items.Water)
		

def needsFetrtilizer():
	if (unlockSystem.ItemIsUnlocked(Unlocks.Fertilizer)):
		if (num_items(Items.Fertilizer) >= 1):
			use_item(Items.Fertilizer)
		
