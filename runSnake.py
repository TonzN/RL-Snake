import ui
import time
import qlearn
import sys
import snakelib as snake

window = ui.NewWindow("Snake game", 200, (60,60,60), (80*4,80*4))

sizeofwindow = (80*4, 80*4)

screen = window.screen

Run = True

player = snake.New(screen, sizeofwindow, 40, (sizeofwindow[0]/2, sizeofwindow[1]/2),200)
scoreDisplay = ui.TextLabel(screen, 0,0, 100, 30, (255,255,255), "Score: 0", 20)
timeDisplay = ui.TextLabel(screen, sizeofwindow[0]-100, 0, 100, 30, (255,255,255), "Time: 0", 20)

Agent = qlearn.Agent(player)
Agent.epsilon = 0.7
count = 0

while Run:
    window.NextFrame()
    running = Agent.train(screen)
    #player.move(screen)
    #player.update() 
    scoreDisplay.tT = "Score: {score}".format(score = player.score)
    timeDisplay.tT = "Time: {seconds}".format(seconds = player.Seconds)
    if running == False:
        count += 1
        ui.MainRenderQueue.Queue = []
        player = snake.New(screen, sizeofwindow, 40, (sizeofwindow[0]/2, sizeofwindow[1]/2),200)
        scoreDisplay = ui.TextLabel(screen, 0,0, 100, 30, (255,255,255), "Score: 0", 20)
        timeDisplay = ui.TextLabel(screen, sizeofwindow[0]-100, 0, 100, 30, (255,255,255), "Time: 0", 20)
        Agent.snake = player
    if count == 150:
        Agent.epsilon = 0.2
        window.Target_fps = 15