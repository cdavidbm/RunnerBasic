import pgzrun
import random
from pgzero.builtins import Actor, animate, keyboard

WIDTH = 600
HEIGHT = 300
TITLE = "Runner"
FPS = 30

prota = Actor("1", (50, 240), size=(120, 120))
background = Actor("fondo")
ground = Actor('ground', (550, 265))
bat = Actor('bat', (550, 175))

game_state = 0
count = 0
enemy = random.randint(1,2)

def draw():
    if game_state == 0:
        background.draw()
        prota.draw()
        screen.draw.text(str(count), pos=(10, 10), color="white", fontsize = 24)
    elif game_state == 1:
        background.draw()
        screen.draw.text('Press Enter', pos=(WIDTH/2 - 85, HEIGHT/2), color="red", fontsize=36, align='center')
        
    ground.draw() if enemy == 1 else bat.draw()

def grounds():
    global count, enemy
    if ground.x > 0:
        ground.x -= 5
        ground.angle += 5 
    else:
        ground.x = WIDTH
        count += 1
        enemy = random.randint(1,2)
        
def bats():
    global count, enemy, bat
    if bat.x > 0:
        bat.x -= 5
    else:
        bat.x = WIDTH
        bat.y = random.randint(120, 550)
        count +=1
        enemy = random.randint(1,2)

def update(dt):
    global new_image, count, game_state, speed
    
    grounds() if enemy == 1 else bats()
        
    if keyboard.RIGHT or keyboard.d:
        prota.x += 5
    if keyboard.LEFT or keyboard.a:
        prota.x -= 5
    if keyboard.space or keyboard.up or keyboard.w:
        prota.y = 100
        animate(prota, tween='bounce_end', duration=2, y=240)
    
    if prota.colliderect(ground) or prota.colliderect(bat):
        game_state = 1
        
pgzrun.go()