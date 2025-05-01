import pgzrun
import random
from pgzero.builtins import Actor, animate, keyboard

WIDTH = 600
HEIGHT = 300
TITLE = "Runner"
FPS = 30

prota = Actor("1", (50, 240), size=(120, 120))
lista_de_img = ["1", "2", "3", "4", "5", "6"]
indice = 0

background = Actor("fondo")
ground = Actor('ground', (550, 265))
bat = Actor('bat', (550, 175))

game_state = 0
count = 0
enemy = random.randint(1,2)
speed = 5

bg_x = 0
bg_speed = 2 

def grounds():
    global count, enemy, speed
    if ground.x > 0:
        ground.x -= speed
        ground.angle += 5 
    else:
        ground.x = WIDTH
        count += 1
        enemy = random.randint(1,2)
        speed += 0.25
        
def bats():
    global count, enemy, speed, bat
    if bat.x > 0:
        bat.x -= speed
    else:
        bat.x = WIDTH
        count +=1
        enemy = random.randint(1,2)
        speed += 0.25
        bat.y = random.randint(120, 180)

def draw():
    if game_state == 0:
        screen.fill("black")
        screen.blit('fondo', (bg_x, 0))
        screen.blit('fondo', (bg_x + background.width, 0))
        prota.draw()
        screen.draw.text(str(count), pos=(10, 10), color="white", fontsize = 24)
    elif game_state == 1:
        background.draw()
        screen.draw.text('Press Enter', pos=(WIDTH/2 - 85, HEIGHT/2), color="red", fontsize=36, align='center')
    
    if enemy == 1:
        ground.draw()
    else:
        bat.draw()

def update(dt):
    global new_image, count, game_state, speed, bg_x, indice
    
    sounds.ost.play()
    
    bg_x -= bg_speed
    if bg_x <= -background.width:
        bg_x = 0
    
    if enemy == 1:
        grounds()
    else:
        bats()
        
    prota.image = lista_de_img[indice]
    indice += 1
    if indice == len(lista_de_img):
        indice = 0
    
    if prota.x <= WIDTH and (keyboard.RIGHT or keyboard.d):
        prota.x += 5
    if prota.x >= 0 and (keyboard.LEFT or keyboard.a):
        prota.x -= 5
    
    if game_state == 1 and keyboard.RETURN:
        game_state = 0 
        count = 0
        prota.pos = (50, 240)
        ground.pos = (550, 265)
        bat.pos = (550, 175)
        speed = 5
    
    if prota.colliderect(ground) or prota.colliderect(bat):
        game_state = 1
        
def on_key_down(key):
    if keyboard.space or keyboard.up or keyboard.w:
        prota.y = 100
        animate(prota, tween='bounce_end', duration=2, y=240)

pgzrun.go()