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
        newPos=this.floatX+(direction*0.12*dt)
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

    def HandleBlocks(this,block,curDir): ##OS BLOCOS COMPORTAM-SE DE MANEIRA ESTRANHA NO JOGO NORMAL
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
        newPos=this.intX+(this.dirX*0.12*dt)
        if(newPos<77):
            newPos=77
            this.dirX=1
        elif(newPos>723-32):
            newPos=723-32
            this.dirX=-1
        if(this.dirX==1 and this.behaviour==1):
            this.dirX=4
        elif(this.dirX==-1 and this.behaviour==-1):
            this.dirX=-4
        this.intX=newPos

class fish():
    def __init__(this,intX,intY,dirX,speedX):
        this.intX=intX
        this.intY=intY
        this.dirX=dirX
        this.speedX=speedX
    def Move(this,dt):
        this.intX+=this.speedX*dt*this.dirX
        if(this.intX<-70):
            this.intX=870
        elif(this.intX>870):
            this.intX=-70
    def Draw(this,screen,image):
        screen.blit(image,(this.intX,this.intY))

