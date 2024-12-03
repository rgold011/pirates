
import game.display as display
from game import location
import game.config as config
import game.combat as combat
import game.items as item
import game.event as event
import random




class rgold011_ISLAND(location.Location):
    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["Beach_In_Cove"] = Beach_In_Cove(self)
        self.locations["Beach_Abandoned_Tower"] = Beach_Abandoned_Tower(self)
        self.locations["Tower"] = Tower(self)
        self.locations['Dark_Cave'] = Dark_Cave(self)
        self.locations["Glade"] = Glade(self)
        self.locations['Coconut_Tree_Beach'] = Coconut_Tree_Beach(self)
        self.locations['Great_Temple_Forest'] = Great_Temple_Forest(self)
        self.locations['Great_Temple'] = Great_Temple(self)
        

        
        self.starting_location = self.locations["Beach_In_Cove"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

##############################
########## LOCATION ##########
##############################

# The Beach in the cove will be the starting location for RG island. 
class Beach_In_Cove (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
      
        
    def enter (self):
        display.announce ("You arrived at the RG Island. You dock your ship in a small cove, in the south of the island. There is a cave to the west, a beach with a tower to the east, and a forest to the north")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations["Great_Temple_Forest"]
            display.announce ("You travel North into the island. You approach a forest. There is a temple. ")
        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations["Dark_Cave"]
            display.announce("You travel west towards a cave.")
        elif (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations["Beach_Abandoned_Tower"]
            display.announce("You travel east along the beach, towards a tower.")
###############################################
##### SUBLOCATIONS AND SUPPORTING CLASSES #####
###############################################

class Temple_Sentinel(combat.Monster): #'boss' enemy
    def __init__(self, name):
        attacks = {}
        attacks['beam'] = ['beam attack', random.randrange(80,100), (15, 25)]
        attacks['smash'] = ['smash', random.randrange(25,100), (10,20)]
        super().__init__(name, random.randrange(100,150), attacks, 100 + random.randrange(-30,30))
        self.type_name = "Temple Sentinel"

class Giant_Bat(combat.Monster):  
    def __init__(self, name):
        attacks = {}
        attacks['bite'] = ["bites", random.randrange(50, 100), (5, 15)]  #First set is range of combat accuracy, generated when the enemy is created. The second is range of damage the attack does.
        attacks['hit'] = ["hits", random.randrange(75, 80), (2,10)]
        super().__init__(name, random.randrange(7,20), attacks, 100 + random.randrange(-10, 50)) #1st, number of HP, 2nd, range of speed/
        self.type_name = "Giant Bat"
class Musket(item.Item): 
    def __init__(self):
        super().__init__('musket', 500) #500 is the value in shillings, total value of all treasure is generated at the end of the game.
        self.damage = (80,120)
        self.firearm = True
        self.charges = 1
        self.skill = 'guns'
        self.verb = 'shoot'
        self.verb2 = 'shoots'

class Feberge_Egg(item.Item):
    def __init__ (self):
        super().__init__('Feberge Egg', 2500)
class Sentinel_Mace(item.Item):
    def __init__(self):
        super().__init__('Sentinel-Mace', 1000)
        self.damage = (100)
        self.skill = 'bludgeons'
        self.verb = 'hit'
        self.verb2 = 'hits'

class Giant_Bat_Attack (event.Event):
    petemade = False
    def __init__ (self):
        self.name = "Giant Bat Attack"
    def process (self, world):
        result = {}
        result["message"] = 'Giant bat is defeated...'
        monsters = []
        n_appearing = random.randrange(1,2)
        n = 1
        while n <= n_appearing:
            monsters.append(Giant_Bat('Giant Bat'+str(n)))
            n += 1
        display.announce('You are being attacked by a giant bat')
        combat.Combat(monsters).combat()
        if random.randrange(2) == 0:
            result['newevents'] = [ self ]
        else:
            result['newevents'] = [ ]
        config.the_player.ship.food += n_appearing*4

        return result
class Temple_Sentinel_Attack(event.Event):
    petemade = False
    def __init__ (self):
        self.name = "Temple Sentinel Attack"
    def process (self, world):
        result = {}
        result['message'] = "Temple Sentinel is defeated..."
        monsters = []
        n_appearing = 1
        n = 1
        while n <= n_appearing:
            monsters.append(Temple_Sentinel('Temple Sentinel'+str(n)))
            n += 1
        display.announce('A Temple Sentinel has awoken!')
        combat.Combat(monsters).combat()
     
        result['newevents'] = [ ]

        weapon_gained = Sentinel_Mace()
        config.the_player.add_to_inventory([weapon_gained])
        display.announce('You pick up the weapon the temple sentinel was using... "Sentinel-Mace"')
        return result
class Coconuts(event.Event):
    petemade = False
    def __init__ (self):
        self.name = 'Coconut Collection'
    def process(self, world):
        result = {}
        n_appearing = random.randrange(5,25)
        msg = f"There are {n_appearing} coconuts on this beach, a good souce of food!"
        config.the_player.ship.food += n_appearing
        result["message"] = msg
        result["newevents"] = [ self ]
        return result


 #Abondoned Tower beach will be East of the starting cove. You can enter the tower, or go back.      
class Beach_Abandoned_Tower (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Abandoned Tower Beach"
        self.verbs['west'] = self
        self.verbs['enter'] = self
    def enter (self): 
        display.announce ("You arrive at a beach with an abandoned tower; what could be inside?")
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Beach_In_Cove"]
            display.announce ("You travel back to the cove.")
        elif (verb == 'enter'):
            config.the_player.next_loc = self.main_location.locations["Tower"]


# the tower will have an item to collect, and also a 100% guarentee of an enemy attacking you. 
class Tower (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Abandoned Tower"
        self.verbs['exit'] = self
        self.verbs['take'] = self
        self.item_in_tower = Musket()
        self.event_chance = 50
        self.events.append(Giant_Bat_Attack())
    def enter (self):
        display.announce ("You walk inside the tower, there is a musket racked on the wall.")
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'exit'):
            config.the_player.next_loc = self.main_location.locations['Beach_Abandoned_Tower']
            config.the_player.go = True
            display.announce ('You exit the tower and return the Tower Beach')
        elif (verb == 'take'):
            if self.item_in_tower == None:
                display.announce ("There is not anything to take")
            elif len(cmd_list) > 1:
                at_least_one = False
                item = self.item_in_tower
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == 'all'):
                    display.announce (f'You pick up the {item.name} from its rack')
                    config.the_player.add_to_inventory([item])
                    self.item_in_tower = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce('What? Nothing there')






# Dark Cave will be to the west of the starting cove. There will be a puzzle, resulting in unlucky (damage) or lucky (proceed to glade sublocation)
class Dark_Cave (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Dark Cave"
        self.verbs = ['exit']
    def enter(self):
        display.announce("You enter the cave. PUZZLE OPTION")
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit"):
            config.the_player.next_loc = self.main_location.locations['Beach_In_Cove']
            config.the_player.go = True
            display.announce('You exit the cave and travel back to the cove')
#The Glade will only be acessible if you beat the cave puzzle. It will contain an exclusive treasure/food.
class Glade (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Glade"
        self.verbs = ['exit']
    def enter(self):
        display.announce('You slide out of the cave, and into a hidden glade on the island. There is a treasure chest nearby')
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "exit"):
            config.the_player.next.loc = self.main_location.locations['Coconut_Tree_Beach']
            config.the_player.go = True
            display.announce('You find a pathway leading to the North side of the island, it is very steep, you will not be able to go back')
# The coconut tree beach will contain a bountiful amount of food. 
class Coconut_Tree_Beach(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Beach with Coconut Trees"
        self.verbs['south'] = self
        self.event_chance = 100
        self.events.append(Coconuts())
    def enter(self):
        display.announce('You walk to the North end of the island. There is a beach with lots of coconuts.')
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['Great_Temple_Forest']

#The temple forest will be a 'lobby' for the great temple. ypu can enter the temple or move on to the next sublocation.
class Great_Temple_Forest(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Great Temple Forest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['enter'] = self
    def enter(self):
        display.announce('You walk into the forest. There is a temple to enter, and also a beach to the north')
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['Coconut_Tree_Beach']
            config.the_player.go = True
            display.announce('You walk North towards a beach')
        elif (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['Beach_In_Cove']
            config.the_player.go = True
            display.announce('You walk back towards the cove')
        elif (verb == 'enter'):
            config.the_player.next_loc = self.main_location.locations['Great_Temple']
            config.the_player.go = True
            display.announce('You walk towards the Great Temple')

        


#the Great Temple will contain a boss enemy, and will also have treasure to collect. It will be north of the starting cove.

class Great_Temple(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Great Temple"
        self.verbs['exit'] = self
        self.event_chance = 75
        self.events.append(Temple_Sentinel_Attack())
    def enter(self):
        display.announce('You enter the great temple. You have a bad feeling about this.')
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'exit'):
            config.the_player.next_loc = self.main_location.locations['Great_Temple_Forest']
            config.the_player.go = True
            display.announce('You exit the temple')