def needsWater():
	
	if (get_water() < 1 and num_items(Items.Water) >= 1):
		use_item(Items.Water)
		

def needsFetrtilizer():
	if (num_items(Items.Fertilizer) >= 1):
		use_item(Items.Fertilizer)
		
