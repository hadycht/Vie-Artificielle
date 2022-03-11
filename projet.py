import sys
import datetime
from random import *
import math
import time

import pygame
from pygame.locals import *

import numpy as np
from abc import abstractmethod

###

# variables for initialisation 
nbAgents = 50
nbTrees = 100
nbBurningTrees = 5

probGrowth = 0
probIgnite = 0.00002
probChange = 0.02

probZombieIntelChangeDir = 0.2

###########################
## Parameters: rendering ##
###########################

# display screen dimensions
screenWidth = 1600#930
screenHeight = 1000#640

# world dimenesions (total number of cells)
worldWidth = 33#64
worldHeight = 33#64

# surface of displayed tiles (number of cells that are rendered)
viewWidth = 33#64
viewHeight = 33#64

objectMapLevels = 11 #number of levels for objectMap

scaleMultiplier = 0.40 #re-scaling of loaded images

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

    objectType.append(None)
    objectType.append(loadImage('assets/Monde/tree_E_ret.png')) # tree
    objectType.append(loadImage('assets/Monde/voxelTile_30.png')) #wall block 
    objectType.append(loadImage('assets/Monde/transparent_wall.png')) #wall block transparent
    objectType.append(loadImage('assets/Monde/voxelTile_19.png')) #just a home
    objectType.append(loadImage('assets/Monde/tree_fall_ret.png')) #tree on fire
    objectType.append(loadImage('assets/Monde/burned_tree.png')) #burned_tree
    objectType.append(loadImage('assets/Monde/wallHalf_NW_ret.png')) #border
    objectType.append(loadImage('assets/Monde/wallHalf_SE_ret.png')) #lateral border far
    objectType.append(loadImage('assets/Monde/wallHalf_NE_ret.png')) #lateral border close
    objectType.append(loadImage('assets/Monde/arrow-ret.png')) #arrow
    
    agentType.append(None)
    agentType.append(loadImage('assets/Monde/zombie_walk1.png')) #night walker 
    agentType.append(loadImage('assets/Monde/ninja.png')) #soldier
    agentType.append(loadImage('assets/Monde/archer.png')) #archer
    

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

zombieId = 1
soldierId = 2
archerId = 3

grassId = 0
rockId = 1

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

###

resetImages()

###

terrainMap = [x[:] for x in [[0] * worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]

newHeightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
newObjectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
newAgentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]

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


###########################
## CORE/USER : Rendering ##
###########################

def render( it = 0 ):
    global xViewOffset, yViewOffset
    # create the screen
    pygame.draw.rect(screen, (255,255,255), (0, 0, screenWidth, screenHeight)) # overkill - can be optimized. (most sprites are already "naturally" overwritten)

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
                if getAgentAt( xTile, yTile , level) != 0: # agent on terrain?
                    screen.blit( agentType[ getAgentAt( xTile, yTile, level ) ] , ( xScreen, yScreen - heightMultiplier*(level+1) ))
            
            
    return

############
## Agents ##
############

class Agent:
    def __init__(self,imageId):
        self.type = imageId
        self.reset()
        return
    
    @abstractmethod 
    def reset(self):
        pass

    def getPosition(self):
        return (self.x,self.y)

    def move(self, it = 0): 
        xNew = self.x
        yNew = self.y
        
        xNew = ( self.x + [-1,0,+1][randint(0,2)] + getWorldWidth() ) % getWorldWidth()
        yNew = ( self.y + [-1,0,+1][randint(0,2)] + getWorldHeight() ) % getWorldHeight()

        if getObjectAt(xNew,yNew) == 0 and getAgentAt(xNew, yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        return

    def move2(self,xNew,yNew):
        success = False
        if getObjectAt( (self.x+xNew+worldWidth)%worldWidth , (self.y+yNew+worldHeight)%worldHeight ) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt( self.x, self.y, noAgentId)
            self.x = ( self.x + xNew + worldWidth ) % worldWidth
            self.y = ( self.y + yNew + worldHeight ) % worldHeight
            setAgentAt( self.x, self.y, self.type)
            success = True
        return

    def getType(self):
        return self.type

class HumanAgent(Agent) : 
    def reset(self) : 
        self.x = randint(0,getWorldWidth()//2-1)
        self.y = randint(0,getWorldHeight()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()//2-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return

class ArcherAgent(HumanAgent) : 
    def __init__(self,imageId):
        self.type = imageId
        self.arrow = arrowId
        self.reset()
        return

    def reset(self) : 

        self.x = getWorldWidth()//2 
        self.posarrowx = self.posarrowy = self.posarrowz = 0
        self.y = randint(1,getWorldHeight()-2)
        self.z =objectMapLevels-2 
        self.destarrowx = 0
        self.angle = 0
        while getAgentAt(self.x,self.y,self.z) != 0 :
            self.y = randint(0,getWorldHeight()-1)
    
        setAgentAt(self.x, self.y, self.type, self.z)
        return

    def getPosition(self) :
        return (self.x,self.y, self.z)

    def tirage(self):
        
        (self.posarrowx, self.posarrowy, self.posarrowz) = self.getPosition()
        self.posarrowx+=1
        setObjectAt(self.posarrowx, self.posarrowy, arrowId, self.posarrowz) 
        self.destarrowx = randint(getWorldHeight()//2 + 1, getWorldHeight()-1) 
        self.angle = np.arcsin(math.sin(self.destarrowx / (math.sqrt(self.z*self.z + (self.destarrowx-self.x)*(self.destarrowx-self.x)))))
        self.arrow = pygame.transform.rotate(objectType[arrowId], -math.degrees(self.angle))

    def move(self, it = 0):

        if it%50==0 :
            self.tirage()

        else : 
            if self.posarrowx < self.destarrowx : 
                setObjectAt(self.posarrowx, self.posarrowy, noObjectId, self.posarrowz)
                self.posarrowz = self.posarrowz - (self.posarrowz//(self.destarrowx - self.posarrowx))
                self.posarrowx+=1
                setObjectAt(self.posarrowx, self.posarrowy, arrowId, self.posarrowz) 
            
            
            
            


        
class ZombieAgent(Agent) :
    def reset(self) : 
        self.x = randint(getWorldWidth()//2+1,getWorldWidth()-1)
        self.y = randint(0,getWorldHeight()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(getWorldWidth()//2+1,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return

class IntelligentZombieAgent(ZombieAgent) :
    def move(self, it = 0) :
        xNew = self.x
        yNew = self.y
        
        if random() > probZombieIntelChangeDir: # vers le mur
            xNew = self.x - 1 
        else : 
            xNew = ( self.x + [-1,0,+1][randint(0,2)] + getWorldWidth() ) % getWorldWidth()
            yNew = ( self.y + [-1,0,+1][randint(0,2)] + getWorldHeight() ) % getWorldHeight()

        if getObjectAt(xNew,yNew) == 0 and getAgentAt(xNew, yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        return

agents = []
#archeragents = []

######################
## Initialise world ##
######################

def initWorld() : 
    # make a border
    for i in range(getWorldHeight()) :
        setObjectAt(0, i, borderId)

    # make lateral borders
    for r in range(getWorldWidth()//2) :
        setObjectAt(r, 0, latBorderFarId)
        setObjectAt(r, getWorldHeight() - 1, latBorderCloseId)
    
    # build the wall
    y = (getWorldWidth()) // 2
    for i in range(0, getViewHeight()) : 
        for level in range(0, objectMapLevels-2):
            setObjectAt(y, i, blockId, level)  
            setObjectAt(y+1, i, blockId, level)  
        setTerrainAt(y, i, rockId)
        setTerrainAt(y+1, i, rockId)

    #spawn the houses
    # add a pyramid-shape building with a tree on top
    building2TerrainMap = [
    [ 0, 4, 4, 4, 4, 4, 0 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 4, 4, 4, 4, 4, 4, 4 ],
    [ 0, 4, 4, 4, 4, 4, 0 ]
    ]
    building2HeightMap = [
    [ 0, 1, 1, 1, 1, 1, 0 ],
    [ 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 2, 2, 2, 2, 2, 1 ],
    [ 1, 2, 3, 3, 3, 2, 1 ],
    [ 1, 2, 3, 4, 3, 2, 1 ],
    [ 1, 2, 3, 3, 3, 2, 1 ],
    [ 1, 2, 2, 2, 2, 2, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1 ],
    [ 0, 1, 1, 1, 1, 1, 0 ]
    ]
    x_offset = 4
    y_offset = 13
    for x in range( len( building2TerrainMap[0] ) ):
        for y in range( len( building2TerrainMap ) ):
            setObjectAt( x+x_offset, y+y_offset, building2TerrainMap[y][x] , building2HeightMap[y][x]-1)
            
    setObjectAt( x_offset+3, y_offset+4, treeId , 4)
    setObjectAt( x_offset+10, y_offset+10, homeId)
    
    
    #setObjectAt(10,10,homeId)

    #make trees
    h = getWorldHeight()
    w = getWorldWidth()
    for i in range(nbTrees) :
        #x = choice([i for i in range((w-1)//2, w-1] )
        # [(19,4),(18,3),()][randint(0,le)]
        y = choice([i for i in range(0, h-1) if i not in [j for j in range(h//4, 3*h//4)]])
        x = randint(w//2+1, w-1)
        #y = randint(getWorldHeight()//4,getWorldHeight()-getWorldHeight()//4)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0 or getAgentAt(x,y) != 0:
            x = randint(w//2+1, w-1)
            y = choice([i for i in range(0, h-1) if i not in [j for j in range(h//4, 3*h//4)]])
        setObjectAt(x,y,treeId)

    for i in range(nbBurningTrees):
        x = randint(w//2+1, w-1)
        y = choice([i for i in range(0, h-1) if i not in [j for j in range(h//4, 3*h//4)]])
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0 or getAgentAt(x,y) != 0:
            x = randint(w//2+1, w-1)
            y = choice([i for i in range(0, h-1) if i not in [j for j in range(h//4, 3*h//4)]])
        setObjectAt(x,y,burningTreeId)
    return

def initAgents() :
    # spawn the agents
    for i in range(nbAgents) : 
        agents.append(IntelligentZombieAgent(zombieId))
        agents.append(HumanAgent(soldierId))

    for i in range(5):     
        agents.append(ArcherAgent(archerId)) 
    


def stepWorld( it = 0 ):
    global objectMap, newObjectMap

    if it % (maxFps/10) == 0:
        newObjectMap = objectMap
        for x in range(worldWidth):
            for y in range(worldHeight):
                if x >= worldWidth // 2: # remove if we want trees everywhere
                    if getObjectAt(x, y) == noObjectId:
                        if np.random.rand() < probGrowth:
                            setNewObjectAt(x, y, treeId)

                    elif getObjectAt(x, y) == burningTreeId:
                        if np.random.rand() < probChange:
                            setNewObjectAt(x, y, burnedTreeId)

                    elif getObjectAt(x,y) == treeId:
                        if np.random.rand() < probIgnite:
                            setNewObjectAt(x, y, burningTreeId)
                        for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1),(1,-1),(-1,1),(1,1),(-1,-1)):
                            if getObjectAt((x+neighbours[0]+worldWidth) % worldWidth,(y+neighbours[1]+worldHeight) % worldHeight) == burningTreeId:
                                setNewObjectAt(x,y,burningTreeId)
        objectMap = newObjectMap                        
    return

def stepAgents(it = 0) : 
    if it % (maxFps/5) == 0:
        for a in agents : 
            a.move(it)            
            #a.move2(getWorldHeight()//2, getWorldWidth()//2)
            

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
            elif event.key == pygame.K_z :
                if scaleMultiplier < 1.0:
                    scaleMultiplier = scaleMultiplier * 1.25
                if scaleMultiplier > 1.0:
                    scaleMultiplier = 1.0
                resetImages()
            elif event.key == pygame.K_w :
                changeWall = 1 - changeWall
                if changeWall == 1:
                    id = transBlockId
                else:
                    id = blockId
                y = (getWorldWidth())//2
                for i in range(0, getViewHeight()) : 
                    for level in range(0, objectMapLevels-2):
                        setObjectAt(y, i, id, level) 
                        setObjectAt(y+1, i, id, level)  
    it+=1
    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps

pygame.quit()
sys.exit()
