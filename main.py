clear()
change_hat(Hats.Wizard_Hat)

isTree = False

def carrotRessurces():
    if (num_items(Items.Hay) >= 1 and num_items(Items.Wood) >= 1):
        return True
    else:
        return False
            
def pumpkinRessurces():
    if (num_items(Items.Carrot) >= 1):
        return True 
    else:
        return False
                
def plantWithTill(Entity):
    if (get_ground_type() != Grounds.Soil):
        till()
    plant(Entity)
                
def plantWithRessurces(Entity):
    if (Entity == Entities.Carrot):
        if (carrotRessurces()):
            plantWithTill(Entity)
        else:
            plant(Entities.Grass)
            
    if (Entity == Entities.Pumpkin): 
        if (pumpkinRessurces()):
            plantWithTill(Entity)
        else:
            plant(Entities.Grass)

def TreePflanzen():
    global isTree
    if (isTree):
        plant(Entities.Bush)
        isTree = False
    else:
        plant(Entities.Tree)
        isTree = True

while True:
    for i in range(get_world_size()):
        # Bewässerung
        if (get_water() < 0.5 and num_items(Items.Water) >= 1):
            use_item(Items.Water)   
        
        if (can_harvest()):
            harvest()
            
        x = get_pos_x()
        
        if (x == 0):
            plant(Entities.Grass)
        elif (x == 1 or x == 3 or x == 7):
            TreePflanzen()
        elif (x == 2):
            plantWithRessurces(Entities.Carrot)
        elif (x == 4 or x == 5 or x == 6):
            plantWithRessurces(Entities.Pumpkin)

        move(North) 
        
    move(East)