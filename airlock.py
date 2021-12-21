import pygame
class playerClass():
    def __init__(this):
        this.floatX=500
        this.floatY=534
        this.intFloorY=this.floatY
        this.floatVy=0
        this.boolEnabled=False
        this.boolJumping=False
        this.intHurt=0 #Em milésimos de segundo
        
    def NextFloor(this,intFloorY):
        this.intFloorY=intFloorY
        
    def Draw(this,screen,image):
        screen.blit(image, (int(this.floatX), int(this.floatY-24)))
        
    def Move(this,direction,dt,wall):
        newPos=this.floatX+(direction*0.15*dt)
        if(newPos<22):
            newPos=22
        elif(newPos>779-32):
            newPos=779-32
        elif(wall and newPos<77):
            newPos=77
        elif(wall and newPos>723-32):
            newPos=723-32
        this.floatX=newPos
        
    def Jump(this):
        this.floatVy=float(-0.3)
        this.boolJumping=True

    def Down(this):
        this.floatVy=abs(this.floatVy)
        
    def Fall(this,dt):
        this.floatY+=(this.floatVy*dt)
        this.floatVy+=0.001*dt

    def HandleBlocks(this,block): ##OS BLOCOS COMPORTAM-SE DE MANEIRA ESTRANHA NO JOGO NORMAL
        if(not block):
            return(False)
        if(this.floatX+16>=block.intX+12):
            return(1)
        else:
            return(-1)
        return(False)
        
class enemyClass():
    def __init__(this,intX,intY,dirX,behaviour):
        '''
        BEHAVIOUR 0 NORMAL
        BEHAVIOUR 1 VAI RAPIDO PARA A DIREITA
        BEHAVIOUR -1 VAI RAPIDO PARA A ESUQERDA'''
        this.intX=intX
        this.intY=intY
        this.dirX=dirX
        this.boolEnabled=False
        this.behaviour=behaviour
    def Draw(this,screen,image):
        screen.blit(image, (int(this.intX), int(this.intY)))
    def Move(this,dt):
        newPos=this.intX+(this.dirX*0.15*dt)
        if(newPos<77):
            newPos=77
            this.dirX=1
        elif(newPos>723-32):
            newPos=723-32
            this.dirX=-1
        if(this.dirX==1 and this.behaviour==1):
            this.dirX=2
        elif(this.dirX==-1 and this.behaviour==-1):
            this.dirX=-2
        this.intX=newPos

class tileWall():
    def __init__(this,intY):
        this.intY=intY
        this.boolEnabled=False
        
    def Draw(this,screen,image):
        screen.blit(image, (58, this.intY))

class tileBlock():
    def __init__(this,intX,intY,intFloor):
        this.intX=intX
        this.intY=intY
        this.intFloor=intFloor
        this.boolEnabled=False
    def Draw(this,screen,image):
        screen.blit(image, (this.intX, this.intY))

class tileElevator():
    def __init__(this,intX,intY,intNewY):
        this.intX=intX
        this.intY=intY
        this.intNewY=intNewY
        this.boolEnabled=False
        this.boolElevating=False
        
    def Draw(this,screen,image,image2):
        if(this.boolEnabled):
            screen.blit(image, (this.intX, this.intY)) #EVENTUALMENTE SUBSTITUIR POR UM DESENHO Q N PRECISE DE IMAGEM
        else:
            screen.blit(image2, (this.intX, this.intNewY))

    def IsElevator(this,player):
        if(this.intX==21):
            if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX),int(player.floatY),32,24),pygame.Rect(this.intX-1,this.intY-24,12,25))):
               return(True)
        elif(this.intX==741):
            if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX),int(player.floatY),32,24),pygame.Rect(this.intX+30,this.intY-24,12,25))):
               return(True)
        return(False)

    def Elevate(this,player,intNextY,dt):
        this.boolElevating=True
        newPos=this.intY-(0.2*dt)
        if(newPos<=intNextY):
            this.boolEnabled=False
            newPos=intNextY
        this.intY=newPos
        player.floatY=newPos
        player.intFloorY=newPos

class switch():
    def __init__(this,intX,intY,intFloor):
        this.intX=intX
        this.intY=intY
        this.intFloor=intFloor
        this.boolEnabled=False
    def Draw(this,screen,image):
        screen.blit(image, (this.intX, this.intY))

class bigSwitch(switch):
    def press(this,walls):
        this.boolEnabled=False
        for wall in walls:
            wall.boolEnabled=True

class smallSwitch(switch):
    def press(this,wall):
        this.boolEnabled=False
        wall.boolEnabled=False

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

'''
 _____     ____
 /      \  |  o | 
|        |/ ___\| 
|_________/     
|_|_| |_|_|
'''


pygame.init()
pygame.font.init()
kill=False

colourYellow = (188,140,76)
colourRed = (208,112,112)
colourPurple = (160,112,204)

clock=pygame.time.Clock()
player=playerClass()
floors = [534,449,361,276,189,106]
enemies = [enemyClass(140,522,1,0),enemyClass(660,437,-1,0),enemyClass(140,349,1,0),enemyClass(660,264,-1,1),enemyClass(140,177,1,-1)]
walls = [tileWall(460),tileWall(370),tileWall(283),tileWall(200),tileWall(117)]
screen = pygame.display.set_mode((800, 600))
elevators = [tileElevator(21,534,449),tileElevator(741,449,361),tileElevator(21,361,276),tileElevator(741,276,189),tileElevator(21,189,106)]
blocks = [tileBlock(562,520,0),tileBlock(207,520,0),tileBlock(562,434,1),tileBlock(207,434,1),tileBlock(207,348,2),tileBlock(562,348,2),tileBlock(207,262,3),tileBlock(562,262,3),tileBlock(207,176,4),tileBlock(562,176,4)]
bigSwitches = [bigSwitch(660,462,0),bigSwitch(140,375,1),bigSwitch(660,290,2),bigSwitch(140,203,3),bigSwitch(660,118,4)]
smallSwitches = [smallSwitch(140,462,0),smallSwitch(660,375,1),smallSwitch(140,290,2),smallSwitch(660,203,3),smallSwitch(140,118,4)]

intDir=0
intCurFloor=0 ##O PISO DE BAIXO E 0, O DE CIMA DE TUDO E O 4
intNoMoreJumping=0 ##VARIAVEL PARA PREVENIR PYGAME BRUH MOMENTS
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

while(not kill):
    
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
                boolHoldingW = True
                player.Jump()
    if (keys[pygame.K_a] and (not player.boolJumping)):
        intDir=-1
    elif (keys[pygame.K_d] and (not player.boolJumping)):
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


    
    ##DETETAR COLISOES
    if (player.intHurt > 0):
        player.intHurt-=dt
        player.floatVy=abs(player.floatVy) ##PARA CAIR
    else:
        if(badCollision(player,enemies,enemyImage)): ##DETETAR SE BATEU EM UM INIMGO
            player.intHurt=3000 ##3 SEGUNDOS
            player.floatY=player.intFloorY
        else:
            if(not(elevators[intCurFloor].boolElevating)): ##SO SE MEXE SE NAO ESTIVER EM UM ELEVADOR
                intNewDir=player.HandleBlocks(badCollision(player,blocks,blockImage))
                if(intNewDir):
                    player.floatVy=abs(player.floatVy)
                    intNoMoreJumping=50
                    player.floatVy=0.3
                    intDir=intNewDir
                player.Move(intDir,dt,walls[intCurFloor].boolEnabled)
            player.Fall(dt)
            if(player.floatY>=player.intFloorY and player.floatVy>0):
                player.floatY=player.intFloorY
                player.floatVy=0
                player.boolJumping=False

            ##SALTOS (SÓ SALTA SE NÃO ESTIVER MAGOADO)
        
        if(bigSwitches[intCurFloor].boolEnabled and goodCollision(player,bigSwitches[intCurFloor],bigSwitchImage)): ##DETETAR SE CARREGOU EM UM BOTAO GRANDE
            bigSwitches[intCurFloor].press(walls)
        
        elif(goodCollision(player,smallSwitches[intCurFloor],smallSwitchImage) and not bigSwitches[intCurFloor].boolEnabled and smallSwitches[intCurFloor].boolEnabled): ##DETETAR SE CARREGOU EM UM BOTAO PEQUENO
            smallSwitches[intCurFloor].press(walls[intCurFloor])
            if(intCurFloor<4):
                walls[intCurFloor+1].boolEnabled=False
        
        elif(not elevators[intCurFloor].boolEnabled): ##DETETAR SE O ELEVADOR ACABOU DE SUBIR
            intCurFloor+=1
            if(intCurFloor==5):
                kill = True
                ##CODIGO
        
        elif(not bigSwitches[intCurFloor].boolEnabled and not smallSwitches[intCurFloor].boolEnabled): ##DETETAR SE ESTÁ EM UM ELEVADOR
            if(elevators[intCurFloor].IsElevator(player) or elevators[intCurFloor].boolElevating):
                elevators[intCurFloor].Elevate(player,floors[intCurFloor+1],dt)



    ##MEXER OS INIMIGOS
    for enemy in enemies:
        enemy.Move(dt)

    '''
    DESENHAR
    '''
    
    ##screen.fill((255,255,255)) EU SEI QUE O .fill EXISTE, MAS PREFIRO FAZER ISTO ASSIM
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 800, 600))
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
