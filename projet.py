import sys
import datetime
from random import *
import math
import time

from matplotlib.pyplot import get

import pygame
from pygame.locals import *

import numpy as np
from abc import abstractmethod

###

################################
## Parameters: initialisation ##
################################

<<<<<<< HEAD
nbHumans = 100
nbZombies = 50
nbCleverZombies = 30
nbTrees = 800# pas inferieur a 2*(worldWidth//2+1) + worldHeight-2
nbBurningTrees = 10
=======
nbHumans = 30
nbZombies = 20
nbCleverZombies = 10
nbTrees = 250# pas inferieur a 2*(worldWidth//2+1) + worldHeight-2
nbBurningTrees = 0
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c

probGrowth = 0.0001 #probabilité qu'un arbre se pousse
probIgnite = 0.001 #probabilité qu'un arbre se met en feu tt seul
probChange = 0.1 #probabilité qu'un un arbre en feu devient tout noir
proGagner = 0.0 #probabilité qu'un humain gagne le duel contre un zombie
probGendre = 0.5 #probabilité du genre (Masculain ou féminin)
probReproduction = 1 #probabilité de reproduction
probZombieIntelChangeDir = 0.8 #probabilité qu'un zombie intelligent change de direction quand il est bloqué
<<<<<<< HEAD
probPluie = 0.00
=======
probPluie = 0.02
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
probRegrowth = 0.001
ID = 0 
LaunchOrder = 0 #Ordre de Lancer des flèches
PorteBrise = False #Porte Brisée 
Pluie = False
nbFoisPluie = 500
<<<<<<< HEAD
afficheEnergie = False
=======
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c

###########################
## Parameters: rendering ##
###########################

# display screen dimensions
screenWidth = 1400 
screenHeight = 900

# world dimenesions (total number of cells)
worldWidth = 65
worldHeight = 65

# surface of displayed tiles (number of cells that are rendered)
viewWidth = 65
viewHeight = 65

objectMapLevels = 12 #number of levels for objectMap

scaleMultiplier = 0.2 #re-scaling of loaded images

# set scope of displayed tiles
xViewOffset = 0
yViewOffset = 0

maxFps = 30 #maximum frames-per-second

###########################
## SETTING UP SDL/Pygame ##
###########################

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Game of Thrones') 
bg = pygame.image.load("assets/Monde/ciel1.jpg")
<<<<<<< HEAD
font = pygame.font.SysFont('Times New Roman', 15)
=======
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c

#################################
## CORE/USER: image management ##
#################################

def loadImage(filename) : 
    global tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier
    image = pygame.image.load(filename) #image type : Surface
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*scaleMultiplier), int(tileTotalHeightOriginal*scaleMultiplier)))
    return image

def loadAllImages() : 
    global tileType, objectType, agentType

    tileType = []
    objectType = []
    agentType = []

    #tileType.append(loadImage('assets/Monde/voxelTile_55.png')) #grass
    tileType.append(loadImage('assets/Monde/platformerTile_48_ret.png')) #grass
    tileType.append(loadImage('assets/Monde/voxelTile_53.png')) #rock tile
    tileType.append(loadImage('assets/Monde/landscape_32.png')) #road tile



    objectType.append(None)
    objectType.append(loadImage('assets/Monde/tree.png')) # tree
    objectType.append(loadImage('assets/Monde/voxelTile_30.png')) #wall block 
    objectType.append(loadImage('assets/Monde/transparent_wall.png')) #wall block transparent
    objectType.append(loadImage('assets/Monde/voxelTile_19.png')) #just a home
    objectType.append(loadImage('assets/Monde/firetree.png')) #tree on fire
    objectType.append(loadImage('assets/Monde/burned_tree.png')) #burned_tree
    objectType.append(loadImage('assets/Monde/wallHalf_NW_ret.png')) #border
    objectType.append(loadImage('assets/Monde/wallHalf_SE_ret.png')) #lateral border far
    objectType.append(loadImage('assets/Monde/wallHalf_NE_ret.png')) #lateral border close
    objectType.append(loadImage('assets/Monde/arrow-ret.png')) #arrow
    objectType.append(loadImage('assets/Monde/voxelTile_26.png')) #porte
    objectType.append(loadImage('assets/Monde/turkey_NW.png')) #food
<<<<<<< HEAD
    objectType.append(None) #building
    objectType.append(loadImage('assets/Monde/tower_40.png')) #tower
    objectType.append(loadImage('assets/Monde/tent.png')) #tent
    objectType.append(loadImage('assets/Monde/campfire.png')) #campfire
    objectType.append(loadImage('assets/Monde/signpost.png')) #signpost
    objectType.append(loadImage('assets/Monde/strcloth.png')) #structure cloth
    objectType.append(loadImage('assets/Monde/towerbase.png')) #tower1
    objectType.append(loadImage('assets/Monde/towermiddle.png')) #tower2
    objectType.append(loadImage('assets/Monde/towertop.png')) #tower3
    objectType.append(loadImage('assets/Monde/pretty-rock.png')) #rocks


    agentType.append(None)
    agentType.append(loadImage('assets/Monde/zom1.png')) #night walker 
    agentType.append(loadImage('assets/Monde/V.png')) #MaleAdventurer
    agentType.append(loadImage('assets/Monde/archer2.png')) #archer
    agentType.append(loadImage('assets/Monde/transparent_wall.png')) #archer transparent
    agentType.append(loadImage('assets/Monde/zomb1.png')) #burning zombie
=======
    objectType.append(loadImage('assets/Monde/blockHuge_N_ret.png')) #building
    objectType.append(loadImage('assets/Monde/tower_40.png')) #tower



    agentType.append(None)
    agentType.append(loadImage('assets/Monde/zom.png')) #night walker 
    agentType.append(loadImage('assets/Monde/V.png')) #MaleAdventurer
    agentType.append(loadImage('assets/Monde/archer2.png')) #archer
    agentType.append(loadImage('assets/Monde/transparent_wall.png')) #archer transparent
    agentType.append(loadImage('assets/Monde/zombie.png')) #burning zombie
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
    agentType.append(loadImage('assets/Monde/f.png')) #FemaleAdventurer

def resetImages() : 
    global tileTotalWidth, tileTotalHeight, tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier, heightMultiplier, tileVisibleHeight
    tileTotalWidth = tileTotalWidthOriginal * scaleMultiplier  # width of tile image, as stored in memory
    tileTotalHeight = tileTotalHeightOriginal * scaleMultiplier # height of tile image, as stored in memory
    tileVisibleHeight = tileVisibleHeightOriginal * scaleMultiplier # height "visible" part of the image, as stored in memory
    heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight
    loadAllImages()
    return

####################################
## CORE/USER : Objects parametres ##
####################################

tileTotalWidthOriginal = 111  # width of tile image
tileTotalHeightOriginal = 128 # height of tile image
tileVisibleHeightOriginal = 64 # height "visible" part of the image, i.e. top part without subterranean part

###

tileType = [] 
objectType = []
agentType = []

noObjectId = noAgentId = 0

# AGENTS
zombieId = 1
maleId = 2
archerId = 3
agentTransparentId = 4
burnedZomId = 5
femaleId = 6 

# TERRAIN
grassId = 0
rockId = 1
roadLId = 2

# OBJETS
treeId = 1
blockId = 2
transBlockId = 3
homeId = 4
burningTreeId = 5
burnedTreeId = 6
borderId = 7
latBorderFarId = 8
latBorderCloseId = 9
arrowId = 10
porteId = 11
foodId = 12
buildingId = 13
towerId = 14
<<<<<<< HEAD
tentId = 15
campfireId = 16
signpostId = 17
strclothId = 18
towerbaseId = 19
towermiddleId = 20
towertopId = 21
prettyrockId = 22


=======
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c

###

resetImages()

###

terrainMap = [x[:] for x in [[0] * worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]

#newHeightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
newObjectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
#newAgentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]

###

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 2*tileTotalHeight # border. Could be 0.

####

###################################
## CORE/USER : Set / get methods ##
###################################

def getWorldWidth():
    return worldWidth

def getWorldHeight():
    return worldHeight

def getViewWidth():
    return viewWidth

def getViewHeight():
    return viewHeight

def getTerrainAt(x,y):
    return terrainMap[y][x]

def setTerrainAt(x,y,type):
    terrainMap[y][x] = type

def getHeightAt(x,y):
    return heightMap[y][x]

def setHeightAt(x,y,height):
    heightMap[y][x] = height

def getObjectAt(x,y,level=0):
    if level < objectMapLevels:
        return objectMap[level][y][x]
    else:
        print ("[ERROR] getObjectMap(.) -- Cannot return object. Level does not exist.")
        return 0

def setObjectAt(x,y,type,level=0): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        objectMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def setNewObjectAt(x,y,type,level=0): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        newObjectMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def getAgentAt(x,y, level = 0):
    if level < objectMapLevels:
        return agentMap[level][y][x]
    else:
        print ("[ERROR] getObjectMap(.) -- Cannot return object. Level does not exist.")
        return 0

def setAgentAt(x,y,type, level = 0):
    if level < objectMapLevels:
        agentMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def getAgentByPos(agents, x, y) :
    for a in agents: 
        if(a.getType() != archerId):
            (x1, y1) = a.getPosition()
            if x1==x and y1==y:
                return a

###########################
## CORE/USER : Rendering ##
###########################

def render( it = 0 ):
    global xViewOffset, yViewOffset
    screen.fill((0,0,0)) # create the screen
    #pygame.draw.rect(screen, (255,255,255), (0, 0, screenWidth, screenHeight)) # overkill - can be optimized. (most sprites are already "naturally" overwritten)
    screen.blit(bg,(0,0))
    for y in range(getViewHeight()):
        for x in range(getViewWidth()):
            # assume: north-is-upper-right
            xTile = ( xViewOffset + x + getWorldWidth() ) % getWorldWidth()
            yTile = ( yViewOffset + y + getWorldHeight() ) % getWorldHeight()
            
            height = getHeightAt( xTile , yTile ) * heightMultiplier

            xScreen = xScreenOffset + x * tileTotalWidth / 2 - y * tileTotalWidth / 2 
            yScreen = yScreenOffset + y * tileVisibleHeight / 2 + x * tileVisibleHeight / 2 - height 
            
            screen.blit( tileType[ getTerrainAt( xTile , yTile ) ] , (xScreen, yScreen)) # display terrain
            
            for level in range(objectMapLevels):
                if getObjectAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit(objectType[ getObjectAt( xTile , yTile, level) ] , ( xScreen, yScreen - heightMultiplier*(level+1) )) 
                idA = getAgentAt( xTile, yTile , level)
                if idA != 0: # agent on terrain?
                    if afficheEnergie and idA in [maleId, femaleId]:
                        a = getAgentByPos(humanAgents, xTile, yTile)
                        text = font.render(str(a.energie), True, 'Black', 'White')
                        screen.blit(text, ( xScreen + 10, yScreen - heightMultiplier*(level+1) - 17))

                    screen.blit( agentType[ getAgentAt( xTile, yTile, level ) ] , ( xScreen, yScreen - heightMultiplier*(level+1) ))
            
    pygame.display.update()     
    return

############
## Agents ##
############

class Agent:
    def __init__(self,imageId, x = None, y = None, energie = None):
        global ID
        self.type = imageId
        self.id = ID
        ID+=1
        self.reset(x,y, energie)

        return
        
    @abstractmethod 
    def reset(self):
        pass

    def getPosition(self):
        return (self.x,self.y)

    def move(self, it = 0): 
        pass

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def setType(self,imageId) : 
        self.type = imageId
    
############
## HUMANS ##
############

class HumanAgent(Agent) : 
    def reset(self, x, y, energie) : 
        if energie == None : 
            self.energie = 100 
        else : 
            self.energie = energie
        
        if x != None and y != None : 
            self.x = x
            self.y = y
        else : 
            self.x = randint(0,getWorldWidth()//2-1)
            self.y = randint(0,getWorldHeight()-1)
            while getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
                self.x = randint(0,getWorldWidth()//2-1)
                self.y = randint(0,getWorldHeight()-1)
            
        setAgentAt(self.x,self.y,self.type)
        return


    def move(self, it = 0): 
        global humanAgents, zombieAgents

        ### SI L'HUMAIN N'A PLUS D'ENERGIE, IL MEURT 
        if self.energie <= 0:
            a = getAgentByPos(humanAgents, self.x, self.y)
            humanAgents.remove(a)
            setAgentAt(self.x, self.y, noAgentId)
            return
        else : 
            xNew = self.x
            yNew = self.y

            ### FUITE : SI DANS DEUX PAS IL Y A UN ZOMBIE, FAUT FUIRE 
            for neighbours in ((-2,0),(+2,0),(0,-2),(0,+2)): 
                y1 = (yNew + neighbours[0] + worldWidth) % worldWidth
                x1 = (xNew + neighbours[1] + worldHeight) % worldHeight
                if getAgentAt(x1,y1) == zombieId:
                    if neighbours[0] < 0 : 
                        yNew = (yNew+1+worldHeight) % worldHeight
                    elif neighbours[0] > 0 : 
                        yNew = (yNew-1+worldHeight) % worldHeight
                    elif neighbours[1] < 0 : 
                        xNew = (xNew+1+worldWidth) % worldWidth
                    elif neighbours[1] > 0 : 
                        xNew = (xNew-1+worldWidth) % worldWidth
                    break  

<<<<<<< HEAD
            if xNew == self.x and yNew == self.y :  
                ### LOOK FOR FOOOOOD
                for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1),(-1,-1),(-1,1),(1,-1),(1,1)):
                    y1 = (yNew + neighbours[0] + worldWidth) % worldWidth
                    x1 = (xNew + neighbours[1] + worldHeight) % worldHeight
                    if getObjectAt(x1, y1) == foodId:
                        xNew = x1
                        yNew = y1
                        setObjectAt(x1, y1, noObjectId)
                        self.energie += 10
                        break

            if xNew == self.x and yNew == self.y :  
                ### REPRODUCTION
                if random() < probReproduction and self.energie > 50 and self.getType() == maleId: 
                    for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)): 
                        y1 = (yNew + neighbours[0] + worldWidth) % worldWidth
                        x1 = (xNew + neighbours[1] + worldHeight) % worldHeight
                        if (getAgentAt(x1, y1)== femaleId) :
                            a = getAgentByPos(humanAgents, x1, y1) 
                            if a.energie > 50 : 
                                for neighbors in ((-1,0),(1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)) : 
                                    if getAgentAt(xNew + neighbors[0], yNew + neighbors[1]) == noAgentId and getObjectAt(xNew + neighbors[0], yNew + neighbors[1]) == noAgentId :
                                        if random() > probGendre : 
                                            humanAgents.append(HumanAgent(maleId, xNew + neighbors[0], yNew + neighbors[1], self.energie//2 + a.energie//2))
                                        else : 
                                            humanAgents.append(HumanAgent(femaleId, xNew + neighbors[0], yNew + neighbors[1], self.energie//2 + a.energie//2))
                                        self.energie  = self.energie - self.energie//5
                                        a.energie  = a.energie - a.energie//4
                                        break

            if xNew == self.x and yNew == self.y :  
=======
                
            ### LOOK FOR FOOOOOD
            for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1),(-1,-1),(-1,1),(1,-1),(1,1)):
                y1 = (yNew + neighbours[0] + worldWidth) % worldWidth
                x1 = (xNew + neighbours[1] + worldHeight) % worldHeight
                if getObjectAt(x1, y1) == foodId:
                    xNew = x1
                    yNew = y1
                    setObjectAt(x1, y1, noObjectId)
                    self.energie += 10
                    break
        
            ### REPRODUCTION
            if random() < probReproduction and self.energie > 50 : 
                for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)): 
                    y1 = (yNew + neighbours[0] + worldWidth) % worldWidth
                    x1 = (xNew + neighbours[1] + worldHeight) % worldHeight
                    if (getAgentAt(x1, y1) in [maleId, femaleId]) :
                        a = getAgentByPos(humanAgents, x1, y1) 
                        if (self.getType() != a.getType() and a.energie > 50) : 
                                #if getAgentAt(x1+1, y1) == noAgentId and getObjectAt(x1+1, y1) == noObjectId: 
                                if random() > probGendre : 
                                    humanAgents.append(HumanAgent(maleId, xNew, yNew, (self.energie//2 + a.energie//2)))
                                else : 
                                    humanAgents.append(HumanAgent(femaleId, xNew, yNew, self.energie//2 + a.energie//2))
                                self.energie //= 2
                                a.energie //= 2
            
            if xNew == self.x and yNew == self.y :
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
                xNew = ( self.x + [-1,0,+1][randint(0,2)] + getWorldWidth() ) % getWorldWidth()
                yNew = ( self.y + [-1,0,+1][randint(0,2)] + getWorldHeight() ) % getWorldHeight()
            
            if getObjectAt(xNew,yNew) in [noObjectId, foodId] and getAgentAt(xNew, yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
                setAgentAt(self.x,self.y,noAgentId)
                self.x = xNew
                self.y = yNew
                setAgentAt(self.x,self.y,self.type)
                self.energie -= 1
        return

#############
## Archers ##
#############


class ArcherAgent(HumanAgent) : 
    global zombieAgents
    def __init__(self, imageId):
        self.type = imageId
        self.arrow = arrowId
        self.reset()
        return

    def reset(self) : 
        self.x = getWorldWidth()//2 
        self.posarrowx = self.posarrowy = self.posarrowz = 0
        self.y = randint(1,getWorldHeight()-2)
        self.z = objectMapLevels-2 
        self.destarrowx = 0
        while getAgentAt(self.x,self.y,self.z) != 0 :
            self.y = randint(0,getWorldHeight()-1)
    
        setAgentAt(self.x, self.y, self.type, self.z)
        return

    def getPosition(self) :
        return (self.x, self.y, self.z)

    def tirage(self):
        (self.posarrowx, self.posarrowy, self.posarrowz) = self.getPosition()
        self.posarrowx+=1
        setObjectAt(self.posarrowx, self.posarrowy, arrowId, self.posarrowz) 
        self.destarrowx = randint(getWorldHeight()//2 + 2, getWorldHeight()-1)  
    
    def deleteArrow(self) :  
        if getObjectAt(self.posarrowx, self.posarrowy, self.posarrowz) == arrowId : 
            setObjectAt(self.posarrowx, self.posarrowy, noObjectId, self.posarrowz)
        else : 
            setObjectAt(self.posarrowx, self.posarrowy, getObjectAt(self.posarrowx, self.posarrowy, self.posarrowz), self.posarrowz)
            
        
    def move(self, it = 0):
        if it%50 == 0 and LaunchOrder == 1 :
            self.deleteArrow()
            self.tirage()

        else : 
            if self.posarrowx < self.destarrowx : 
                setObjectAt(self.posarrowx, self.posarrowy, noObjectId, self.posarrowz)
                self.posarrowz = self.posarrowz - (self.posarrowz//(self.destarrowx - self.posarrowx))
                self.posarrowx+=1
                if (self.posarrowz <= 0) :  
                    if getObjectAt(self.posarrowx, self.posarrowy) == treeId : 
                        setObjectAt(self.posarrowx, self.posarrowy, burningTreeId)
                    elif getAgentAt(self.posarrowx, self.posarrowy) == zombieId :
                        a = getAgentByPos(zombieAgents, self.posarrowx, self.posarrowy) 
                        a.setType(burnedZomId)
                    elif getObjectAt(self.posarrowx, self.posarrowy) == noObjectId : 
                        setObjectAt(self.posarrowx, self.posarrowy, arrowId)
                else : 
                        setObjectAt(self.posarrowx, self.posarrowy, arrowId, self.posarrowz) 

#############
## Zombies ##
#############

class ZombieAgent(Agent) :
    def reset(self, x, y, energie = None) :
        self.burningDays = 3
        if x != None and y != None : 
            self.x = x
            self.y = y
        else :  
            self.x = randint(getWorldWidth()//2+1,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
            while getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
                self.x = randint(getWorldWidth()//2+1,getWorldWidth()-1)
                self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y, self.type)
        return
        
    def decrementeDays(self):
        self.burningDays-=1
    
    def move(self, it = 0):
        global humanAgents, zombieAgents
        
        xNew = self.x
        yNew = self.y
        ###DUEL
        if(self.getType() != burnedZomId):
            for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)):
                x1 = (xNew+neighbours[0]+worldWidth) % worldWidth
                y1 = (yNew+neighbours[1]+worldHeight) % worldHeight
                if getAgentAt(x1,y1) in [maleId, femaleId]:
                
                    if random() > proGagner : # le zombie a gagne
                        a = getAgentByPos(humanAgents, x1, y1)
                        humanAgents.remove(a)
                        #setObjectAt(xNew, yNew, noAgentId)
                        z = ZombieAgent(zombieId, x1, y1) 
                        zombieAgents.append(z) 
                    else : # le zombie a perdu 
                        z = getAgentByPos(zombieAgents, xNew, yNew)
                        z.setType(burnedZomId)
                    
        ###CHASSE
        for neighbours in ((-2,0),(+2,0),(0,-2),(0,+2)): #il regarde le voisinage
            y1 = (yNew+neighbours[0]+worldWidth) % worldWidth
            x1 = (xNew+neighbours[1]+worldHeight) % worldHeight
            if getAgentAt(x1,y1) in [maleId, femaleId]:
                if neighbours[0] < 0 : 
                    yNew = (yNew-1+worldHeight) % worldHeight
                elif neighbours[0] > 0 : 
                    yNew = (yNew+1+worldHeight) % worldHeight
                elif neighbours[1] < 0 : 
                    xNew = (xNew-1+worldWidth) % worldWidth
                elif neighbours[1] > 0 : 
                    xNew = (xNew+1+worldWidth) % worldWidth
                break  

        ###SI LA PORTE EST BRISE, ALORS ATTAQUE
        if PorteBrise : 
            m = getWorldHeight() // 2
            xNew = self.x - 1 
            if(self.y not in [m, m+1, m-1]):
                if(self.y >= getWorldHeight() // 2):
                    yNew = self.y - 1
                elif(self.y < getWorldHeight() // 2):
                    yNew = self.y + 1  
        else : 
            ###Si tu ne chasses pas ou tu n'attaque pas, bouge au hasard
            if xNew == self.x and yNew == self.y : 
                if not PorteBrise : #SI LA PORTE N'EST TOUJOURS PAS BRISE, BOUGE AU HASARD
                    xNew = ( self.x + [-1,0,+1][randint(0,2)] + getWorldWidth() ) % getWorldWidth()
                    yNew = ( self.y + [-1,0,+1][randint(0,2)] + getWorldHeight() ) % getWorldHeight()
            
        if getObjectAt(xNew,yNew) in [noObjectId, foodId] and getAgentAt(xNew, yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        return
    
#########################
## Intelligent Zombies ##
#########################


class IntelligentZombieAgent(ZombieAgent):
    def move(self, it = 0) :
        global humanAgents, zombieAgents
        xNew = self.x
        yNew = self.y

        ###DUEL
        if(self.getType() != burnedZomId):
            for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)):
                x1 = (xNew + neighbours[0] + worldWidth) % worldWidth
                y1 = (yNew + neighbours[1] + worldHeight) % worldHeight
                if getAgentAt(x1,y1) in [maleId, femaleId]:
                    if random() > proGagner : # le zombie a gagne
                        a = getAgentByPos(humanAgents, x1, y1)
                        humanAgents.remove(a)
                        z = ZombieAgent(zombieId, x1, y1) 
                        zombieAgents.append(z) 
                    else : # le zombie a perdu 
                        z = getAgentByPos(zombieAgents, xNew, yNew)
                        z.setType(burnedZomId)
                    
        
        ##CHASSE        
        for neighbours in ((-2,0),(+2,0),(0,-2),(0,+2)): #il regarde le voisinage 
            if getAgentAt((xNew+neighbours[0]+worldWidth) % worldWidth,(yNew+neighbours[1]+worldHeight) % worldHeight) in [maleId, femaleId]:
                xNew += neighbours[0]
                yNew += neighbours[1]
                break
        
        ##SI IL NE CHASSE PAS OU IL N'EST PAS DANS UN DUEL, ALORS ATTAQUE LE MUR POUR LE BRISER
        m = getWorldHeight() // 2
        if xNew == self.x and yNew == self.y :
            if random() < probZombieIntelChangeDir and not PorteBrise: # vers le mur quand il est entouré pas des objets ou des agents, et qu'il ne peut pas bouger 
                xNew = self.x - 1 
                if(self.y not in [m, m+1, m-1]):
                    if(self.y >= getWorldHeight() // 2):
                        yNew = self.y - 1
                    elif(self.y < getWorldHeight() // 2):
                        yNew = self.y + 1 
            elif PorteBrise and random() < probZombieIntelChangeDir: 
                if self.y not in [m, m+1, m-1] and self.x >= getWorldWidth()//2: # il n'est pas bien aligne tel qu'il entre et il se trouve encore dans le territoire des zombies
                    xNew = ( self.x + [-1,0,+1][randint(0,2)] + getWorldWidth() ) % getWorldWidth()
                    if(self.y >= getWorldHeight() // 2):
                        yNew = self.y - 1
                    elif(self.y < getWorldHeight() // 2):
                        yNew = self.y + 1   
                elif self.y in [m, m+1, m-1] and self.x >= getWorldWidth()//2 : #si il est aligné mais il est dans l'endroit 
                    xNew = self.x - 1
                elif self.x < getWorldWidth()//2 : # ce else: il est dans le territoire des humains
                    xNew = self.x -1
                    yNew = ( self.y + [-1,0,+1][randint(0,2)] + getWorldHeight() ) % getWorldHeight()
            else :  # il bouge au hasard, pour ne pas etre bloques 
                xNew = ( self.x + [-1,0,+1][randint(0,2)] + getWorldWidth() ) % getWorldWidth()
                yNew = ( self.y + [-1,0,+1][randint(0,2)] + getWorldHeight() ) % getWorldHeight()
            
            

        if getObjectAt(xNew,yNew) in [noObjectId, foodId] and getAgentAt(xNew, yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        return

###########
## Porte ##
###########


class Porte: 
    def __init__(self, x, y, z, imageId):
        self.type = imageId
        self.duree = 10
        self.x = x
        self.y = y
        self.z = z
        setObjectAt(self.x, self.y, self.type, self.z)
    
    def change(self, imageID) : 
        self.type = imageID
        setObjectAt(self.x, self.y, self.type, self.z)
    
    def verif(self) : 
        if getAgentAt(self.x+1, self.y) == zombieId : 
            self.duree -= 1
            if self.duree == 0 :
                self.type = noObjectId 
                setObjectAt(self.x, self.y, self.type, self.z)


##########
## Rain ##
##########

class ParticlePrinciple:
	def __init__(self):
		self.particles = []

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2]
				particle[1] -= 0.1
				#pygame.draw.circle(screen, pygame.Color(173, 216, 230), particle[0], int(particle[1]))
				pygame.draw.line(screen, pygame.Color(173, 216, 230), (particle[0][0], particle[0][1]), (particle[0][0],particle[0][1] + particle[1]), 2)


	def add_particles(self): 
		pos_x = randint(0, screenWidth)
		pos_y = randint(0, screenHeight)
<<<<<<< HEAD
		radius = 5
=======
		radius = 10
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
		direction = 1
		particle_circle = [[pos_x,pos_y],radius,direction]
		self.particles.append(particle_circle)

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particles = particle_copy

humanAgents = []
zombieAgents = []
porte = []

######################
## Initialise world ##
######################

def initWorld() : 
    global nbTrees 
<<<<<<< HEAD
    # spawn pretty rocks
    count = 0
    while(count < 20):
        xp = randint(getWorldWidth() // 2 + 2, getWorldWidth() - 2)
        yp = randint(1, getWorldHeight() - 2)
        #if getObjectAt(xp, randint(getWorldHeight()-1) == noObjectId:
        setObjectAt(xp, yp, prettyrockId)
        count+=1
	
    #Le village est uniquement valable pour la dimension 64*64, en cas d'utilisation d'autres dimensions, merci de commenter. 
    # make village
    x_offset = 1
    y_offset = 1
    roadter = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    
    ]

    for x in range(len(roadter[0])):
        for y in range(len(roadter)):
            setTerrainAt(y+y_offset, x+x_offset, roadter[y][x])

    roadobj = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, 0, 0, 15, 0, 0, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 18, 0, 0, 16, 0, 0, 17, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 15, 0, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 15, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 15, 0, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    
    ]
    for x in range(len(roadobj[0])):
        for y in range(len(roadobj)):
            if roadobj[y][x] == -1: # tour base + middle + top
                setObjectAt(y+y_offset, x+x_offset, towerbaseId, 0)
                setObjectAt(y+y_offset, x+x_offset, towermiddleId, 1)
                setObjectAt(y+y_offset, x+x_offset, towertopId, 2)
                setHeightAt(y+y_offset, x+x_offset, 0)
 
            else:
                setObjectAt(y+y_offset, x+x_offset, roadobj[y][x])
                setHeightAt(y+y_offset, x+x_offset, 0)
    
    # make human side borders
    for l in range(objectMapLevels//2) : 
        for i in range(getWorldHeight()) :
            setObjectAt(0, i, towerId, l)

    for l in range(objectMapLevels//2) : 
=======
    
    # make village

    setTerrainAt(10, 19, rockId)

    # make human side borders
    for l in range(objectMapLevels//3) : 
        for i in range(getWorldHeight()) :
            setObjectAt(0, i, towerId, l)

    for l in range(objectMapLevels//3) : 
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
        for r in range(getWorldWidth()//2) :
            setObjectAt(r, 0, towerId, l)
            setObjectAt(r, getWorldHeight() - 1, towerId, l)
    
    for i in range(getWorldHeight()) :
<<<<<<< HEAD
        setObjectAt(0, i, borderId, objectMapLevels//2)
    for r in range(getWorldWidth()//2) :
        setObjectAt(r, 0, latBorderFarId, objectMapLevels//2)
=======
        setObjectAt(0, i, borderId, objectMapLevels//3)
    for r in range(getWorldWidth()//2) :
        setObjectAt(r, 0, latBorderFarId, objectMapLevels//3)
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
        setObjectAt(r, getWorldHeight() - 1, latBorderCloseId, objectMapLevels//3)
    
    # build the wall
    y = getWorldWidth() // 2
    x = getWorldHeight() // 2
    for i in range(0, getWorldHeight()) : 
        for level in range(0, objectMapLevels-2): 
            if(i not in [x, x+1, x-1]):
                setObjectAt(y, i, blockId, level)  
                setObjectAt(y+1, i, blockId, level)
        setTerrainAt(y, i, rockId)
        setTerrainAt(y+1, i, rockId)  
    for i in [x, x+1, x-1] : 
        for level in range(4, objectMapLevels-2): 
            setObjectAt(y, i, blockId, level)  
            setObjectAt(y+1, i, blockId, level) 
    

    # build the door
    for i in range(4) :
        for j in [x, x+1]:
            porte.append(Porte(j, y, i, porteId))
            porte.append(Porte(j, y-1, i, porteId))
            porte.append(Porte(j, y+1, i, porteId))
    
    #make trees border
    for i in range(getWorldWidth()//2+2, getWorldWidth()):
        setObjectAt(i, 0, treeId)
        setObjectAt(i, getWorldWidth()-1, treeId)
        nbTrees-=2

    for i in range(0, getWorldHeight()):
        setObjectAt(getWorldWidth()-1, i, treeId)
        nbTrees-=1
    
    
    #make trees
    h = getWorldHeight()
    w = getWorldWidth()
    listeInterx = [i for i in range(w//4, 3*w//4)]
    listeIntery = [i for i in range(h//4, 3*h//4)] 

    for i in range(nbTrees) :
        x = randint(w//2+2, w-1)
        y = randint(0,h-1)
        while (x in listeInterx and y in listeIntery) or getObjectAt(x,y) != 0 or getAgentAt(x,y) != 0:
            x = randint(w//2+1, w-1)
            y = randint(0,h-1)
        setObjectAt(x,y,treeId)

    for i in range(nbBurningTrees):
        x = randint(w//2+1, w-1)
        y = randint(0,h-1)
        while (x in listeInterx and y in listeIntery) or getObjectAt(x,y) != 0 or getAgentAt(x,y) != 0:
            x = randint(w//2+1, w-1)
            y = randint(0,h-1)
        setObjectAt(x, y, burningTreeId)
    return

def initAgents() :
    # spawn the agents
    for i in range(nbHumans) : 
        if random() < probGendre : 
            humanAgents.append(HumanAgent(maleId)) 
        else : 
            humanAgents.append(HumanAgent(femaleId))

    #spawn the archers
    for i in range(getWorldHeight()):     
       humanAgents.append(ArcherAgent(archerId)) 
    
    #spawn stupid zombies
    for i in range(nbZombies) :
        zombieAgents.append(ZombieAgent(zombieId))
    
    #spawn clever zombies
    for i in range(nbCleverZombies) :
        zombieAgents.append(IntelligentZombieAgent(zombieId)) 
    
def stepWorld( it = 0 ):
    global objectMap, newObjectMap, PorteBrise, Pluie, nbFoisPluie, bg

    if it % (maxFps/5) == 0:
        if random() < probPluie and Pluie == False:
            Pluie = True
            bg = pygame.image.load("assets/Monde/ciel3.jpg")


        h = getWorldHeight()
        w = getWorldWidth()
        newObjectMap = [ [ [ 0 for i in range(w) ] for j in range(h) ] for k in range(objectMapLevels) ]
        
        listeInterx = [i for i in range(w//4, 3*w//4)]
        listeIntery = [i for i in range(h//4, 3*h//4)] 
        for x in range(w):
            for y in range(h):
                # level 0
                if getObjectAt(x, y) == noObjectId and getAgentAt(x,y) == noAgentId and (x not in listeInterx or y not in listeIntery) and x >= w//2 + 1:
                    if np.random.rand() <= probGrowth:
                        setNewObjectAt(x, y, treeId)
                    else:
                        setNewObjectAt(x, y, getObjectAt(x, y)) 

                
                elif getObjectAt(x, y) == burningTreeId:
                    if Pluie : 
                        setNewObjectAt(x,y,treeId)
                    elif np.random.rand() <= probChange:
                        setNewObjectAt(x, y, burnedTreeId)
                    else:
                        setNewObjectAt(x, y, getObjectAt(x, y)) 
                
                elif getObjectAt(x, y) == burnedTreeId:
                    if random() < probRegrowth:
                        setNewObjectAt(x, y, treeId)
                    else:
                        setNewObjectAt(x, y, burnedTreeId)

                elif getObjectAt(x,y) == treeId and not Pluie:                          
                    if np.random.rand() < probIgnite:
                        setNewObjectAt(x, y, burningTreeId)
                    nonF = False
                    for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)):
                        if getObjectAt((x + neighbours[0] + worldWidth) % worldWidth,(y + neighbours[1] + worldHeight) % worldHeight) == burningTreeId:
                            setNewObjectAt(x,y,burningTreeId)
                            nonF = True
                    if nonF == False:
                        setNewObjectAt(x, y, getObjectAt(x, y)) 
                        
                            
                elif getObjectAt(x, y) == arrowId:
                    setNewObjectAt(x, y, noObjectId) 
                
                else:
                    setNewObjectAt(x, y, getObjectAt(x, y)) 

                for level in range(1, objectMapLevels):
                    setNewObjectAt(x, y, getObjectAt(x, y, level), level) 
        
        objectMap = newObjectMap
        
        ##SPAWN FOOD               
        if(it % 15 == 0):
            for i in range((len(humanAgents)-getWorldHeight())//5):
                x = randint(0, getWorldHeight()//2 - 1)
                y = randint(0, getWorldHeight() - 1)
                while(getObjectAt(x, y) != 0) :
                    x = randint(0, getWorldHeight()//2 - 1)
                    y = randint(0, getWorldHeight()-1)
                setObjectAt(x, y, foodId)

        ## Update the door
        for p in porte:
            p.verif()
        for p in porte:
            if p.type == noObjectId:
                setObjectAt(p.x, p.y, noObjectId, p.z)
                porte.remove(p) 
    
        #REGARDER SI LA PORTE EST BRISE OU PAS
        m = getWorldHeight() // 2
        n = getWorldWidth() // 2 
        if getObjectAt(m, n) == noObjectId and getObjectAt(m-1, n) == noObjectId and getObjectAt(m+1, n) == noObjectId:
            PorteBrise = True

        #print(len(porte))
                      
    return

def stepAgents(it = 0) : 
    global humanAgents, zombieAgents
    if it % (maxFps/5) == 0:
        for a in zombieAgents :
            a.move(it) 
            (x,y) = a.getPosition()
            if a.getType() == burnedZomId: 
                if a.burningDays == 0:
                    a = getAgentByPos(zombieAgents, x, y)
                    zombieAgents.remove(a)
                    setAgentAt(x, y, noAgentId)
                else:
                    a.decrementeDays()
        for a in humanAgents : 
            a.move(it)  
        

##########
## Main ##
##########
    
loadAllImages()

initWorld()
initAgents()

# game loop
it = 0
running = True
changeWall = 0

###

particle1 = ParticlePrinciple()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,3000)

###

while running: 
    
    render(it)

    stepWorld(it)
    stepAgents(it)

    # continuous stroke
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] :
        xViewOffset  = (xViewOffset - 1 + getWorldWidth() ) % getWorldWidth()
    elif keys[pygame.K_RIGHT] :
        xViewOffset = (xViewOffset + 1 ) % getWorldWidth()
    elif keys[pygame.K_DOWN] :
        yViewOffset = (yViewOffset + 1 ) % getWorldHeight()
    elif keys[pygame.K_UP] :
        yViewOffset = (yViewOffset - 1 + getWorldHeight() ) % getWorldHeight()
    
    #single stroke
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT : 
            running = False
        if event.type == KEYDOWN : 
            if event.key == K_ESCAPE : 
                running = False
            elif event.key == pygame.K_d :
                if scaleMultiplier > 0.125:
                    scaleMultiplier = scaleMultiplier / 1.25
                if scaleMultiplier < 0.125:
                    scaleMultiplier = 0.125
                resetImages() 
            elif event.key == pygame.K_p : 
                time.sleep(10)
            elif event.key == pygame.K_z :
                if scaleMultiplier < 1.0:
                    scaleMultiplier = scaleMultiplier * 1.25
                if scaleMultiplier > 1.0:
                    scaleMultiplier = 1.0
                resetImages()
            elif event.key == pygame.K_w :
                changeWall = 1 - changeWall
                if changeWall == 1:
                    id1 = transBlockId 
                    id2 = agentTransparentId

                    y = getWorldWidth() // 2
                    x = getWorldHeight() // 2
                    for i in range(0, getWorldHeight()) : 
                        for level in range(0, objectMapLevels-2): 
                            if(i not in [x, x+1, x-1]):
                                setObjectAt(y, i, id1, level)  
                                setObjectAt(y+1, i, id1, level)
                    for i in [x, x+1, x-1] : 
                        for level in range(4, objectMapLevels-2): 
                            setObjectAt(y, i, id1, level)  
                            setObjectAt(y+1, i, id1, level)  
                    
                    for i in range(0, getWorldHeight()) : 
                        #if getAgentAt(y, i, objectMapLevels-2) == ArcherAgent:
                            setAgentAt(y, i, id2, objectMapLevels-2)
                    
                else : 
                    id1 = blockId
                    id2 = archerId
                    # build the wall again
                    y = (getWorldWidth()) // 2
                    x = getWorldHeight() // 2
                    for i in range(0, getViewHeight()) : 
                        for level in range(0, objectMapLevels-2): 
                            if(i not in [x, x+1, x-1]):
                                setObjectAt(y, i, blockId, level)  
                                setObjectAt(y+1, i, blockId, level)  
                    for i in [x, x+1, x-1] : 
                        for level in range(4, objectMapLevels-2): 
                            setObjectAt(y, i, blockId, level)  
                            setObjectAt(y+1, i, blockId, level) 
                    
                    if len(humanAgents) != 0 : 
                        for i in range(0, getWorldHeight()) : 
                            #if getAgentAt(y, i, objectMapLevels-2) == agentTransparentId:
                            setAgentAt(y, i, id2, objectMapLevels-2) 
            
            elif event.key == pygame.K_l : 
                LaunchOrder = 1 
                it = -1
            elif event.key == pygame.K_s : 
                LaunchOrder = 0
<<<<<<< HEAD
            elif event.key == pygame.K_e : 
                afficheEnergie = not afficheEnergie
=======
>>>>>>> 25b55e802b45126ed2ca498648ac6c6c195b273c
        elif event.type == PARTICLE_EVENT and Pluie:
            for i in range(nbFoisPluie):
                particle1.add_particles()
            nbFoisPluie -= 100
            if(nbFoisPluie <= 0) :
                nbFoisPluie = 500
                Pluie = False
                bg = pygame.image.load("assets/Monde/ciel1.jpg")


                    
    it+=1
   
    particle1.emit()
    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps

pygame.quit()
sys.exit()
