from opensimplex import OpenSimplex
import random
import dataTypes
import spritesheet
import pygame

class Chunk:
    def __init__(self, chunkData):
        self.pos = chunkData.chunkPos
        self.tilePos = dataTypes.pos(self.pos.x*dataTypes.chunkSize, self.pos.y*dataTypes.chunkSize)
        self.tileGroup =  pygame.sprite.Group()

    def genChunk(self, noiseMap):
        for row in noiseMap:
            for noise, pos in row:
                if noise < 0.2:
                    self.tileGroup.add(waterTile(pos))
                elif noise < 0.3:
                    self.tileGroup.add(sandTile(pos))
                    pass
                elif noise < 0.8:
                    if 0.55< noise and noise < 0.56:
                        self.tileGroup.add(grassFlowerTile(pos, 1))
                    elif 0.57< noise and noise < 0.58:
                        self.tileGroup.add(grassFlowerTile(pos, 2))
                    else:
                        self.tileGroup.add(grassTile(pos))
                elif noise < 0.9:
                    self.tileGroup.add(mountainTile(pos))
                else:
                    self.tileGroup.add(snowTile(pos))

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.tilePos = position
        self.position = dataTypes.pos(self.tilePos.x * 32+(dataTypes.w/2), self.tilePos.y * 32+(dataTypes.h/2))

        self.rect = image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def update(self, playerPos,*args):
        self.rect.x = self.position.x - playerPos.x
        self.rect.y = self.position.y - playerPos.y

class sandTile(Tile):
    def __init__(self, position):
        self.image = pygame.image.load("resources/Sprites/tiles/sand.png")
        x,y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x*4, y*4))

        super().__init__(position, self.image)

class waterTile(Tile):
    def __init__(self, position):
        self.ss = spritesheet.spritesheet("resources/Sprites/tiles/water.png")
        self.sprites = [
            self.ss.image_at((8, 8, 8, 8), colorkey=dataTypes.WHITE),#main
            self.ss.image_at((0, 0, 8, 8), colorkey=dataTypes.WHITE),#feather top left
            self.ss.image_at((0, 8, 8, 8), colorkey=dataTypes.WHITE),  # feather left
            self.ss.image_at((8, 0, 8, 8), colorkey=dataTypes.WHITE),  # feather top
            self.ss.image_at((0, 16, 8, 8), colorkey=dataTypes.WHITE),  # feather bottom left
            self.ss.image_at((16, 0, 8, 8), colorkey=dataTypes.WHITE),  # feather top right
            self.ss.image_at((8, 16, 8, 8), colorkey=dataTypes.WHITE),  # feather bottom
            self.ss.image_at((16, 8, 8, 8), colorkey=dataTypes.WHITE),  # feather right
            self.ss.image_at((16, 16, 8, 8), colorkey=dataTypes.WHITE)  # feather bottom right
        ]

        self.image = self.sprites[0]

        super().__init__(position, self.image)

class grassTile(Tile):
    def __init__(self, position):
        self.image = pygame.image.load("resources/Sprites/tiles/grass.png")
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x*4, y*4))

        super().__init__(position, self.image)

class grassFlowerTile(Tile):
    def __init__(self, position, flowerNum):
        self.image = pygame.image.load("resources/Sprites/tiles/grassFlowers" + str(flowerNum) + ".png")
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x * 4, y * 4))

        super().__init__(position, self.image)

class mountainTile(Tile):
    def __init__(self, position):
        self.image = pygame.image.load("resources/Sprites/tiles/mountain8x8.png")
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x * 4, y * 4))

        super().__init__(position, self.image)

class snowTile(Tile):
    def __init__(self, position):
        self.image = pygame.image.load("resources/Sprites/tiles/snow.png")
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (x*4, y*4))

        super().__init__(position, self.image)

class world:
    def __init__(self, chunkData=None, seed=random.randint(1, 100000)):
        self.seed = seed
        self.gen = OpenSimplex(seed=self.seed)
        self.chunkSize = dataTypes.chunkSize
        self.chunkData = chunkData

    def noise(self, x, y):
        return self.gen.noise2d(x=x, y=y)/ 2.0 + 0.5

    def returnWorldData(self):
        return {"seed":self.seed}
    
    def genNoiseMap(self, tilePos):
        startPos = tilePos

        map = []

        for y in range(self.chunkSize):
            row = []
            for x in range(self.chunkSize):
                nx = (startPos.x+x)/ self.chunkSize - 0.5
                ny = (startPos.y+y)/ self.chunkSize - 0.5
                #print(self.noise(2*nx, 2*ny))
                row.append([self.noise(0.25*nx, 0.25*ny), dataTypes.pos(startPos.x+x, startPos.y+y)])
            #break
            map.append(row)

        return map