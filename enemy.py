# Enemy class started Jan 17, 2019

import pygame
import dataTypes
import xml.etree.ElementTree as ET
import item
import spritesheet
import random
import math

class dropTable:
    def __init__(self, dropsList):
        self.dropsList = dropsList

    def get_Drops(self):
        loot = []
        for x in self.dropsList:
            temp = random.randint(1, 100)
            if temp < x.chance:
                loot.append(item.ItemStack(random.randint(x.amount[0], x.amount[1]), x.Item))
        return loot

class dropCell:
    def __init__(self, itemId, chance, amount):
        self.Item = item.allItems[itemId]
        self.amount = [int(_) for _ in amount.split("-")]
        if len(self.amount) ==1:
            self.amount.append(self.amount[0])
        self.chance = chance

class Behavior:
    def __init__(self, type, distance=0):
        self.type = type
        self.distance = distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, projectileTexture, startPos, moveTo, rotation, bulletSpeed=1, toTravel=0):
        super().__init__()
        self.position = dataTypes.pos(startPos.x, startPos.y)
        self.startPos = dataTypes.pos(self.position.x, self.position.y)
        self.image = projectileTexture
        self.moveTo = moveTo
        self.bulletSpeed = bulletSpeed*0.03
        self.distance = dataTypes.pos(self.moveTo.x - self.position.x, self.moveTo.y - self.position.y)
        self.toTravel = toTravel
        self.image = pygame.transform.rotate(self.image, rotation-45)

        self.rect = self.image.get_rect()

    def update(self, *args):
        if math.sqrt((self.position.x - self.startPos.x)**2 + (self.position.y - self.startPos.y)**2) >= self.toTravel:
            self.kill()

        velo = [self.distance.x*self.bulletSpeed, self.distance.y*self.bulletSpeed]
        self.position.x +=velo[0]
        self.position.y +=velo[1]

        self.rect.x = self.position.x
        self.rect.y = self.position.y

class EnemyData:
    def __init__(self, group, type, name, stats, position, texture, projectile, drops, behavior):
        super().__init__()

        self.stats = stats
        self.position = position
        self.entityGroup = group
        self.type= type
        self.name = name

        self.Texture = texture
        self.projectile = projectile

        self.behavior = behavior

        self.droptable = drops

class Goblin(pygame.sprite.Sprite):
    def __init__(self, x, y, data):
        super().__init__()
        self.data = data

        self.position = dataTypes.pos(x,y)

        self.canAttack = True

        ss=spritesheet.spritesheet(self.data.Texture.fileLocation)
        self.image = ss.image_at((self.data.Texture.index[0], self.data.Texture.index[1], 8, 8), colorkey=dataTypes.WHITE)

        ss = spritesheet.spritesheet(self.data.projectile.fileLocation)
        self.projImage = ss.image_at((self.data.Texture.index[0], self.data.Texture.index[1], 8, 8), colorkey=dataTypes.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        self.tilePos = dataTypes.pos(self.position.x // 32, self.position.y // 32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // 16, self.tilePos.y // 16)

        self.projRange = 5

        self.bullets = pygame.sprite.Group()

    def update(self, playerPos, screen, *args):
        self.bullets.update()
        self.tilePos = dataTypes.pos(self.position.x // 32, self.position.y // 32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // dataTypes.chunkSize, self.tilePos.y // dataTypes.chunkSize)
        self.HpBar = pygame.Surface((50, 10))
        pygame.draw.rect(self.HpBar, dataTypes.RED, (0, 0, ((50 / goblins[self.data.type].stats.health) * self.data.stats.health), 10))
        self.rect.x = self.position.x - playerPos.x
        self.rect.y = self.position.y - playerPos.y

        screen.blit(self.HpBar, (self.rect.x-10, self.rect.y+50))

    def Fire(self, playerPos):
        rel_x, rel_y = playerPos.x - self.rect.x , playerPos.y- self.rect.y
        angle = (180/math.pi) * -math.atan2(rel_y, rel_x)
        moveToPos = dataTypes.pos(self.projRange*math.cos(angle/55.47)+dataTypes.w//2, self.projRange*math.sin(-angle/55.47)+ dataTypes.h//2)
        self.bullets.add(Bullet(self.projImage, dataTypes.pos(self.rect.x, self.rect.y), moveToPos, angle, toTravel=self.projRange*32))


allMobs = {}
goblins = {}

def init():
    tree = ET.parse("resources/xml/enemies.xml")
    root = tree.getroot()
    for child in root:
        allMobs[child.get('type')] = EnemyData(
            child.find("Group").text,
            child.get("type"),
            child.get("id"),
            dataTypes.entityStats(
                hp=int(child.find("stats").find("Hitpoints").text),
                defen=int(child.find("stats").find("Defence").text),
                spd=int(child.find("stats").find("Speed").text),
                atk=[int(_) for _ in child.find("stats").find("Attack").text.split("-")],
                dex=int(child.find("stats").find("Dexterity").text)
            ),
            dataTypes.pos(None, None),
            item.spriteRef(child.find("Texture").find("File").text, child.find("Texture").find("Index").text, "enemies"),
            item.spriteRef(child.find("ProjectileTexture").find("File").text, child.find("ProjectileTexture").find("Index").text, "enemies"),
            dropTable([dropCell(x.find("itemId").text, int(x.find("Chance").text), x.find("Amount").text) for x in child.find("DropTable").findall("DropCell")]),
            Behavior(child.find("Behavior").get("type"), distance=child.find("Behavior").get("distance"))
        )
        if child.find("Group").text == "Goblins":
            goblins[child.get('type')] = allMobs[child.get('type')]
    print(allMobs)