import pygame
from pygame.locals import *  # Import necessary constants like K_UP, K_DOWN, etc.
import time  # For adding delays in the game loop
import random  # To randomize apple positions

# Define the size of each block in the grid
size = 40

class Apple:
    def __init__(self, parent_screen):
        """Initialize the apple with a parent screen and position."""
        self.parent_screen = parent_screen  # Reference to the game's surface
        self.image = pygame.image.load("resources/apple.jpg").convert()  # Load apple image
        self.x = size * 3  # Initial x-coordinate of the apple
        self.y = size * 3  # Initial y-coordinate of the apple

    def draw(self):
        """Draw the apple on the screen."""
        self.parent_screen.blit(self.image, (self.x, self.y))  # Place apple image at its position
        pygame.display.flip()  # Update the screen

    def move(self):
        """Randomly move the apple to a new position."""
        self.x = random.randint(0, 24) * size  # Random x-coordinate
        self.y = random.randint(0, 16) * size  # Random y-coordinate

class Snake:
    def __init__(self, parent_screen, length):
        """Initialize the snake with a given length."""
        self.parent_screen = parent_screen  # Reference to the game's surface
        self.block = pygame.image.load("resources/block.jpg").convert()  # Load snake block image
        self.length = length  # Initial length of the snake
        self.x = [size] * length  # Initialize x-coordinates for each block of the snake
        self.y = [size] * length  # Initialize y-coordinates for each block of the snake
        self.direction = "right"  # Initial movement direction
        self.last_direction = "right"  # Used to prevent instant reversal

    def increase_length(self):
        """Increase the length of the snake."""
        self.length += 1  # Add one to the snake's length
        self.x.append(-1)  # Add placeholder for new block's x-coordinate
        self.y.append(-1)  # Add placeholder for new block's y-coordinate

    def draw(self):
        """Draw the snake on the screen."""
        for i in range(self.length):  # Draw each block of the snake
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()  # Update the screen

    # Movement methods, ensure no immediate reversal of direction
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
        """Move the snake by updating its position."""
        for i in range(self.length - 1, 0, -1):  # Shift each block to the position of the block ahead of it
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update the head based on the direction
        if self.direction == "left":
            self.x[0] -= size
        elif self.direction == "right":
            self.x[0] += size
        elif self.direction == "up":
            self.y[0] -= size
        elif self.direction == "down":
            self.y[0] += size

        self.last_direction = self.direction  # Update the last direction
        self.draw()  # Redraw the snake

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()  # Initialize pygame
        pygame.mixer.init()  # Initialize pygame's sound mixer
        self.play_background_music()  # Start background music
        self.surface = pygame.display.set_mode((1000, 680))  # Create the game window
        self.snake = Snake(self.surface, 1)  # Create a snake with one block
        self.snake.draw()  # Draw the snake
        self.apple = Apple(self.surface)  # Create an apple
        self.apple.draw()  # Draw the apple
        self.speed = 0.2  # Initial speed of the snake

    def render_background(self):
        """Draw the background image."""
        bg = pygame.image.load("resources/background.jpg")  # Load the background image
        self.surface.blit(bg, (0, 0))  # Draw it on the screen

    def display_score(self):
        """Display the current score."""
        font = pygame.font.SysFont("arial", 30)  # Load the font
        score = font.render(f"Score : {self.snake.length}", True, (255, 255, 255))  # Render the score
        self.surface.blit(score, (850, 5))  # Display the score in the top-right corner

    def play_background_music(self):
        """Play the background music."""
        pygame.mixer.music.load("resources/bg_music_1.mp3")  # Load the music file
        pygame.mixer.music.play(-1, 0)  # Play the music on a loop

    def reset(self):
        """Reset the game state."""
        self.snake = Snake(self.surface, 1)  # Create a new snake
        self.apple = Apple(self.surface)  # Create a new apple
        self.speed = 0.2  # Reset the speed

    def play(self):
        """Main game logic."""
        self.render_background()  # Draw the background
        self.snake.walk()  # Move the snake
        self.apple.draw()  # Draw the apple
        self.display_score()  # Display the score
        pygame.display.flip()  # Update the screen

        # Check collision with the apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resources/ding.mp3")  # Load sound effect
            pygame.mixer.Sound.play(sound)  # Play sound effect
            self.snake.increase_length()  # Increase snake length
            self.apple.move()  # Move the apple to a new position
            self.speed = max(0.05, self.speed - 0.01)  # Increase speed

        # Check collision with the snake's body
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/crash.mp3")  # Load crash sound
                pygame.mixer.Sound.play(sound)  # Play crash sound
                raise RuntimeError("Game Over")  # End the game

        # Check collision with the boundaries
        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 680):
            raise RuntimeError("Game Over")  # End the game

    def is_collision(self, x1, y1, x2, y2):
        """Check if two objects collide."""
        if abs(x1 - x2) < size and abs(y1 - y2) < size:  # Collision condition
            return True
        return False

    def show_game_over(self):
        """Display the Game Over screen."""
        self.render_background()  # Draw the background
        font = pygame.font.SysFont("arial", 25)  # Load the font
        line1 = font.render(f"Your game is over! Your score is {self.snake.length}", True, (255, 255, 255))  # Game over text
        self.surface.blit(line1, (200, 300))  # Display the text
        line2 = font.render("To play again, press Enter. To exit, press Escape.", True, (255, 255, 255))  # Restart instructions
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()  # Update the screen
        pygame.mixer.music.pause()  # Pause the music

    def run(self):
        """Main game loop."""
        running = True  # Game is running
        pause = False  # Pause state

        while running:  # Run until the game is stopped
            for event in pygame.event.get():
                if event.type == KEYDOWN:  # Key press events
                    if event.key == K_ESCAPE:  # Quit the game
                        running = False

                    if event.key == K_RETURN:  # Restart after Game Over
                        pygame.mixer.music.unpause()  # Resume music
                        pause = False

                    if not pause:  # Allow movement if not paused
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:  # Quit event
                    running = False

            try:
                if not pause:
                    self.play()  # Execute game logic
            except RuntimeError:
                self.show_game_over()  # Show Game Over screen
                pause = True
                self.reset()  # Reset the game

            time.sleep(self.speed)  # Control game speed

if __name__ == "__main__":
    game = Game()
    game.run()
