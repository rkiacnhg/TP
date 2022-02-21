import sys, pygame, math, random
pygame.init()

width = 1200
height = 700    

board = [
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0]]

wallWidth = int(width / 20) #60
wallHeight = height
wallCellWidth = int(wallWidth / len(board[0])) #15
wallCellHeight = int(wallHeight / len(board))  #25
wallRows = len(board) #14
wallCols = len(board[0]) #4

def getCellBounds(row,col):
    x0 = (row*wallCellWidth) + 350
    y0 = col*wallCellHeight
    x1 = ((row+1)*wallCellWidth)
    y1 = (col+1)*wallCellHeight
    return (x0,y0,x1,y1)

def getCellPos(y):
    for row in range(wallRows):
        for col in range(wallCols,-1,-1):
            x0,y0,x1,y1 = getCellBounds(col,row)
            if y < y1+wallCellHeight and y > y0-wallCellHeight:
                return (row,col)

class Figure(object):
    def __init__(self):
        self.image= pygame.image.load("naruto1.png")
        self.x = 200
        self.y = 300
        self.offset = 50
        self.pPause = False
        self.blasterUpgrade = 0
        self.teammateUpgrade = 0
        
    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 5
        if key[pygame.K_s]: # down key
            if self.y < 600:
                self.y += dist # move down
        elif key[pygame.K_w]: # up key
            if self.y >20:
                self.y -= dist # move up
        elif key[pygame.K_d]: # right key
            if self.x < width/4:
                self.x += dist # move right
        elif key[pygame.K_a]: # left key
            if self.x > 20:
                self.x -= dist # move left
        elif key[pygame.K_r]:
            wall.rebuild(self)
        elif key[pygame.K_p]:
            self.pPause = True
            #Pauses game
            
    def shoot(self):
        figure.image = pygame.image.load("naruto2.png")
        x,y = pygame.mouse.get_pos()
        cx, cy = line.x, line.y
        radius = math.sqrt(((x-cx)**2) + ((y-cy)**2))
        angleHelper = (x-cx) / radius
        if y <= cy: #Checks quadrants
            angle = math.degrees(math.asin(angleHelper)) + math.degrees(2*math.pi - math.pi/2)
        elif y > cy: #Checks quadrants
            angle = math.degrees(math.acos(angleHelper))
        
        if self.blasterUpgrade == 0:
            return (Blaster(cx,cy,angle))
        elif self.blasterUpgrade == 1:
            return (RecursiveBlaster(cx,cy,angle))
    
    def getTeammate(self):
        imgTupList = [("teammate1.1.png","teammate1.2.png")]
        for i in range(self.teammateUpgrade):
            offset = 100
            x = width /4
            y = random.randint(offset,height-offset)
            img = imgTupList[i]
            return (Teammate(x,y,img))
            
    def draw(self, surface):
        screen.blit(self.image,(self.x, self.y))
    
    def hitByZombie(self,other):
        if isinstance(other,Zombie):
            if abs(other.x - figure.x) <30 and abs(other.y - figure.y) <30:
                return True

class Teammate(object):
    def __init__(self,x,y,img):
        self.imageList = img
        self.image = pygame.image.load(self.imageList[0])
        self.x = x
        self.y = y
        self.speed = 20
    
    def draw(self,surface):
        screen.blit(self.image,(self.x,self.y))
    
    def shoot(self):
        #RANDOMLY shoots at zombies. (might not even hit them)
        self.image = pygame.image.load(self.imageList[1])
        angle1 = random.randint(0,75)
        angle2 = random.randint(270,345)
        angleList = [angle1,angle2]
        shotAngle = random.choice(angleList)
        return (Blaster(self.x,self.y,shotAngle))
    
    def move(self):
        for zombie in zombies:
            if zombie.passable:
                maybe = [True,False,False,False]
                #Teammate only sometimes listens to me
                a = random.choice(maybe)
                if a:
                    key = pygame.key.get_pressed()
                    dist = 5
                    if key[pygame.K_w]: # down key
                        if self.y < 600:
                            self.y += dist # move down
                    elif key[pygame.K_s]: # up key
                        if self.y >20:
                            self.y -= dist # move up
                    elif key[pygame.K_a]: # right key
                        if self.x < width/4:
                            self.x += dist # move right
                    elif key[pygame.K_d]: # left key
                        if self.x > 20:
                            self.x -= dist # move left
                            
    def hitByZombie(self,other):
        if isinstance(other,Zombie):
            if abs(other.x - self.x) <40 and abs(other.y - self.y) <40:
                return True

class Line(Figure):
    #Invisible line extends from figure
    def __init__(self):
        self.x = figure.x +20
        self.y = figure.y+40
        
    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 5
        if key[pygame.K_s]: # down key
            if self.y < 650:
                self.y += dist # move down
        elif key[pygame.K_w]: # up key
            if self.y >60:
                self.y -= dist # move up
        elif key[pygame.K_d]: # right key
            if self.x < 330:
                self.x += dist # move right
        elif key[pygame.K_a]: # left key
            if self.x > 50:
                self.x -= dist # move left
        elif key[pygame.K_p]:
            state = PAUSE
    
    def draw(self,surface):
        x0,y0 = pygame.mouse.get_pos()
        pygame.draw.lines(screen, (0,0,0), True, [(self.x,self.y),(x0,y0)],5)
   

class Blaster(object):
    # Model
    def __init__(self, x, y, angle, ammo=111):
        # A bullet has a position, a size, a direction
        self.cx = x
        self.cy = y
        self.r = 2
        self.angle = angle
        self.speed = 40
        self.ammo = ammo
        self.originalAmmo = ammo
    # View
    def draw(self, surface):
        radius = 10
        pygame.draw.circle(surface, (140,229,241), (int(self.cx), int(self.cy)), radius)
        pygame.draw.circle(surface, (255,255,255), (int(self.cx), int(self.cy)),radius-3)
    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        rad = math.radians(self.angle)
        self.cx += (math.cos(rad)) * self.speed
        self.cy += (math.sin(rad)) * self.speed
        
    def hitZombie(self, other):
        # Check if the bullet and zombie overlap at all
        if(isinstance(other, Zombie)) or isinstance(other,Player2): 
        # Other must be a zombie
            ((x,y),(w,z)) =other.zombieArea()
            if self.cx > x and self.cx < y and self.cy>w and self.cy<z:
                return True
            return False
    
    def isOffscreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        return (self.cx + self.r <= 0 or self.cx - self.r >= width) or \
               (self.cy + self.r <= 0 or self.cy - self.r >= height)
    
class RecursiveBlaster(Blaster):
    #an upgrade of the regular blaster. It is recursive!
    def __init__(self, x, y, angle):
        super().__init__(self,x,y,angle)
        self.cx = x
        self.cy = y
        self.angle = angle
    
    def split(self, cx, cy, angle):
        return (RecursiveBlaster(cx,cy,angle+45)), (RecursiveBlaster(cx,cy,angle-45))
    
    
class Wall(object):
    def __init__(self):
        self.board = board
        self.x = 350 + wallWidth
    
    def hitByZombie(self,other):
        #Zombie Hitting Wall
        if isinstance(other,Zombie) and other.x - (self.x) < 3:
            return True
    
    def drawWall(self,surface):
        for row in range(wallRows):
            for col in range(wallCols):
                (x0,y0,x1,y1) = getCellBounds(col,row)
                fill = (0,44,55) if self.board[row][col] == 0 else (185,122,86)
                pygame.draw.rect(surface,fill,(x0,y0,wallCellWidth,wallCellHeight))   

    def rebuild(self,other):
        if isinstance(other,Figure) and abs(self.x - other.x) <200:
            row,col = getCellPos(other.y+other.offset)
            board[row] = [0,0,0,0]
        
class Player2(object):
    def __init__(self):
        self.image = pygame.image.load("bossZombie.png")
        self.health1 = pygame.image.load("health1.jpg")
        self.hpBar1 = pygame.image.load("hp1.png")
        self.health2 = pygame.image.load("health2.jpg")
        self.offset = 150
        self.x = width - 150
        self.y = height - self.offset * 2
        self.hp1 = 30
        self.hp2 = 200
        self.count = 0
        self.speed = 1
    
    def zombieArea(self):
        return ((self.x+20,self.x+50),(self.y+30,self.y+130))
        
    
    def handle_keys(self):
        #Control p2
        key = pygame.key.get_pressed()
        dist = 5
        if key[pygame.K_DOWN]: # down key
            if self.y < height-self.offset:
                self.y += dist # move down
        elif key[pygame.K_UP]: # up key
            if self.y >self.offset:
                self.y -= dist # move up
        elif key[pygame.K_RIGHT]: # right key
            if self.x < width-self.offset:
                self.x += dist
        elif key[pygame.K_SEMICOLON]:
            self.count += 1
            if int(self.count%3) == 0:
                zomb = Runner.makeZombie()
                zombieList2.append(zomb)
            elif int(self.count%5) == 0:
                zomb = Strong.makeZombie()
                zombieList2.append(zomb)
            else:
                zomb = Zombie.makeZombie()
                zombieList2.append(zomb)
                
    def move(self):
        (row,col) = getCellPos(self.y+self.offset)
        if self.x > wall.x:
            self.x -= self.speed
        elif (board[row] == [1,1,1,1]):
            self.x -= self.speed
            
    def draw(self, surface):
        #Drawing p2 and health
        for hp in range(self.hp1):
            screen.blit(self.health1, (self.x+25+ (8*hp),self.y-20))
        for hp in range(self.hp2):
            screen.blit(self.health2, (self.x+25+(1*hp),self.y-20))
        screen.blit(self.hpBar1, (self.x+10, self.y-30))
        screen.blit(self.image, (self.x, self.y))

class Zombie(object):
    #Zombie has coordinates and hp
    def __init__(self,x,y, hp = 3, speed = 15):
        self.health = pygame.image.load("health1.jpg")
        self.image = pygame.image.load("zombie.png")
        self.hpBar = pygame.image.load("hp1.png")
        self.x, self.y= x,y
        self.hp = hp
        self.speed = speed
        self.breakWall = True 
        #Bullion so that one zombie doesnt destroy every wall
        self.offset = 70
        self.passable = False
        
    def draw(self, surface):
        #Draws zombies and hp bar
        for hp in range(self.hp):
            screen.blit(self.health, (self.x+25+(10*hp),self.y-20))
        screen.blit(self.hpBar, (self.x+10, self.y-30))
        screen.blit(self.image,(self.x,self.y))
    
    def moveZombie(self):
        #Moves zombies
        (row,col) = getCellPos(self.y+self.offset)
        if self.x > wall.x:
            self.x -= self.speed
            self.y += random.randint(-10,10)
        elif (board[row] == [1,1,1,1]) or (self.passable):
            self.passable = True
            self.x -= self.speed
            if len(teamList) > 0:
                for teammate in teamList:
                    if teammate.y > self.y:
                        self.y += self.speed
                    elif teammate.y <self.y:
                        self.y -= self.speed
                        
            elif self.x+self.offset < (wall.x - wallWidth):
                if figure.y > self.y:
                    self.y += self.speed
                elif figure.y <self.y:
                    self.y -= self.speed
            
    def zombieArea(self):
        #The area of a zombie that a blaster can hit
        return ((self.x-10,self.x+10),(self.y-20,self.y+80))
    
    @staticmethod
    def makeZombie():
        x = 1200
        y = random.randint(30,width/2)
        return (Zombie(x,y))

class Runner(Zombie):
    def __init__(self,x,y):
        super().__init__(self,x,y)
        self.image = pygame.image.load("zombie2.png")
        self.speed = 25
        self.hp = 4
        self.x, self.y = x,y
    
    @staticmethod
    def makeZombie():
        x = 1200
        y = random.randint(30,width/2)
        return (Runner(x,y))
    
class Strong(Zombie):
    def __init__(self,x,y):
        super().__init__(self,x,y, speed = 5)
        self.x, self.y = x,y
        self.hp = 15
        self.image = pygame.image.load("zombie3.png")
    
    @staticmethod
    def makeZombie():
        x = 1200
        y = random.randint(30,width/2)
        return (Strong(x,y))
        
        
        figure.image = pygame.image.load("naruto2.png")
        x,y = pygame.mouse.get_pos()
        cx, cy = line.x, line.y
        radius = math.sqrt(((x-cx)**2) + ((y-cy)**2))
        angleHelper = (x-cx) / radius
        if y <= cy: #Checks quadrants
            angle = math.degrees(math.asin(angleHelper)) + math.degrees(2*math.pi - math.pi/2)
        elif y > cy: #Checks quadrants
            angle = math.degrees(math.acos(angleHelper))
        return (Blaster(cx,cy,angle))
        
class BlasterUpgrade(object):
    def __init__(self):
        self.width = 250
        self.height = 150
        self.textSize = 32
    
    def draw(self, surface):
        pygame.draw.rect(surface, pygame.color.Color("DeepSkyBlue"),((width/2)-(self.width),height/2,self.width,self.height),10)
        blaster_text1 = pygame.font.SysFont('Consolas', self.textSize).render('Blaster', True, pygame.color.Color('Orange'))
        screen.blit(blaster_text1, ((width/2)+self.textSize-(self.width),(height/2)+self.height/2,self.width,self.height))
        blaster_text2 = pygame.font.SysFont('Consolas', self.textSize).render('Upgrade', True, pygame.color.Color('Orange'))
        screen.blit(blaster_text2, ((width/2)+self.textSize-(self.width),(height/2)+self.textSize+self.height/2,self.width,self.height))
        
    def select(self):
        x0,y0 = pygame.mouse.get_pos()
        if x0 in range(int((width/2)-self.width),int(width/2)) and \
        y0 in range(int(height/2),int(height/2)+self.height):
            figure.blasterUpgrade +=1
            return True
            
        
class TeammateUpgrade(object):
    def __init__(self):
        self.width = 250
        self.height = 150
        self.textSize = 32
        
    def draw(self,surface):
        pygame.draw.rect(surface, pygame.color.Color("DeepSkyBlue"),((width/2)+(self.width),height/2,self.width,self.height),10)
        teammate_text1 = pygame.font.SysFont('Consolas', self.textSize).render('Teammate', True, pygame.color.Color('Orange'))
        screen.blit(teammate_text1, ((width/2)+self.textSize+(self.width),(height/2)+self.height/2,self.width,self.height))
        teammate_text2 = pygame.font.SysFont('Consolas', self.textSize).render('Upgrade', True, pygame.color.Color('Orange'))
        screen.blit(teammate_text2, ((width/2)+self.textSize+(self.width),(height/2)+self.textSize+self.height/2,self.width,self.height))
        
    def select(self):
        x0,y0 = pygame.mouse.get_pos()
        if x0 in range(int(width/2)+self.width,int(width/2)+2*self.width) and \
        y0 in range(int(height/2),int(height/2)+self.height):
            figure.teammateUpgrade +=1
            teamList.append(figure.getTeammate())
            return True

class StartButton2(object):
    def __init__(self):
        self.width = 250
        self.height = 150
        self.textSize = 32
        
    def draw(self,surface):
        pygame.draw.rect(surface, pygame.color.Color("DeepSkyBlue"),((width/2)+(self.width),height/2,self.width,self.height),10)
        teammate_text1 = pygame.font.SysFont('Consolas', self.textSize).render('Two', True, pygame.color.Color('Orange'))
        screen.blit(teammate_text1, ((width/2)+self.textSize+(self.width),(height/2)+self.height/2,self.width,self.height))
        teammate_text2 = pygame.font.SysFont('Consolas', self.textSize).render('Player', True, pygame.color.Color('Orange'))
        screen.blit(teammate_text2, ((width/2)+self.textSize+(self.width),(height/2)+self.textSize+self.height/2,self.width,self.height))
        
    def select(self):
        x0,y0 = pygame.mouse.get_pos()
        if x0 in range(int(width/2)+self.width,int(width/2)+2*self.width) and \
        y0 in range(int(height/2),int(height/2)+self.height):
            return 2
            
class StartButton1(object):
    def __init__(self):
        self.width = 250
        self.height = 150
        self.textSize = 32
    
    def draw(self, surface):
        pygame.draw.rect(surface, pygame.color.Color("DeepSkyBlue"),((width/2)-(self.width),height/2,self.width,self.height),10)
        blaster_text1 = pygame.font.SysFont('Consolas', self.textSize).render('Single', True, pygame.color.Color('Orange'))
        screen.blit(blaster_text1, ((width/2)+self.textSize-(self.width),(height/2)+self.height/2,self.width,self.height))
        blaster_text2 = pygame.font.SysFont('Consolas', self.textSize).render('Player', True, pygame.color.Color('Orange'))
        screen.blit(blaster_text2, ((width/2)+self.textSize-(self.width),(height/2)+self.textSize+self.height/2,self.width,self.height))
        
    def select(self):
        x0,y0 = pygame.mouse.get_pos()
        if x0 in range(int((width/2)-self.width),int(width/2)) and \
        y0 in range(int(height/2),int(height/2)+self.height):
            return 1
            
        
screen = pygame.display.set_mode((width, height))

##Time
#Zombies
waves = 2
score = 0

def wave():
    z, r, s = 0, 0, 0
    z, r, s = 10, 5 * waves//1, 5 * waves//2
    return z, r, s
zombieTimer = 1000
makeZombie = pygame.USEREVENT+1
walkZombie = pygame.USEREVENT+2
notShoot = pygame.USEREVENT+3
hitWall = pygame.USEREVENT+4
checkZombie = pygame.USEREVENT+5
AIshoot = pygame.USEREVENT+6
pygame.time.set_timer(checkZombie,zombieTimer+100)
pygame.time.set_timer(makeZombie, zombieTimer)
pygame.time.set_timer(walkZombie,80)
pygame.time.set_timer(notShoot, 300)
pygame.time.set_timer(hitWall,750)
pygame.time.set_timer(AIshoot, 500)

def createZombie():
    nz, rz, sz = wave()
    for i in range(nz):
        zomb = Zombie.makeZombie()
        zombieList.append(zomb)
        zomb = None
    for j in range(rz):
        zomb = Runner.makeZombie()
        zombieList.append(zomb)
        zomb = None
    for h in range(sz):
        zomb = Strong.makeZombie()
        zombieList.append(zomb)
        zomb = None
        
#Lists
teamList = []
blasterList = []
zombies = []
zombieList2 = []
zombieList = []
figure = Figure() # create an instance
player2 = Player2()
line = Line()
time = pygame.time.Clock()
wall = Wall()
button1 = BlasterUpgrade()
button2 = TeammateUpgrade()
sb1 = StartButton1()
sb2 = StartButton2()
backgroundImage = pygame.image.load("grass.jpg")


def dontShoot():
    figure.image = pygame.image.load("naruto1.png")
    for teammate in teamList:
        teammate.image = pygame.image.load(teammate.imageList[0])

def hittingWall():
    for zombie in zombies:
        if zombie.breakWall and wall.hitByZombie(zombie):
            row, col = getCellPos(zombie.y + zombie.offset)
            for i in range(col):
                board[row][i] = 1
                if 0 not in board[row]:
                    if row-1>0 and row +1 <=wallRows:
                        board[row+1] = [1,1,1,1]
                        board[row-1] = [1,1,1,1]
                    elif row-1>0 and row+1 > wallRows:
                        board[row-1] = [1,1,1,1]
                    elif row -1 <=0 and row +1 <= wallRows:
                        board[row+1] = [1,1,1,1]
                    zombie.breakWall = False

running = True
alive = True
RUNNING, PAUSE = 0 ,1
mode = 0
state = PAUSE

while running:
    if state == RUNNING and mode ==1:
        ###Single Player
        #Citation: https://www.pygame.org/docs/ref/draw
        #Citation for some of the key handling codes.
        myfont = pygame.font.SysFont("monospace",35)
        text1 = "Wave:" + str(waves)
        label1 = myfont.render(text1,1,(255,255,0))
        text2 = "Score:" + str(score)
        label2 = myfont.render(text2,1,(255,255,0))
        cursor = pygame.cursors.broken_x #MOUSE
        pygame.mouse.set_cursor(*cursor)
        click = pygame.mouse.get_pressed()
        if click[0]: #Mouse Click
            time1 = pygame.time.get_ticks()
            time2 = pygame.time.get_ticks()
            if time2-time1 < 100:
                shoot = figure.shoot()
                blasterList.append(shoot)
        screen.blit(backgroundImage, (0,0))
        screen.blit(backgroundImage, (width/2,0))
        screen.blit(backgroundImage, (0,height/2))
        screen.blit(backgroundImage, (width/2,height/2))
        # handle every event since the last frame.
        if pygame.event.get(AIshoot):
            for teammate in teamList:
                fired = teammate.shoot()
                blasterList.append(fired)
        if pygame.event.get(hitWall):
            hittingWall()
        if pygame.event.get(walkZombie):
            for zombie in zombies:
                if zombie.x <= 0:
                    zombies.remove(zombie)
                    continue
                zombie.moveZombie()
                if figure.hitByZombie(zombie):
                    #If zombie is near player, game is over.
                    gameOver_text = pygame.font.SysFont('Consolas', 50).render('GameOver', True, pygame.color.Color('Black'))
                    screen.blit(gameOver_text, (width/2, height/2))
                    running = False
                elif len(teamList) > 0:
                    for teammate in teamList:
                        if teammate.hitByZombie(zombie):
                            figure.teammateUpgrade -= 1
                            teamList.remove(teammate)
                
        for teammate in teamList:
            teammate.move()
        if pygame.event.get(notShoot):
            dontShoot()
        if pygame.event.get(checkZombie):
            #Checks if there are no zombies on the screen
            if len(zombies) == 0 and len(zombieList2) == 0:
                createZombie()
                while len(zombieList)>0:
                    i = random.choice(zombieList)
                    zombieList.remove(i)
                    zombieList2.append(i)
                waves +=1
                pygame.time.wait(1500)
                if waves % 3 == 0:
                    state = PAUSE
        #Key handling and Drawing
        figure.handle_keys() # handle the keys
        wall.drawWall(screen)
        line.handle_keys()
        line.draw(screen)
        figure.draw(screen) # draw the figure to the screen
        figure.getTeammate()
        screen.blit(label1, (20,50))
        screen.blit(label2, (20,650))
        for zombie in zombieList2:
            if pygame.event.get(makeZombie):
                zombies.append(zombie)
                zombieList2.remove(zombie)
        for zombie in zombies:
            zombie.draw(screen)
        for teammate in teamList:
            teammate.draw(screen)
        for blast in blasterList:
            blast.draw(screen)
            blast.moveBullet()
            if blast.isOffscreen(1200,700):
                blasterList.remove(blast)
            
            for zombie in zombies:
                if blast.hitZombie(zombie):
                    zombie.hp -= 1
                    if isinstance(blast,RecursiveBlaster):
                        a, b = blast.split(zombie.x, zombie.y,blast.angle)
                        blasterList.append(a)
                        blasterList.append(b)
                    if zombie.hp == 0:
                        zombies.remove(zombie)
                        score += 1
                    try:
                        blasterList.remove(blast)
                    except:
                        continue
        key = pygame.key.get_pressed()
        if key[pygame.K_p]:
            state = PAUSE
    ###Two Player
    elif state == RUNNING and mode ==2:
        cursor = pygame.cursors.broken_x #MOUSE
        pygame.mouse.set_cursor(*cursor)
        click = pygame.mouse.get_pressed()
        if click[0]: #Mouse Click
            time1 = pygame.time.get_ticks()
            time2 = pygame.time.get_ticks()
            if time2-time1 < 100:
                shoot = figure.shoot()
                blasterList.append(shoot)
        screen.blit(backgroundImage, (0,0))
        screen.blit(backgroundImage, (width/2,0))
        screen.blit(backgroundImage, (0,height/2))
        screen.blit(backgroundImage, (width/2,height/2))
        # handle every event since the last frame.
        if pygame.event.get(hitWall):
            hittingWall()
        if pygame.event.get(walkZombie):
            for zombie in zombies:
                if zombie.x <= 0:
                    zombies.remove(zombie)
                    continue
                zombie.moveZombie()
                if figure.hitByZombie(zombie):
                    screen.fill((0,0,0))
                    #If zombie is near player, game is over.
                    gameOver_text = pygame.font.SysFont('Consolas', 50).render('Player 2 Wins', True, pygame.color.Color('White'))
                    screen.blit(gameOver_text, (width/2, height/2))
                    running = False
        if pygame.event.get(notShoot):
            dontShoot()
        #Key handling and Drawing
        figure.handle_keys() # handle the keys
        wall.drawWall(screen)
        line.handle_keys()
        line.draw(screen)
        figure.draw(screen) # draw the figure to the screen
        player2.draw(screen)
        player2.handle_keys()
        player2.move()
        for zombie in zombieList2:
            if pygame.event.get(makeZombie):
                zombies.append(zombie)
                zombieList2.remove(zombie)
        for zombie in zombies:
            zombie.draw(screen)
        for teammate in teamList:
            teammate.draw(screen)
        for blast in blasterList:
            blast.draw(screen)
            blast.moveBullet()
            if blast.isOffscreen(1200,700):
                blasterList.remove(blast)
            if blast.hitZombie(player2):
                blasterList.remove(blast)
                if player2.hp2 >0:
                    player2.hp2 -= 1
                else:
                    player2.hp1 -=1
                    if player2.hp1 <= 0:
                        screen.fill((0,0,0))
                        gameOver_text = pygame.font.SysFont('Consolas', 50).render('Player 1 Wins', True, pygame.color.Color('White'))
                        screen.blit(gameOver_text, (width/2, height/2))
                        running = False
            for zombie in zombies:
                if blast.hitZombie(zombie):
                    zombie.hp -= 1
                    if isinstance(blast,RecursiveBlaster):
                        a, b = blast.split(zombie.x, zombie.y,blast.angle)
                        blasterList.append(a)
                        blasterList.append(b)
                    if zombie.hp == 0:
                        zombies.remove(zombie)
                        score += 1
                    try:
                        blasterList.remove(blast)
                    except:
                        continue
        
    elif state == PAUSE:
        #Pause Code from 
        #https://stackoverflow.com/questions/30744237/how-to-create-a-pause-button-in-pygame
        if figure.pPause:
            pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))
            screen.blit(pause_text, (width/2, height/2))
            key = pygame.key.get_pressed()
            if key[pygame.K_o]:#Start Again
                state = RUNNING
        elif mode == 0:
            #Start Screen
            sb1.draw(screen)
            sb2.draw(screen)
            click = pygame.mouse.get_pressed()
            if click[0]:
                if sb1.select() == 1:
                    print("y")
                    mode = 1
                    state = RUNNING
                elif sb2.select() == 2:
                    print("y1")
                    mode =2
                    state = RUNNING
        else:
            button1.draw(screen)
            button2.draw(screen)
            click = pygame.mouse.get_pressed()
            if click[0]:
                if button1.select() or button2.select():
                    state = RUNNING
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            zombieList2 = []
            zombies = []
            waves = 0
            pygame.quit() # quit the screen
            running = False            
    pygame.display.update()    
    time.tick(40)