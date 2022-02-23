import sys
import datetime
from random import *
import math
import time

import pygame
from pygame.locals import *

nbAgents = 10

# display screen dimensions
screenWidth = 1400
screenHeight = 900

#world dimenesions

worldWidth = 64
worldHeight = 64

#the view

viewWidth = 64
viewHeight = 64

#number of levels
objectMapLevels = 8

#re-scaling of loaded images
scaleMultiplier = 0.25

# set scope of displayed tiles
xViewOffset = 0
yViewOffset = 0

maxFps = 30

###########################
## SETTING UP SDL/Pygame ##
###########################

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption('Game of Thrones') 


#############################
## Partie image management ##
#############################


def loadImage(filename) : 
    global tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier
    image = pygame.image.load(filename).convert_alpha() #image type Surface
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*scaleMultiplier), int(tileTotalHeightOriginal*scaleMultiplier)))
    return image

def loadAllImages() : 
    global tileType, objectType, agentType

    tileType = []
    objectType = []
    agentType = []

    tileType.append(loadImage('assets/Monde/platformerTile_48_ret.png')) #grass

    objectType.append(None)
    objectType.append(None)
    objectType.append(loadImage('assets/Monde/voxelTile_30.png')) #wall block 
    objectType.append(loadImage('assets/Monde/e.png')) #wall block transparent
    objectType.append(loadImage('assets/Monde/tower_39.png')) #just a home



    agentType.append(None)
    agentType.append(loadImage('assets/Monde/zombie_walk1.png')) #night walker 
    agentType.append(loadImage('assets/Monde/soldier_cheer1.png')) #soldier



def resetImages() : 
    global tileTotalWidth, tileTotalHeight, tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier, heightMultiplier, tileVisibleHeight
    tileTotalWidth = tileTotalWidthOriginal * scaleMultiplier  # width of tile image, as stored in memory
    tileTotalHeight = tileTotalHeightOriginal * scaleMultiplier # height of tile image, as stored in memory
    tileVisibleHeight = tileVisibleHeightOriginal * scaleMultiplier # height "visible" part of the image, as stored in memory
    heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight
    loadAllImages()
    return

###############################
## Core : Objects parametres ##
###############################

tileTotalWidthOriginal = 111  # width of tile image
tileTotalHeightOriginal = 128 # height of tile image
tileVisibleHeightOriginal = 64 # height "visible" part of the image, i.e. top part without subterranean part


###############################

tileType = [] 
objectType = []
agentType = []


noObjectId = noAgent = 0
zombieId = 1
soldierId = 2
grassId = 0
blockId = 2
transBlockId = 3
homeId = 4

###
resetImages()

####
terrainMap = [x[:] for x in [[0] * worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 3*tileTotalHeight # border. Could be 0.

####

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

def getAgentAt(x,y):
    return agentMap[y][x]

def setAgentAt(x,y,type):
    agentMap[y][x] = type


def render( it = 0 ):
    global xViewOffset, yViewOffset

    pygame.draw.rect(screen, (0,0,0), (0, 0, screenWidth, screenHeight), 0) # overkill - can be optimized. (most sprites are already "naturally" overwritten)
    #pygame.display.update()

    for y in range(getViewHeight()):
        for x in range(getViewWidth()):
            # assume: north-is-upper-right

            xTile = ( xViewOffset + x + getWorldWidth() ) % getWorldWidth()
            #print(xTile)
            yTile = ( yViewOffset + y + getWorldHeight() ) % getWorldHeight()
            height = getHeightAt( xTile , yTile ) * heightMultiplier

            xScreen = xScreenOffset + x * tileTotalWidth / 2 - y * tileTotalWidth / 2
            yScreen = yScreenOffset + y * tileVisibleHeight / 2 + x * tileVisibleHeight / 2 - height
            #print(getTerrainAt(xTile, yTile))
            screen.blit( tileType[ getTerrainAt( xTile , yTile ) ] , (xScreen, yScreen)) # display terrain
            for level in range(objectMapLevels):
                if getObjectAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit(objectType[ getObjectAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) )) 
            
            if getAgentAt( xTile, yTile ) != 0: # agent on terrain?
                screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
            
    return

class BasicAgent:

    def __init__(self,imageId):
        self.type = imageId
        self.reset()
        return

    def reset(self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return

    def getPosition(self):
        return (self.x,self.y)

    def move(self):
        xNew = self.x
        yNew = self.y
        if random() < 0.5:
            xNew = ( self.x + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth()
        else:
            yNew = ( self.y + [-1,+1][randint(0,1)] + getWorldHeight() ) % getWorldHeight()
        if getObjectAt(xNew,yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        if verbose == True:
            print ("agent of type ",str(self.type),"located at (",self.x,",",self.y,")")
        return

    def move2(self,xNew,yNew):
        success = False
        if getObjectAt( (self.x+xNew+worldWidth)%worldWidth , (self.y+yNew+worldHeight)%worldHeight ) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt( self.x, self.y, noAgentId)
            self.x = ( self.x + xNew + worldWidth ) % worldWidth
            self.y = ( self.y + yNew + worldHeight ) % worldHeight
            setAgentAt( self.x, self.y, self.type)
            success = True
        if verbose == True:
            if success == False:
                print ("agent of type ",str(self.type)," cannot move.")
            else:
                print ("agent of type ",str(self.type)," moved to (",self.x,",",self.y,")")
        return

    def getType(self):
        return self.type

agents = []


def initWorld() : 
    y = (getWorldWidth())//2
    for i in range(0, getViewHeight()) : 
        for level in range(0, objectMapLevels):
            setObjectAt(y, i, blockId, level)  
    for i in range(nbAgents) : 
        agents.append(BasicAgent(zombieId))
        agents.append(BasicAgent(soldierId)) 
    
    setObjectAt(24,32,homeId)

    
loadAllImages() 
initWorld()
it = 0
running = True
changeWall = 0
while running: 

    render(it)
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
        if event.type == QUIT : 
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
                    for level in range(0, objectMapLevels):
                        setObjectAt(y, i, id, level)  

                
    it+=1
    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps


pygame.quit()
sys.exit()