import pygame
from pygame.locals import *
import time
import random

size = 40

class Apple:
    def __init__(self, parent_screen):

        self.parent_screen = parent_screen

        self.image = pygame.image.load("resources/apple.jpg").convert()

        self.x = size * 3
        self.y = size * 3

    def draw(self):

        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):

        self.x = random.randint(0, 24) * size
        self.y = random.randint(0, 16) * size

class Snake:

    def __init__(self, parent_screen, length):

        self.parent_screen = parent_screen

        self.block = pygame.image.load("resources/block.jpg").convert()

        self.length = length

        self.x = [size] * length
        self.y = [size] * length

        self.direction = "right"

        self.last_direction = "right"

    def increase_length(self):

        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.flip()

    def move_left(self):

        if self.last_direction != "right":  
            self.direction = "left"

    def move_right(self):

        if self.last_direction != "left":  
            self.direction = "right"

    def move_down(self):

        if self.last_direction != "up":  
            self.direction = "down"

    def move_up(self):

        if self.last_direction != "down":  
            self.direction = "up"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= size

        elif self.direction == "right":
            self.x[0] += size

        elif self.direction == "up":
            self.y[0] -= size

        elif self.direction == "down":
            self.y[0] += size

        self.last_direction = self.direction
        self.draw()

class Game:

    def __init__(self):

        pygame.init()

        pygame.mixer.init()

        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 680))

        self.snake = Snake(self.surface, 1)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

        self.speed = 0.2

    def render_background(self):

        bg= pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def display_score(self):

        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score : {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (850, 5))

    def play_background_music(self):

        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1,0)

    def reset(self):

        self.snake = Snake(self.surface, 1)

        self.apple = Apple(self.surface)

        self.speed = 0.2

    def play(self):

        self.render_background()

        self.snake.walk()

        self.apple.draw()

        self.display_score()

        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):

            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)

            self.snake.increase_length()

            self.apple.move()

            self.speed = max(0.05, self.speed - 0.01)

        for i in range(2, self.snake.length):

            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/crash.mp3")

                pygame.mixer.Sound.play(sound)

                raise RuntimeError("Game Over")

        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 680):
            raise RuntimeError("Game Over")

    def is_collision(self, x1, y1, x2, y2):

        if abs(x1 - x2) < size and abs(y1 - y2) < size:
            return True

        return False

    def show_game_over(self):

        self.render_background()

        font = pygame.font.SysFont("arial", 25)

        line1 = font.render(f"Your game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))

        line2 = font.render("To play again, press Enter. To exit, press Escape.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def run(self):

        running = True

        pause = False

        while running:

            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
    
            except RuntimeError:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.speed)

if __name__ == "__main__":
    
    game = Game()
    
    game.run()