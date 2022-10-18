import ui
import time
import qlearn
import sys
import snakelib as snake

window = ui.NewWindow("Snake game", 200, (60,60,60), (80*4,80*4))

sizeofwindow = (80*4, 80*4)

screen = window.screen

Run = True

player = snake.New(screen, sizeofwindow, 40, (sizeofwindow[0]/2, sizeofwindow[1]/2), window.Target_fps)
scoreDisplay = ui.TextLabel(screen, 0,0, 100, 30, (255,255,255), "Score: 0", 20)
timeDisplay = ui.TextLabel(screen, sizeofwindow[0]-100, 0, 100, 30, (255,255,255), "Time: 0", 20)
runDisplay = ui.TextLabel(screen, sizeofwindow[0]/2-50, 0, 100, 30, (255,255,255), "Run: 0", 20)

Agent = qlearn.Agent(player)
Agent.epsilon = 0.8
count = 0

while Run:
    window.NextFrame()
    running = Agent.train(screen)
    #player.move(screen)
    #player.update() 
    scoreDisplay.tT = "Score: {score}".format(score = player.score)
    timeDisplay.tT = "Time: {seconds}".format(seconds = player.Seconds)
    runDisplay.tT = "Run: {runs}".format(runs = Agent.run_count)
    if running == False:
        count += 1
        ui.MainRenderQueue.Queue = []

        player = snake.New(screen, sizeofwindow, 40, (sizeofwindow[0]/2, sizeofwindow[1]/2), window.Target_fps)
        scoreDisplay = ui.TextLabel(screen, 0,0, 100, 30, (255,255,255), "Score: 0", 20)
        timeDisplay = ui.TextLabel(screen, sizeofwindow[0]-100, 0, 100, 30, (255,255,255), "Time: 0", 20)
        runDisplay = ui.TextLabel(screen, sizeofwindow[0]/2-50, 0, 100, 30, (255,255,255), "Run: 0", 20)
        Agent.snake = player
    if count == 10:
        Agent.epsilon == 0.5
    if count == 30:
        Agent.epsilon == 0.2
    if count == 50:
        Agent.epsilon = 0.1
        