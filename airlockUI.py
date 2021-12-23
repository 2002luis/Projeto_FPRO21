import pygame

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
