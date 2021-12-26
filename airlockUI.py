import pygame

class tileWall():
    def __init__(this,intY):
        this.intY=intY
        this.boolEnabled=False
        
    def Draw(this,screen):
        ##screen.blit(image, (58, this.intY))
        pygame.draw.rect(screen, (160,112,204), pygame.Rect(59, this.intY, 18, 80))
        pygame.draw.rect(screen, (160,112,204), pygame.Rect(59+664, this.intY, 18, 80))

class tileBlock():
    def __init__(this,intX,intY,intFloor):
        this.intX=intX
        this.intY=intY
        this.intFloor=intFloor
        this.boolEnabled=False
    def Draw(this,screen):
        ##screen.blit(image, (this.intX, this.intY))
        pygame.draw.rect(screen, (160,112,204), pygame.Rect(this.intX+8, this.intY, 4, 15))

class tileElevator():
    def __init__(this,intX,intY,intNewY):
        this.intX=intX
        this.intY=intY
        this.intNewY=intNewY
        this.boolEnabled=False
        this.boolElevating=False
        
    def Draw(this,screen):
        if(this.boolEnabled):
            pygame.draw.rect(screen, (188,140,76), pygame.Rect(this.intX, this.intY, 38, 10))
            ##screen.blit(image, (this.intX, this.intY)) #EVENTUALMENTE SUBSTITUIR POR UM DESENHO Q N PRECISE DE IMAGEM
        else:
            pygame.draw.rect(screen, (160,112,204), pygame.Rect(this.intX, this.intNewY, 38, 10))
            ##screen.blit(image2, (this.intX, this.intNewY))

    def IsElevator(this,player):
        if(this.intX==21):
            if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX),int(player.floatY),32,24),pygame.Rect(this.intX-1,this.intY-4,12,25))):
               return(True)
        elif(this.intX==741):
            if(pygame.Rect.colliderect(pygame.Rect(int(player.floatX),int(player.floatY),32,24),pygame.Rect(this.intX+30,this.intY-1,12,25))):
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
    '''
    def Draw(this,screen,image):
        screen.blit(image, (this.intX, this.intY))
    '''

class bigSwitch(switch):
    def Press(this,walls):
        this.boolEnabled=False
        for wall in walls:
            wall.boolEnabled=True
    def Draw(this,screen):
        pygame.draw.rect(screen, (188,140,76), pygame.Rect(this.intX, this.intY, 12, 20))

class smallSwitch(switch):
    def Press(this,wall):
        this.boolEnabled=False
        wall.boolEnabled=False
    def Draw(this,screen):
        pygame.draw.rect(screen, (208,112,112), pygame.Rect(this.intX+2, this.intY, 8, 20))

class button(): ##PARA O COISO DE FAZER OS NIVEIS
    def __init__(this,intX,intY,intType,image):
        this.intX=intX
        this.intY=intY
        this.intType=intType ##0 == SMALL SWITCH, 1 == BIG SWITCH, 2 == ENEMY (NORMAL), 3 == ENEMY (FAST RIGHT), 4 == ENEMY (FAST LEFT),5 == BLOCK, 6 == SAVE
        this.image=image
    def Draw(this,screen,intType):
        if(this.intType==intType):
            pygame.draw.rect(screen, (112,208,112), pygame.Rect(this.intX, this.intY, 48, 48))
        else:
            pygame.draw.rect(screen, (208,112,112), pygame.Rect(this.intX, this.intY, 48, 48))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(this.intX+4, this.intY+4, 40, 40))
        font = pygame.font.Font('consolas.ttf', 16)

        if(this.image==None):
            saveText = font.render("Save", True, (188,140,76))
            saveRect = saveText.get_rect()
            saveRect.center = (this.intX+24, this.intY+24)
            screen.blit(saveText,saveRect)
        else:
            screen.blit(this.image, (this.intX+8, this.intY+16))
    def isPressed(this,pos):
        if(this.intX<=pos[0] and this.intX+48>=pos[0] and this.intY<=pos[1] and this.intY+48>=pos[1]):
            return(True)
        return(False)
