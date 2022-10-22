import ui
import time
import qlearn
import sys
import tensorflow as tf
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
#qlearn.model = tf.keras.models.load_model("snakeAgent")
Agent.epsilon = 0.8
count = 0
newModel = True
savedHighscore = open("highscore.txt", "r")
Agent.Highscore = int(savedHighscore.read())

while Run:
    window.NextFrame()
    running = Agent.train(screen)
    #player.move(screen)
    #player.update() 
    scoreDisplay.tT = "Score: {score}".format(score = player.score)
    timeDisplay.tT = "Time: {seconds}".format(seconds = player.Seconds)
    runDisplay.tT = "Run: {runs}".format(runs = Agent.run_count)
    if player.score > Agent.Highscore:
        qlearn.model.save("snakeAgent")
        Agent.Highscore = player.score
        savedHighscore = open("highscore.txt", "w")
        savedHighscore.write(str(player.score))
        print("\n NEW HIGHSCORE: ",  player.score, "\n")
    if running == False:
        count += 1
        ui.MainRenderQueue.Queue = []

        player = snake.New(screen, sizeofwindow, 40, (sizeofwindow[0]/2, sizeofwindow[1]/2), window.Target_fps)
        scoreDisplay = ui.TextLabel(screen, 0,0, 100, 30, (255,255,255), "Score: 0", 20)
        timeDisplay = ui.TextLabel(screen, sizeofwindow[0]-100, 0, 100, 30, (255,255,255), "Time: 0", 20)
        runDisplay = ui.TextLabel(screen, sizeofwindow[0]/2-50, 0, 100, 30, (255,255,255), "Run: 0", 20)
        Agent.snake = player
   
    if len(qlearn.memory)>17000:
        qlearn.memory = qlearn.memory[8500:]
    
    if newModel == True:
        if count == 20:
            Agent.epsilon == 0.5
        if count == 45:
            Agent.epsilon == 0.1
        if count == 80  :
            Agent.epsilon = 0.05
    
