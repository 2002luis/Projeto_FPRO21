import pickle
import pygame
from airlockEntities import *
from airlockUI import *
from airlockFuncs import *
'''
 _____     ____
 /      \  |  o | 
|        |/ ___\| 
|_________/     
|_|_| |_|_|
'''

pygame.mixer.init() ##MUSICA E SONS
pygame.init()
pygame.display.set_caption("Criador de Níveis para o Airlock da Wish")
icon=pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
pygame.font.init()
kill=False

colourYellow = (188,140,76)
colourRed = (208,112,112)
colourPurple = (160,112,204)

screen = pygame.display.set_mode((800, 600))
clock=pygame.time.Clock()
player=playerClass()
floors = [534,449,361,276,189,106]
walls = [tileWall(460),tileWall(370),tileWall(283),tileWall(200),tileWall(117)]
elevators = [tileElevator(21,534,449),tileElevator(741,449,361),tileElevator(21,361,276),tileElevator(741,276,189),tileElevator(21,189,106)]
fishes = [[fish(175,310,1,0.15)],[fish(200,404,-1,0.23),fish(300,404,-1,0.23),fish(400,404,-1,0.23)],[fish(600,500,1,0.05)],[fish(100,586,-1,0.005),fish(300,586,-1,0.005),fish(500,586,-1,0.005),fish(700,586,-1,0.005),fish(-26,586,-1,0.005)]]

'''
enemies = [enemyClass(100,522,1,0),enemyClass(700,437,-1,0),enemyClass(100,349,1,0),enemyClass(700,264,-1,1),enemyClass(100,177,1,-1)]
blocks = [tileBlock(562,520,0),tileBlock(207,520,0),tileBlock(562,434,1),tileBlock(207,434,1),tileBlock(207,348,2),tileBlock(562,348,2),tileBlock(207,262,3),tileBlock(562,262,3),tileBlock(207,176,4),tileBlock(562,176,4)]
bigSwitches = [bigSwitch(660,462,0),bigSwitch(140,375,1),bigSwitch(660,290,2),bigSwitch(140,203,3),bigSwitch(660,118,4)]
smallSwitches = [smallSwitch(140,462,0),smallSwitch(660,375,1),smallSwitch(140,290,2),smallSwitch(660,203,3),smallSwitch(140,118,4)]

writeFile([enemies,blocks,bigSwitches,smallSwitches],"loadedLevel")
'''

enemies = []
blocks = []
bigSwitches = [bigSwitch(660,462,0),bigSwitch(140,375,1),bigSwitch(660,290,2),bigSwitch(140,203,3),bigSwitch(660,118,4)]
smallSwitches = [smallSwitch(140,462,0),smallSwitch(660,375,1),smallSwitch(140,290,2),smallSwitch(660,203,3),smallSwitch(140,118,4)]

boolLmb=False
intSelected = 0

##IMAGENS
levelImage=pygame.image.load("images/mundoVazio.png")
blockImage=pygame.image.load("images/block.png")
##elevatorImage=pygame.image.load("images/elevator.png")
##elevatorImage2=pygame.image.load("images/elevator2.png")
##wallImage=pygame.image.load("images/wall.png")
playerImage=pygame.image.load("images/playerChar.png")
playerFallenImage=pygame.image.load("images/playerCharHurt.png")
bigSwitchImage=pygame.image.load("images/bigSwitch.png")
smallSwitchImage=pygame.image.load("images/smallSwitch.png")
enemyImage=pygame.image.load("images/enemyChar.png")
enemyImage2=pygame.image.load("images/enemyChar2.png")
enemyImage3=pygame.image.load("images/enemyChar3.png")
mainMenuImage=pygame.image.load("images/mainMenu.png")
victoryRoyaleImage=pygame.image.load("images/victoryRoyale.png")
gameOverImage=pygame.image.load("images/gameOver.png")
peixes=[pygame.image.load("images/peixe1.png"),pygame.image.load("images/peixe2.png"),pygame.image.load("images/peixe3.png"),pygame.image.load("images/inimigoDoJCL.png")]

buttons = [button(20,10,0,smallSwitchImage),button(80,10,1,bigSwitchImage),button(140,10,2,enemyImage),button(200,10,3,enemyImage2),button(260,10,4,enemyImage3),button(320,10,5,blockImage),button(750,10,6,None)]

for wall in walls:
    wall.boolEnabled=True
for elevator in elevators:
    elevator.boolEnabled=True
for block in blocks:
    block.boolEnabled=True
for switch in bigSwitches:
    switch.boolEnabled=True
for switch in smallSwitches:
    switch.boolEnabled=True
for enemy in enemies:
    enemy.boolEnabled=True
player.boolEnabled=True
player.boolFloor=False

##DESCOBRIR O NOME DO FICHEIRO NOVO
n = 1
strPath = str()
while(strPath == str()):
    try:
        readFile("level"+str(n))
        n+=1
    except:
        strPath = "level"+str(n)

##FICHEIRO
font = pygame.font.Font('consolas.ttf', 32)
fileText = font.render(strPath+".pckl", True, (188,140,76))
fileRect = fileText.get_rect()
fileRect.center = (700, 80)

while(not kill):
    '''
    EVENTOS
    '''
        
    click=pygame.mouse.get_pressed() ##FICA PRESO SE EU NAO ESCREVER ISTO
    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            kill=True
        if event.type == pygame.MOUSEBUTTONUP:
              pos = pygame.mouse.get_pos()
              boolLmb=True

        
    '''    
    "FÍSICA"
    '''

    if(boolLmb):
        boolLmb=False
        for button in buttons:
            if(button.isPressed(pos)):
                intSelected=button.intType
                if(intSelected==6):
                    writeFile([enemies,blocks,bigSwitches,smallSwitches],strPath)
                    writeFile([enemies,blocks,bigSwitches,smallSwitches],"loadedLevel")
                    kill=True
        levelInfo=levelMakerInfo(pos[0],pos[1])
        if(levelInfo):
            if(intSelected==0): ##EU SEI QUE PODIA FAZER ISTO COM ARRAYS EM VEZ DE IFS. MAS AGORA NÃO VOU ESTAR A MUDAR O CÓDIGO TODO. NEM É QUE ATRASE MUITO, É UMA COISA QUE QUASE NUNCA SE USA.
                smallSwitches[levelInfo[2]].intX=pos[0]
            elif(intSelected==1):
                bigSwitches[levelInfo[2]].intX=pos[0]
            elif(intSelected!=5):
                intDir=1
                if(pos[0]>=400):
                    intDir=-1
                enemies.append(enemyClass(pos[0],levelInfo[1]-12,intDir,[0,1,-1][intSelected-2]))
                enemies[len(enemies)-1].boolEnabled=True
            else:
                blocks.append(tileBlock(pos[0],levelInfo[1]-15,levelInfo[2]))
                blocks[len(blocks)-1].boolEnabled=True




    '''
    DESENHAR
    '''
    ##screen.fill((255,255,255)) EU SEI QUE O .fill EXISTE, MAS PREFIRO FAZER ISTO ASSIM
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 800, 600))
        

    screen.blit(levelImage, (0,0))

    drawList(walls,screen)
    ##drawList(elevators,screen,elevatorImage)
    drawList(bigSwitches,screen) ##NÃO QUERO ESTAR A FAZER UMA IMAGEM PARA CADA INSTANCIA DA CLASSE PQ ASSIM IA ESTAR A TER UM MONTE DE VARIAVEIS Q ERAM TODAS A MESMA IMAGEM
    drawList(smallSwitches,screen)
    drawList(blocks,screen)
        
    drawListEntity(enemies,screen,enemyImage)

    for elevator in elevators:
        elevator.Draw(screen)
        '''
        for wall in walls:
            if (wall.boolEnabled):
                wall.Draw(screen,wallImage)
        
        for elevator in elevators:
            if (elevator.boolEnabled):
                elevator.Draw(screen,elevatorImage)

        for switch in bigSwitches:
            if (switch.boolEnabled):
                switch.Draw(screen,bigSwitchImage)
        for switch in smallSwitches:
            if (switch.boolEnabled):
                switch.Draw(screen,smallSwitchImage)
        
        for block in blocks:
            block.Draw(screen,blockImage)

        for enemy in enemies:
            enemy.Draw(screen,enemyImage)
        '''
        
    player.Draw(screen,playerImage)

    ##PARTE DE FAZER O NIVEL
    for button in buttons:
        button.Draw(screen,intSelected)


    screen.blit(fileText, fileRect)
    pygame.display.flip()
pygame.quit()
