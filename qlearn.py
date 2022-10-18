from cProfile import run
import re
from tabnanny import verbose
from matplotlib.backend_tools import ToolCopyToClipboardBase
import numpy as np
import random
import nn 
import snakelib as sl
import tensorflow as tf
import copy


lr = 0.001
border = -100
apple = 5
plrSelf = -100

memory = [

]

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(11, activation = "relu"),
    tf.keras.layers.Dense(22, activation='relu'),   
    tf.keras.layers.Dense(3, activation="relu")
])
mse = tf.keras.losses.MeanSquaredError()
model.compile(optimizer='adam',
        loss=mse,
        metrics=['accuracy'])

class Agent:
    def __init__(self, snake):
        self.run_count = 0
        self.gamma = 0.8
        self.epsilon = 0.8
        self.snake = snake
        self.lr = 0.0000000000001

    def getState(self):
     #   fruit = [self.snake.look(i) for i in range(4)]
        self.snake.rotateDir()
        arr = []
        for i in self.snake.lookForFruit():
            arr.append(i)
            
        for i in self.snake.lookForBorder():
            arr.append(i)
        
        for i in range(4):
            arr.append(self.snake.getDir(i))
        
        state = np.array([arr])
      #  print(state.shape)
        return state

    def addMemory(self,oldstate, newstate, reward, action, running):
        memory.append([oldstate, newstate, reward, action, running])

    def typeAction(self, state):
        if np.random.uniform() < self.epsilon:
            action = np.array([0,0,0])
            action[ random.randint(0,2)] = 1
            return action, action.argmax()
        else:
            #pred = ai.feedforward(state)
            pred = tf.nn.softmax(model(state)).numpy()
           # print(state)
          #  print(pred, pred.argmax())
            
            return pred, pred.argmax()
    
    def shortTrain(self, oldstate, newstate, reward, action, running):
        pred = tf.nn.softmax(model(oldstate)).numpy()
        target = copy.copy(pred)
        newQ = reward
        if running:
            newQ = reward + self.gamma * np.max(tf.nn.softmax(model(newstate)))
        target[0][action.argmax()] = newQ
     #   print("\n TARGET VALUES", target[action.argmax()], "\n")
        model.fit(oldstate, target, epochs = 1, verbose = 0)

    def longTrain(self):
        oldstate, newstate, reward, action, running = zip(*memory)
        
        pred = []
        target = []
        arr = []
        for i in range(len(oldstate)):
            run = tf.nn.softmax(model(oldstate[i])).numpy()
            pred.append(run)
            arr.append(oldstate[i])
            target.append(copy.copy(run))
        
        for i in range(len(running)): 
            newQ = reward[i]
            if running[i]:
                newQ = reward[i] + self.gamma * np.max(tf.nn.softmax(model(newstate[i])).numpy())
           
            target[i][0][action[i].argmax()] = newQ

        model.fit(np.array(arr), np.array(target), epochs = 1)

    def train(self, screen):
        state = self.getState()
        action, move = self.typeAction(state)
        sl.direction = sl.directions[str(self.snake.facing[str(move)])]
        self.snake.move(screen)
        running, reward = self.snake.update()
        newState = self.getState()

        if reward > 0:
           # print(reward, self.run_count, self.snake.score, self.snake.pos)
           pass
        self.shortTrain(state, newState, reward, action, running)

        self.addMemory(state, newState, reward, action, running)

        if not running:
            sl.direction = "right"
            self.run_count += 1
            self.longTrain()
            pass
        return running