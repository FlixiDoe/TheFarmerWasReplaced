clear()
change_hat(Hats.Wizard_Hat)



while True:
	for i in range(get_world_size() ):
		if (get_water() < 0.5 and num_items(Items.Water)>=1):
			use_item(Items.Water)	
		harvest()
		if(get_pos_x()==0):
			plant(Entities.Grass)
		elif(get_pos_x()==1 or get_pos_x() == 2 or get_pos_x() ==7  ):
			
			plant(Entities.Bush)
			
		elif(get_pos_x()==3  ):
			plantWithRessurces(Entities.Carrot)

		elif(get_pos_x()==4 or get_pos_x()==5 or get_pos_x()==6 or get_pos_x()==5  ):
			plantWithRessurces(Entities.Pumpkin)
		move(North)	
	move(East)
	def carrotRessurces():
		if (num_items(Items.Hay) >= 1 and num_items(Items.Wood)>=1):
			return True
		else:
			return False
			
	def pumpkinRessurces():
		if (num_items(Items.Carrot) >= 1 ):
			return True	
		else:
			return False
			
			
				
	def plantWithTill(Entitiy):
		
			if (get_ground_type() != Grounds.Soil):
				till()
				plant(Entitiy)
			else:
				plant(Entitiy)
		
				
				
	def plantWithRessurces(Entitiy):
		if (Entitiy== Entities.Carrot):
			if(carrotRessurces()):
				plantWithTill(Entitiy)
			else:
				plant(Entities.Grass)
		if (Entitiy==Entities.Pumpkin):
			if(pumpkinRessurces()):
				plantWithTill(Entitiy)
			else:
				plant(Entities.Grass)
			