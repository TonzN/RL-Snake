from cProfile import run
from matplotlib.backend_tools import ToolCopyToClipboardBase
import numpy as np
import random
import nn 
import snakelib as sl
import copy


lr = 0.001
border = -100
apple = 5
plrSelf = -100

memory = [

]

ai = nn.nNet()
ai.FlattenLayer()
ai.DenseLayer(4*3, 12*3, "relu")
ai.DenseLayer(12*3, 12*3, "relu")
ai.DenseLayer(12*3, 3, "relu")



class Agent:
    def __init__(self, snake):
        self.run_count = 0
        self.gamma = 0.9
        self.epsilon = 0.8
        self.snake = snake
        self.lr = 0.0000000000000001

    def getState(self):
     #   fruit = [self.snake.look(i) for i in range(4)]
        self.snake.rotateDir()
        state = np.array([
        [self.snake.lookForFruit(i)  for i in range(3)], 
        [self.snake.lookForBorder(i) for i in range(3)], 
        [self.snake.look(i)          for i in range(3)],
        [self.snake.getDir(i)        for i in range(3)]
        ])
        return state

    def addMemory(self,oldstate, newstate, reward, action, running):
        memory.append([oldstate, newstate, reward, action, running])

    def typeAction(self, state):
        if np.random.uniform() < self.epsilon:
            action = np.array([0,0,0])
            action[ random.randint(0,2)] = 1
            return action, action.argmax()
        else:
            pred = ai.feedforward(state)
                
            return pred, pred.max().argmax()
    
    def shortTrain(self, oldstate, newstate, reward, action, running):
        pred = ai.feedforward(oldstate)
        target = copy.copy(pred)
        newQ = reward
        if running:
            newQ = reward + self.gamma * np.max(ai.feedforward(newstate))


        target[action.argmax()] = newQ

        loss = nn.Cost(pred, target)
        ai.fit(loss, self.lr)

    def longTrain(self):
        if len(memory) > 100:
            memory = memory[0:70]

        oldstate, newstate, reward, action, running = zip(*memory)
        
        pred = []
        target = []
        for i in range(len(oldstate)):
            pred.append(ai.feedforward(oldstate[i]))
            target.append(ai.feedforward(oldstate[i]))
        

        for i in range(len(running)): 
            newQ = reward[i]
            if running[i]:
                newQ = reward[i] + self.gamma * np.max(ai.feedforward(newstate[i]))
           
            target[i][action[i].argmax()] = newQ


        for i in range(len(pred)):
            loss = nn.Cost(pred[i], target[i])
            ai.fit(loss, self.lr)

    def train(self, screen):
        state = self.getState()
        action, move = self.typeAction(state)
        sl.direction = sl.directions[str(self.snake.facing[str(move)])]
        self.snake.move(screen)
        running, reward = self.snake.update()
        newState = self.getState()

        reward += self.snake.hitFruit()

        self.shortTrain(state, newState, reward, action, running)

        self.addMemory(state, newState, reward, action, running)

        if not running:
            self.longTrain()
        
        return running