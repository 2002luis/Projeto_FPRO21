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


def badCollision(player,testObject,image): ## NO CASO DE COLIDIR COM ALGUMA COISA MÁ, TENHO QUE DAR ALGUM ESPAÇO
    if(type(testObject)==list):
        for i in testObject:
            if (badCollision(player,i,image)):
                return(i)
    else:
        if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX)+5,int(player.floatY)-24,32-10,24),pygame.Rect(testObject.intX+2,testObject.intY+4,image.get_width()-4,image.get_height()))):
            player.floatVy=abs(player.floatVy)
            return(testObject)
    return(False)

def goodCollision(player,testObject,image): ## NO CASO DE COLIDIR COM ALGUMA COISA BOA, NÃO PRECISO
    if(type(testObject)==list):
        for i in testObject:
            if (goodCollision(player,i,image)):
                return(i)
    else:
        if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX),int(player.floatY)-24,32,24),pygame.Rect(testObject.intX,testObject.intY,12,24))):
            return(testObject)
    return(False)

def drawList(listObj,screen,image):
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
'''
 _____     ____
 /      \  |  o | 
|        |/ ___\| 
|_________/     
|_|_| |_|_|
'''

pygame.mixer.init() ##MUSICA E SONS
pygame.init()
pygame.display.set_caption("Airlock da Wish")
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

##LER O NIVEL DE UM FICHEIRO
data=readFile("loadedLevel")

enemies=data[0]
blocks=data[1]
bigSwitches=data[2]
smallSwitches=data[3]

intDir=0
intCurFloor=0 ##O PISO DE BAIXO E 0, O DE CIMA DE TUDO E O 4
intNoMoreJumping=0 ##VARIAVEL PARA PREVENIR PYGAME BRUH MOMENTS
intTimeLeft=50000 ##50 SEGUNDOS, O LIMITE DE TEMPO DO JOGO
boolHoldingW=False

##IMAGENS
levelImage=pygame.image.load("images/mundoVazio.png")
blockImage=pygame.image.load("images/block.png")
elevatorImage=pygame.image.load("images/elevator.png")
elevatorImage2=pygame.image.load("images/elevator2.png")
wallImage=pygame.image.load("images/wall.png")
playerImage=pygame.image.load("images/playerChar.png")
playerFallenImage=pygame.image.load("images/playerCharHurt.png")
bigSwitchImage=pygame.image.load("images/bigSwitch.png")
smallSwitchImage=pygame.image.load("images/smallSwitch.png")
enemyImage=pygame.image.load("images/enemyChar.png")
mainMenuImage=pygame.image.load("images/mainMenu.png")
victoryRoyaleImage=pygame.image.load("images/victoryRoyale.png")
gameOverImage=pygame.image.load("images/gameOver.png")
peixes=[pygame.image.load("images/peixe1.png"),pygame.image.load("images/peixe2.png"),pygame.image.load("images/peixe3.png"),pygame.image.load("images/inimigoDoJCL.png")]

##SONS
buttonSound = pygame.mixer.Sound("sound/button.ogg")
elevatorSound = pygame.mixer.Sound("sound/elevator.ogg")
enemyHitSound = pygame.mixer.Sound("sound/enemyHit.ogg")
epicWinSound = pygame.mixer.Sound("sound/epicWin.ogg")
gameOverSound = pygame.mixer.Sound("sound/gameOver.ogg")
jumpSound = pygame.mixer.Sound("sound/jump.ogg")
menuMusicSound = pygame.mixer.Sound("sound/menuMusic.ogg")
walkSound = pygame.mixer.Sound("sound/walk.ogg")
wallSound = pygame.mixer.Sound("sound/wall.ogg")
victoryRoyaleSound = pygame.mixer.Sound("sound/epicWin.ogg")
gameOverSound = pygame.mixer.Sound("sound/gameOver.ogg")

##CHANNELS DE SOM
jumpChannel = pygame.mixer.Channel(0)
walkChannel = pygame.mixer.Channel(1)
mainMenuChannel = pygame.mixer.Channel(2)
gameOverChannel = pygame.mixer.Channel(3)

##ENQUANTO NAO TIVER UM ECRA DE TITULO VOU INICIALIZAR TUDO AQUI
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




boolDebugger=False
boolMainMenu=True
boolTempImmunity=True ##O JOGO FICA PARADO ATÉ AO PRIMEIRO MOVIMENTO (COMO NO ORIGINAL)
boolVictoryRoyale=False ##SÓ VAI IMPORTAR DEPOIS DE ACABAR O PRIMEIRO JOGO
intTimeLeft=49999
timeMainMenu=200

while(not kill):
    if(boolMainMenu): ##MENU!
        if(not gameOverChannel.get_busy()):
            dt=clock.tick()
            if(not mainMenuChannel.get_busy()):
                mainMenuChannel.play(menuMusicSound)
            '''
            EVENTOS
            '''
            boolTempImmunity=True
            if(timeMainMenu>0):
                timeMainMenu-=dt
            events = pygame.event.get()
            for event in events:
                if(event.type == pygame.KEYDOWN and timeMainMenu<=0):
                    boolMainMenu=False
                elif(event.type == pygame.QUIT):
                    kill=True

            '''
            "FÍSICA" (peixinhos!)
            '''

            moveFish(fishes,dt)

            '''
            DESENHAR
            '''
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 800, 600))
            screen.blit(mainMenuImage,(0,0))
            for i in range(len(fishes)):
                for j in range(len(fishes[i])):
                    fishes[i][j].Draw(screen,peixes[i])
        else:
            if(boolVictoryRoyale):
                screen.blit(victoryRoyaleImage, (0, 0))
            else:
                screen.blit(gameOverImage, (0, 0))
            ##O PYGAME.DISPLAY.FLIP() ESTÁ NO FIM DE TUDO, FORA DOS IFS E ELSES
    else:
        '''
        EVENTOS
        '''
        
        click=pygame.mouse.get_pressed() ##FICA PRESO SE EU NAO ESCREVER ISTO
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                kill=True
            if (event.type == pygame.KEYUP):
                if (event.key==pygame.K_w):
                    boolHoldingW=False
            elif (event.type == pygame.KEYDOWN):
                if (event.key==pygame.K_w and intNoMoreJumping<=0 and (not player.boolJumping) and (not boolHoldingW) and player.intHurt<=0):
                    boolTempImmunity = False
                    boolHoldingW = True
                    player.Jump()
                    jumpChannel.play(jumpSound)
        if (keys[pygame.K_a] and (not player.boolJumping)):
            boolTempImmunity = False
            intDir=-1
        elif (keys[pygame.K_d] and (not player.boolJumping)):
            boolTempImmunity = False
            intDir=1
        elif (not player.boolJumping):
            intDir=0

        if (keys[pygame.K_j]):
            player.floatX=0
            player.floatY=24
        if (keys[pygame.K_l]):
            boolDebugger=True
        if (keys[pygame.K_k]):
            boolDebugger=False
        if (boolDebugger):
            player.floatX=pygame.mouse.get_pos()[0]
            player.floatY=pygame.mouse.get_pos()[1]
        
        '''    
        FÍSICA
        '''

        dt=clock.tick()


        
        intNoMoreJumping-=dt ##NO MORE JUMPING! NO MORE SPACEBAR. NO MORE JUMPING INTO A BLOCK BACKWARDS. NO MORE TROLLS. YOU BEEN BLOCKED.

        if (not boolTempImmunity):
            intTimeLeft-=dt
        
        ##DETETAR COLISOES
        if (player.intHurt > 0):
            player.intHurt-=dt
            player.floatVy=abs(player.floatVy) ##PARA CAIR
        else:
            if(badCollision(player,enemies,enemyImage) and not boolTempImmunity): ##DETETAR SE BATEU EM UM INIMGO
                player.intHurt=3000 ##3 SEGUNDOS
                player.floatY=player.intFloorY
                enemyHitSound.play()
            else:
                if(not(elevators[intCurFloor].boolElevating)): ##SO SE MEXE SE NAO ESTIVER EM UM ELEVADOR
                    intNewDir=player.HandleBlocks(badCollision(player,blocks,blockImage),intDir)
                    if(intNewDir):
                        player.floatVy=abs(player.floatVy)
                        intNoMoreJumping=50
                        player.floatVy=0.3
                        intDir=intNewDir
                        wallSound.play()
                    elif(intDir!=0 and player.floatY==player.intFloorY and not walkChannel.get_busy()):
                        walkChannel.play(walkSound)
                    player.Move(intDir,dt,walls[intCurFloor].boolEnabled)
                    
                player.Fall(dt)
                if(player.floatY>=player.intFloorY and player.floatVy>0):
                    player.floatY=player.intFloorY
                    player.floatVy=0
                    player.boolJumping=False

                ##SALTOS (SÓ SALTA SE NÃO ESTIVER MAGOADO)
            
            if(bigSwitches[intCurFloor].boolEnabled and goodCollision(player,bigSwitches[intCurFloor],bigSwitchImage)): ##DETETAR SE CARREGOU EM UM BOTAO GRANDE
                bigSwitches[intCurFloor].press(walls)
                buttonSound.play()
            
            elif(goodCollision(player,smallSwitches[intCurFloor],smallSwitchImage) and not bigSwitches[intCurFloor].boolEnabled and smallSwitches[intCurFloor].boolEnabled): ##DETETAR SE CARREGOU EM UM BOTAO PEQUENO
                smallSwitches[intCurFloor].press(walls[intCurFloor])
                if(intCurFloor<4):
                    walls[intCurFloor+1].boolEnabled=False
                buttonSound.play()
            
            elif(not elevators[intCurFloor].boolEnabled): ##DETETAR SE O ELEVADOR ACABOU DE SUBIR
                intCurFloor+=1
                if(intCurFloor==5):
                    boolMainMenu = True
                    intTimeLeft = 49999
                    timeMainMenu = 1000
                    gameOverChannel.play(victoryRoyaleSound)
                    boolVictoryRoyale=True
                    ##RESET AS VARIAVEIS PARA UM JOGO NOVO
                    fishes = [[fish(175,310,1,0.15)],[fish(200,404,-1,0.23),fish(300,404,-1,0.23),fish(400,404,-1,0.23)],[fish(600,500,1,0.05)],[fish(100,586,-1,0.005),fish(300,586,-1,0.005),fish(500,586,-1,0.005),fish(700,586,-1,0.005),fish(-26,586,-1,0.005)]]
                    intDir=0
                    intCurFloor=0 ##O PISO DE BAIXO E 0, O DE CIMA DE TUDO E O 4
                    intNoMoreJumping=0 ##VARIAVEL PARA PREVENIR PYGAME BRUH MOMENTS
                    boolHoldingW=False
                    for wall in walls:
                        wall.boolEnabled=True
                    for i in range(len(elevators)):
                        elevators[i].boolEnabled=True
                        elevators[i].boolElevating=False
                        elevators[i].intY=floors[i]
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
                    player=playerClass()
                    enemies=data[0] ##PARA OS INIMIGOS VOLTAREM AS POSIÇOES INICIAIS
            
            elif(not bigSwitches[intCurFloor].boolEnabled and not smallSwitches[intCurFloor].boolEnabled): ##DETETAR SE ESTÁ EM UM ELEVADOR
                if(elevators[intCurFloor].IsElevator(player) or elevators[intCurFloor].boolElevating):
                    elevators[intCurFloor].Elevate(player,floors[intCurFloor+1],dt)
                    elevatorSound.play()

            if(4-(intTimeLeft//10000)>intCurFloor): ##SE A ÁGUA TIVER SUBIDO PARA CIMA DELE E ELE MORRER
                boolMainMenu = True
                intTimeLeft = 49999
                timeMainMenu = 1000
                gameOverChannel.play(gameOverSound)
                boolVictoryRoyale=False
                ##RESET AS VARIAVEIS PARA UM JOGO NOVO
                fishes = [[fish(175,310,1,0.15)],[fish(200,404,-1,0.23),fish(300,404,-1,0.23),fish(400,404,-1,0.23)],[fish(600,500,1,0.05)],[fish(100,586,-1,0.005),fish(300,586,-1,0.005),fish(500,586,-1,0.005),fish(700,586,-1,0.005),fish(-26,586,-1,0.005)]]
                intDir=0
                intCurFloor=0 ##O PISO DE BAIXO E 0, O DE CIMA DE TUDO E O 4
                intNoMoreJumping=0 ##VARIAVEL PARA PREVENIR PYGAME BRUH MOMENTS
                boolHoldingW=False
                for wall in walls:
                    wall.boolEnabled=True
                for i in range(len(elevators)):
                    elevators[i].boolEnabled=True
                    elevators[i].boolElevating=False
                    elevators[i].intY=floors[i]
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
                player=playerClass()
                enemies=data[0] ##PARA OS INIMIGOS VOLTAREM AS POSIÇOES INICIAIS


        ##MEXER OS INIMIGOS
        for enemy in enemies:
            enemy.Move(dt)

        '''
        DESENHAR
        '''
        
        ##screen.fill((255,255,255)) EU SEI QUE O .fill EXISTE, MAS PREFIRO FAZER ISTO ASSIM
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 800, 600))
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(0, floors[4-(intTimeLeft//10000)], 800, 600))
        

        screen.blit(levelImage, (0,0))

        drawList(walls,screen,wallImage)
        ##drawList(elevators,screen,elevatorImage)
        drawList(bigSwitches,screen,bigSwitchImage) ##NÃO QUERO ESTAR A FAZER UMA IMAGEM PARA CADA INSTANCIA DA CLASSE PQ ASSIM IA ESTAR A TER UM MONTE DE VARIAVEIS Q ERAM TODAS A MESMA IMAGEM
        drawList(smallSwitches,screen,smallSwitchImage)
        drawList(blocks,screen,blockImage)
        drawList(enemies,screen,enemyImage)

        for elevator in elevators:
            elevator.Draw(screen,elevatorImage,elevatorImage2)
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
        
        if (player.intHurt>0):
            player.Draw(screen,playerFallenImage)
        else:
            player.Draw(screen,playerImage)
    
        
    pygame.display.flip()
pygame.quit()
