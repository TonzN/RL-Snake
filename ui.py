import pygame
import math
import random
import time
import snakelib as snake
import os

Bools = {
    "CD": False
}

def LinearSearch(l, n):
    # l = list
    for i, v in enumerate(l):
        if v == n:
            return i
    return False

ScreenSize = None

def endPygame():
    print("GAME OVER!!")
    pygame.quit()
    exit()

class Folder:
    def __init__(self):
        self.Objs = {}
        self.Size = len(self.Objs)
    def Clear(self):
        self.Objs = {}

class RenderQueue:
    def __init__(self, Queue = []):
        self.Queue = Queue
    
    def Push(self, n):
        self.Queue.append(n)

    def AddObjects(self, n):
        for i in n:
            if type(n[i]) == list:
                self.AddObjects(n[i])
            else:
                self.Push(n[i])

    def Pop(self):
        if self.Queue:
          del self.Queue[0]
        
    def Remove(self, n):
        item = LinearSearch(self.Queue, n)
        if item:
            self.Queue.pop(item)

MainRenderQueue = RenderQueue()

class NewWindow:
    def __init__(self, Name = "MyGame", TargetFps = 60, BGColor = (60,60,60), Size = (800,600)):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode(Size)
        self.prev_time = time.time()
        self.Target_fps = TargetFps
        self.Size = Size
        self.CDdel = time.time()
        self.BGColor = BGColor

        self.Running = True
        pygame.display.set_caption(Name)
    
    def RenderObjects(self, Layers = None):
        queue = RenderQueue()
        for i in MainRenderQueue.Queue:
            i.Redraw()
        if Layers:
            for i in Layers:
                queue.AddObjects(i)
            for i in queue.Queue:
                i.Redraw()
        
    def NextFrame(self, Layers = None):
        self.Running = EventHandler()
        if self.Running == False:
           endPygame()
           
        self.RenderObjects(Layers)
        pygame.display.update()

        if time.time() - self.CDdel >= 0.05: 
            CDdel = time.time()
            Bools["CD"] = False
        #-------FPS--------#
        fps = pygame.time.Clock()
        fps.tick(self.Target_fps)
        self.screen.fill(self.BGColor)

def runEvents(Objects = False): #Runs object functions. 
    #Objects er bare en array med alle objektene som har events so skal kjøres
    if Objects:
        for i in Objects:
            i.CheckEvents()

def EventHandler(): #Finder hendelser for vinduet
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False
        if e.type == pygame.MOUSEBUTTONUP:
            Bools["CD"] = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w and snake.direction != "down":
                    snake.direction = "up"
            if e.key == pygame.K_s and snake.direction != "up":
                snake.direction = "down"
            if e.key == pygame.K_a and snake.direction != "right":
                snake.direction = "left"
            if e.key == pygame.K_d and snake.direction != "left":
                snake.direction = "right"
            
    return True

class Rect:
    def __init__(self, screen, x, y, width, height, c1, c2 = False, Render = True): #innehold til en Ui
        self.pos     = [x,y]
        self.RQ = MainRenderQueue
        self.width  = width
        self.height = height
        self.c1     = c1
        self.c2     = c2
        self.Render = Render
        self.screen = screen
        self.autoScale = False#AutoScale
        self.AddToRenderQueue(self.RQ)
        if Render:
            if self.autoScale:
                self.AutoScale()
            pygame.draw.rect(screen, c1, (x, y, self.width, self.height))

    def Click(self): #finner mus klikk op posisjonen returnerer True viss du klikker
        mouseP = pygame.mouse.get_pos()
        click  = pygame.mouse.get_pressed()
        if self.Render:
            if self.x + self.width > mouseP[0] > self.x and self.y + self.height > mouseP[1] > self.y:  
                # Hvis mus x og y kordnitaer er riktig/ peker på knappen
                pygame.draw.rect(self.screen, self.c2, (self.pos[0], self.pos[1], self.width, self.height))
                if click[0] == 1 and Bools["CD"] == False:
                    Bools["CD"] = True
                    return True
                return False

    def AutoScale(self): #In %
        self.width, self.height = (ScreenSize[0]/100)*self.width, (ScreenSize[1]/100)*self.height

    def Redraw(self):
       if self.Render:         
            pygame.draw.rect(self.screen, self.c1, (self.pos[0], self.pos[1], self.width, self.height))
    
    def AddText(self, tC, tT, tS):
        font = pygame.font.Font('freesansbold.ttf', tS) #font
        text = font.render(tT, self.Render, tC)
        textRect = text.get_rect()
        textRect.center = (self.pos[0] + (self.width // 2), self.pos[1] + (self.height // 2)) #plasserer teksten i midten
        self.screen.blit(text, textRect)

    def AddToRenderQueue(self, queue = MainRenderQueue):
        queue.Push(self)
    
    def Collision(self):
        pass

class Ball():
    def __init__(self, screen, x, y, radius, color1, Render = True):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color1
        self.Visible = Render
        self.Screen = screen
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def AddToRenderQueue(self, RQ = MainRenderQueue):
        RQ.Push(self)
    
    def Redraw(self):
       # print(self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.Screen, self.color, (self.x, self.y), self.radius)
       
class TextLabel():
        #Info om varibaler
        #c1/c2 = color1/color2
        def __init__(self, screen, x, y, width, height, tC = None, tT = None, tS = None, Render = True):
            self.tC = tC #TextColor
            self.tS = tS #tSize
            self.width = width
            self.height = height
            self.pos = [x,y]
            self.screen = screen
            self.Render = Render
            self.tT = tT #tType
            MainRenderQueue.Push(self)

        def Redraw(self):
            if self.tT:
                font = pygame.font.Font('freesansbold.ttf', self.tS) #font
                text = font.render(self.tT, self.Render, self.tC)
                textRect = text.get_rect()
                textRect.center = (self.pos[0] + (self.width // 2), self.pos[1] + (self.height // 2)) #plasserer teksten i midten
                self.screen.blit(text, textRect)
    
class Button(Rect):
        def __init__(self,screen, x, y, width, height, c1, c2, Event = False, Input = False, Render = True):
            self.Event = Event #Hendelse etter du trykker
            self.Input = Input #Input = funksjon input
            super().__init__(screen, x, y, width, height, c1, c2, Render)

        def CheckEvents(self): #Methods Uten return
            hit = self.Click()
            MEvent = False
            if hit :
                MEvent = True
                if self.Event:
                    if self.Input:
                        self.Event(self.Input)
                    else:
                        self.Event()
          
        def runEvent(self, event, input = False):#Method som returner 
            Hit = self.Click()
            if Hit and event:
                Output = None
                if input:
                    Output = event(input)
                else:
                    Output = event()
                return Output
            else:
                return False

class Frame(Rect):
    def __init__(self,screen, x, y, width, height, c1 ):
        super().__init__(screen,x, y, width, height, c1)    