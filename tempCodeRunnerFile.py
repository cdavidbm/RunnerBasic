import pgzrun
import random
from pgzero.builtins import Actor, animate, keyboard
from dataclasses import dataclass

# Constantes
WIDTH = 600
HEIGHT = 300
TITLE = "Corredor de protaígenas"
FPS = 30
INITIAL_SPEED = 5
SPEED_INCREMENT = 0.25
GROUND_Y = 265
BAT_Y_RANGE = (120, 180)
PLAYER_START_POS = (50, 240)
ENEMY_START_X = 550

@dataclass
class GameState:
    game_over: bool = False
    score: int = 0
    speed: float = INITIAL_SPEED
    bg_x: float = 0
    animation_index: int = 0
    current_enemy: int = random.randint(1, 2)

class Game:
    def __init__(self):
        self.state = GameState()
        self.player = Actor("1", PLAYER_START_POS, size=(80, 80))
        self.background = Actor("fondo")
        self.ground = Actor('ground', (ENEMY_START_X, GROUND_Y))
        self.bat = Actor('bat', (ENEMY_START_X, 175))
        self.animation_frames = ["1", "2", "3", "4", "5", "6"]
        
    def reset(self):
        self.state = GameState()
        self.player.pos = PLAYER_START_POS
        self.ground.pos = (ENEMY_START_X, GROUND_Y)
        self.bat.pos = (ENEMY_START_X, 175)

    def update_ground(self):
        if self.ground.x > 0:
            self.ground.x -= self.state.speed
            self.ground.angle += 5
        else:
            self.ground.x = WIDTH
            self._handle_enemy_reset()

    def update_bat(self):
        if self.bat.x > 0:
            self.bat.x -= self.state.speed
        else:
            self.bat.x = WIDTH
            self.bat.y = random.randint(*BAT_Y_RANGE)
            self._handle_enemy_reset()

    def _handle_enemy_reset(self):
        self.state.score += 1
        self.state.current_enemy = random.randint(1, 2)
        self.state.speed += SPEED_INCREMENT

    def handle_input(self):
        if keyboard.RIGHT or keyboard.d:
            self.player.x += 5
        if keyboard.LEFT or keyboard.a:
            self.player.x -= 5

    def update_animation(self):
        self.player.image = self.animation_frames[self.state.animation_index]
        self.state.animation_index = (self.state.animation_index + 1) % len(self.animation_frames)

game = Game()

def draw():
    if not game.state.game_over:
        screen.fill("black")
        screen.blit('fondo', (game.state.bg_x, 0))
        screen.blit('fondo', (game.state.bg_x + game.background.width, 0))
        game.player.draw()
        screen.draw.text(str(game.state.score), pos=(10, 10), color="white", fontsize=24)
        
        if game.state.current_enemy == 1:
            game.ground.draw()
        else:
            game.bat.draw()
    else:
        game.background.draw()
        screen.draw.text('Press Enter', pos=(WIDTH/2 - 85, HEIGHT/2), color="red", fontsize=36, align='center')

def update(dt):
    if game.state.game_over:
        if keyboard.RETURN:
            game.reset()
        return

    game.state.bg_x -= 2
    if game.state.bg_x <= -game.background.width:
        game.state.bg_x = 0

    if game.state.current_enemy == 1:
        game.update_ground()
    else:
        game.update_bat()

    game.update_animation()
    game.handle_input()

    if game.player.colliderect(game.ground) or game.player.colliderect(game.bat):
        game.state.game_over = True

def on_key_down(key):
    if not game.state.game_over and (keyboard.space or keyboard.up or keyboard.w):
        game.player.y = 100
        animate(game.player, tween='bounce_end', duration=2, y=240)

pgzrun.go()