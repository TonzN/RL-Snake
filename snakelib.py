from turtle import down, screensize, up, update
from numpy import size
import pygame
import ui
import time
import random

direction = "right"

directions = {
    "0"  :    "up",
    "1":    "down",
    "2":    "left",
    "3":    "right",
}

n_directions = {
    "up"  :    "0",
    "down":    "1",
    "left":    "2",
    "right":   "3",
}

axis = {
    "0": 1,
    "1": 1,
    "2": 0,
    "3": 0
}

class New():
    def __init__(self, screen, screenSize, size, position, fps = 20):
        self.fruit_position = [random.randrange(1, (screenSize[0]//size)) * size,
                    random.randrange(1, (screenSize[1]//size)) * size]
        self.fruit = ui.Rect(screen, self.fruit_position[0], self.fruit_position[1], size, size, (255,0,0))
        self.body = [
            [position[0], position[1]],
            [position[0]-size, position[1]],
            [position[0]-size*2, position[1]],
        ]

        self.pos = [position[0], position[1]]

        self.bodies = [] 
        for i in range(len(self.body)):
            self.bodies.append( ui.Rect(screen, self.body[i][0], self.body[i][1], size, size, (0,255,0))) 
        self.score = 0
        self.screenSize = screenSize
        self.screen = screen
        self.size = size
        self.giveReward = False
        
        self.speed = fps
        self.startTime = time.time()
        self.elapsedTime = time.time()
        self.Seconds = 0

    def plr_update(self):
        if self.pos[0] >= self.screenSize[0]:
            ui.endPygame()
        if self.pos[0] <= 0-15:
            ui.endPygame()
        if self.pos[1] >= self.screenSize[1]:
            ui.endPygame()
        if self.pos[1] <= 0-15:
            ui.endPygame()
        for i in range(1,len(self.body)):
            if (self.pos[0], self.pos[1]) == (self.bodies[i].pos[0], self.bodies[i].pos[1]):
                ui.endPygame()

    def update(self):
        if self.pos[0] >= self.screenSize[0]:
            return False, -10
        if self.pos[0] <= 0-15:
            return False, -10
        if self.pos[1]  >= self.screenSize[1]:
            return False, -10
        if self.pos[1]  <= 0-15:
            return False, -10
        for i in range(1,len(self.body)):
            if (self.pos[0] , self.pos[1]) == (self.bodies[i].pos[0], self.bodies[i].pos[1]):
                return True, -1000
        return True, -100

    def move(self, screen):
        if direction == "up":
            self.pos[1] -= self.size
        elif direction == "down":
            self.pos[1] += self.size
        elif direction == "left":
            self.pos[0] -= self.size
        elif direction == "right":
            self.pos[0] += self.size

        self.body.insert(0, list(self.pos))
        if (self.pos[0], self.pos[1]) == (self.fruit_position[0], self.fruit_position[1]):
            self.score += 1
            self.giveReward = True
            self.bodies.append(ui.Rect(screen, self.pos[0], self.pos[1], self.size, self.size, (0,255,0)))
            
            self.fruit_position = [random.randrange(1, (self.screenSize[0]//self.size)) * self.size,
                                random.randrange(1, (self.screenSize[1]//self.size)) * self.size]
            self.fruit.pos[0], self.fruit.pos[1] = self.fruit_position[0], self.fruit_position[1]

        else:
            self.body.pop()

        for i in range(len(self.body)):
            self.bodies[i].pos[0] = self.body[i][0]
            self.bodies[i].pos[1] = self.body[i][1]

        if time.time() - self.elapsedTime >= 1:
            self.giveReward = True
            self.Seconds = round(time.time() - self.startTime)

    def hitFruit(self):
        if self.giveReward == True:
            self.giveReward == False
            return 1000
        return 0

    def rotateDir(self):
        dir = int(n_directions[direction])
        if dir == 0:
            self.facing = {
            "0": "0",
            "1": "2",
            "2": "3"
            }

        if dir == 1:
            self.facing = {
            "0": "1",
            "1": "3",
            "2": "2"
            }
        if dir == 2:
            self.facing =  {
            "0": "2",
            "1": "1",
            "2": "0"
            }
        if dir == 3:
            self.facing ={
            "0": "3",
            "1": "0",
            "2": "1"
            }

    def lookForFruit(self, dir):
        if self.pos[axis[self.facing[str(dir)]]] + self.size == self.fruit_position[axis[self.facing[str(dir)]]]:
            return 1
        return 0

    def lookForBorder(self, dir):
    
        if self.pos[axis[self.facing[str(dir)]]] + self.size >= self.screenSize[0]:
            return 1
        if self.pos[axis[self.facing[str(dir)]]] + self.size <= 0-15:
            return 1
        if self.pos[axis[self.facing[str(dir)]]] + self.size >= self.screenSize[1]:
            return 1
        if self.pos[axis[self.facing[str(dir)]]] + self.size <= 0-15:
            return 1
        for i in range(1,len(self.body)):
            if (self.pos[0] + self.size, self.pos[1] + self.size) == (self.bodies[i].pos[0], self.bodies[i].pos[1]):
                return 1
        return 0
        
    def look(self, dir):
        if self.lookForBorder(dir) == 0 and self.lookForFruit(dir) == 0:
            return 1
        else:
            return 0

    def getDir(self, dir):
        if directions[str(axis[self.facing[str(dir)]])] == direction:
            return 1
        else:
            return 0