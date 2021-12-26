import pickle
import pygame
from airlockEntities import *
from airlockUI import *


def closeWalls(walls,button):
    button.boolEnabled=False
    for wall in walls:
        wall.boolEnabled=True

def openWalls(wall,button):
    button.boolEnabled=False
    wall.boolEnabled=False


'''
.----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| |     _____    | || |     ______   | || |   _____      | |
| |    |_   _|   | || |   .' ___  |  | || |  |_   _|     | |
| |      | |     | || |  / .'   \_|  | || |    | |       | |
| |   _  | |     | || |  | |         | || |    | |   _   | |
| |  | |_' |     | || |  \ `.___.'\  | || |   _| |__/ |  | |
| |  `.___.'     | || |   `._____.'  | || |  |________|  | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'
 '''


def badCollision(player,testObject,tup): ## NO CASO DE COLIDIR COM ALGUMA COISA MÁ, TENHO QUE DAR ALGUM ESPAÇO
    if(type(testObject)==list):
        for i in testObject:
            if (badCollision(player,i,tup)):
                return(i)
    else:
        if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX)+5,int(player.floatY)-24,32-10,24),pygame.Rect(testObject.intX+2,testObject.intY+4,tup[0]-4,tup[1]))):
            player.floatVy=abs(player.floatVy)
            return(testObject)
    return(False)

def goodCollision(player,testObject): ## NO CASO DE COLIDIR COM ALGUMA COISA BOA, NÃO PRECISO
    if(type(testObject)==list):
        for i in testObject:
            if (goodCollision(player,i)):
                return(i)
    else:
        if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX),int(player.floatY)-24,32,24),pygame.Rect(testObject.intX,testObject.intY,12,24))): ##O MESMO TAMANHO FUNCIONA PARA TODAS AS COISAS BOAS, BOTOES E ELEVADORES
            return(testObject)
    return(False)

def drawList(listObj,screen):
    for obj in listObj:
        if (obj.boolEnabled):
            obj.Draw(screen)

def drawListEntity(listObj,screen,image):
    for obj in listObj:
        if (obj.boolEnabled):
            obj.Draw(screen,image)

def moveFish(listObj,dt):
    for obj in listObj:
        if(type(obj)==list):
            moveFish(obj,dt)
        else:
            obj.Move(dt)

def writeFile(data,strPath):
    file = open("levelData/"+strPath+".pckl", "wb")
    pickle.dump(data, file)
    file.close()

def readFile(strPath):
    file = open("levelData/"+strPath+".pckl", "rb")
    obj = pickle.load(file)
    file.close()
    return(obj)
