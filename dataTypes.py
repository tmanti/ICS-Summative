#imports
import item
import random
import pygame
import spritesheet

#define constants
FPS = 120
frames = FPS/8

chunkSize = 16

w,h = [1000, 1000]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150,150,150)
DARK_GRAY = (90, 90, 90)

#get game font
GAME_FONT_BUTTON = pygame.font.Font("8-bit.ttf", 27)
GAME_FONT = pygame.font.Font("8-bit.ttf", 30)
GAME_FONT_BIG = pygame.font.Font("8-bit.ttf", 40)
GAME_FONT_SMALL = pygame.font.Font("8-bit.ttf", 20)

GUI_FONT = pygame.font.Font("Pixel-Miners.otf", 30)
GUI_FONT_BIG = pygame.font.Font("Pixel-Miners.otf", 40)
GUI_FONT_SMALL = pygame.font.Font("Pixel-Miners.otf", 20)
GUI_FONT_SMALLER = pygame.font.Font("Pixel-Miners.otf", 17)
GUI_FONT_BUTTON = pygame.font.Font("Pixel-Miners.otf", 27)
GUI_FONT_DESC = pygame.font.Font("Pixel-Miners.otf", 11)

#position object
class pos:
    def __init__(self, x, y):
        #set variables
        self.x = x
        self.y = y

        #override methods
        self.__repr__ = self.__str__

    def return_Position(self):
        #returns dict
        return {"x":self.x, "y":self.y}

    #returns string
    def __str__(self):
        return str(self.x)+ ":" + str(self.y)

#level object
class Level:
    def __init__(self, lvl, exp):
        self.lvl = int(lvl)
        self.exp = int(exp)

        self.__repr__ = self.__str__

    def returnLvl(self):
        #return Lvl as a dictionary
        return {"lvl":self.lvl, "exp":self.exp}

    def __str__(self):
        #return Lvl as a string
        return "Level: " + str(self.lvl) + " With " + str(self.exp) + " XP"

class entityStats:
    #stats for characters
    def __init__(self, hp=0, mp=0, defen=0, spd=0, atk=0, dex=0, vit=0):
        self.health = hp
        self.defence = defen
        self.magic = mp
        self.speed = spd
        self.attack = atk
        self.dexterity = dex
        self.vitality = vit

    def return_entityStats(self):
        #return entityStats as a dictionary
        return {"hp":self.health, "mp":self.magic, "def": self.defence, "spd": self.speed, "atk": self.attack, "dex":self.dexterity, "vit": self.vitality}

class container:
    #class to store data
    def __init__(self, size, contents=None):
        self.size = size
        if contents:
            self.contents = {}
            for x in range(self.size):
                self.contents[str(x)] = item.ItemStack(contents[str(x)][0],
                                                       item.allItems[contents[str(x)][1]])
        else:
            self.contents={str(_):item.ItemStack(1, item.Nothing) for _ in range(self.size)}

    def AddTo(self, ItemStack):
        #adds data to container
        contains, index = self.contains(ItemStack.material.type)
        if contains:
            self.contents[index].amount += ItemStack.amount
        else:
            for x in self.contents:
                if self.contents[x].material.type == item.Nothing.type:
                    self.contents[x] = ItemStack
                    return

    def contains(self, type):
        #checks if an item with a certain id is in the container
        for x in self.contents:
            if self.contents[x].material.type == type:
                return True, x
        else:
            return False, None

    def containsGroup(self, groupId):
        #checks if an group id is in the container
        for x in self.contents:
            if self.contents[x].material.group == groupId:
                return True, x
        else:
            return False, None

    def return_Container(self):
        #return container as a dictionary
        toReturn = {}
        for x in self.contents:
            toReturn[x] = [self.contents[x].amount, self.contents[x].material.type]
        return toReturn

class playerInventory:
    #class for player inventory
    def __init__(self, weapon=item.ItemStack(1, item.Nothing), special=item.ItemStack(1, item.Nothing), armour=item.ItemStack(1, item.Nothing), ring=item.ItemStack(1, item.Nothing), container=container(30)):
        self.weapon = weapon
        self.special = special
        self.armour = armour
        self.ring = ring
        self.container = container

    def return_playerInventory(self):
        #return player inventory as a dictonary
        return {"weapon":self.weapon.material.type, "special":self.special.material.type, "armour":self.armour.material.type, "ring":self.ring.material.type, "container":self.container.return_Container()}

class playerData:
    #class for player data
    def __init__(self, position, inventory, stats, classType, Level):
        self.position = position
        self.inventory = inventory
        self.stats = stats
        self.playerClass = classType
        self.level = Level

    def return_playerData(self):
        #return player data as a dictionary
        return {"pos":self.position.return_Position(), "inv":self.inventory.return_playerInventory(), "stats": self.stats.return_entityStats(), "class":self.playerClass.ClassType, "level":self.level.returnLvl()}

class chunkData:
    #stores information about a chunk
    def __init__(self, pos, chunkData=None):
        self.chunkPos = pos
        self.chunkData = chunkData

class worldData:
    #class for the world data
    def __init__(self, seed=random.randint(1, 100000)): #seed is used and stored for ease in the database, progression is used and stored in the database for the save as well (world events and other thigns)
        self.seed = seed

    def return_worldData(self):
        #return worlddata as a string
        return {"seed":self.seed}

class saveData:
    #class for saving
    def __init__(self, playerData, worldData):
        self.player = playerData
        self.world =  worldData

    def return_save(self):
        #return save as a dictionary
        return [self.player.return_playerData(), self.world.return_worldData()]