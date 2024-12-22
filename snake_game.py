# Import the necessary libraries
import pygame
import sys
import random

# Initialize the pygame library
pygame.init()

# Set the dimensions of the game window
window_width = 800
window_height = 600
game_window = pygame.display.set_mode((window_width, window_height))

# Set the title of the game window
pygame.display.set_caption('Snake Game')

# Define the colors used in the game
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Set the font for the score display
font = pygame.font.SysFont('arial', 30)

# Set the initial score
score = 0
high_score = 0

# Constants
BLOCK_SIZE = 10
FPS = 15

# Initialize the clock
clock = pygame.time.Clock()

# Set the initial snake position and direction
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'right'
next_direction = direction

# Define the initial food position
food_position = [random.randrange(1, (window_width // BLOCK_SIZE)) * BLOCK_SIZE,
                 random.randrange(1, (window_height // BLOCK_SIZE)) * BLOCK_SIZE]

# Ensure the food does not overlap with the snake's body
while food_position in snake_body:
    food_position = [random.randrange(1, (window_width // BLOCK_SIZE)) * BLOCK_SIZE,
                     random.randrange(1, (window_height // BLOCK_SIZE)) * BLOCK_SIZE]

# Game states
game_states = ['playing', 'paused', 'game_over']
game_state = game_states[0]

# Sound effects
eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over_sound.wav')

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction!= 'down':
                next_direction = 'up'
            elif event.key == pygame.K_DOWN and direction!= 'up':
                next_direction = 'down'
            elif event.key == pygame.K_LEFT and direction!= 'right':
                next_direction = 'left'
            elif event.key == pygame.K_RIGHT and direction!= 'left':
                next_direction = 'right'
            elif event.key == pygame.K_p and game_state == game_states[0]:
                game_state = game_states[1]
            elif event.key == pygame.K_r and game_state == game_states[2]:
                game_state = game_states[0]
                score = 0
                snake_position = [100, 50]
                snake_body = [[100, 50], [90, 50], [80, 50]]
                direction = 'right'
                next_direction = direction
                food_position = [random.randrange(1, (window_width // BLOCK_SIZE)) * BLOCK_SIZE,
                                 random.randrange(1, (window_height // BLOCK_SIZE)) * BLOCK_SIZE]

    # Update the snake's direction
    if game_state == game_states[0]:
        direction = next_direction

    # Move the snake
    if game_state == game_states[0]:
        if direction == 'up':
            snake_position[1] -= BLOCK_SIZE
        elif direction == 'down':
            snake_position[1] += BLOCK_SIZE
        elif direction == 'left':
            snake_position[0] -= BLOCK_SIZE
        elif direction == 'right':
            snake_position[0] += BLOCK_SIZE

        # Add the new head position to the snake body
        snake_body.insert(0, list(snake_position))

        # Check if the snake has eaten the food
        if snake_position == food_position:
            score += 1
            eat_sound.play()
            food_position = [random.randrange(1, (window_width // BLOCK_SIZE)) * BLOCK_SIZE,
                             random.randrange(1, (window_height // BLOCK_SIZE)) * BLOCK_SIZE]
            while food_position in snake_body:
                food_position = [random.randrange(1, (window_width // BLOCK_SIZE)) * BLOCK_SIZE,
                                 random.randrange(1, (window_height // BLOCK_SIZE)) * BLOCK_SIZE]
        else:
            # Remove the last element of the snake body if the snake hasn't eaten the food
            snake_body.pop()

        # Check for collision with the window boundaries or the snake's body
        if (snake_position[0] < 0 or snake_position[0] >= window_width or
            snake_position[1] < 0 or snake_position[1] >= window_height):
            game_state = game_states[2]
            game_over_sound.play()
        for block in snake_body[1:]:
            if snake_position == block:
                game_state = game_states[2]
                game_over_sound.play()

    # Draw everything
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(game_window, white, pygame.Rect(food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))
    text = font.render(f'Score: {score}', True, white)
    game_window.blit(text, [0, 0])
    if game_state == game_states[1]:
        text = font.render('Game Paused', True, red)
        game_window.blit(text, [window_width // 2 - 100, window_height // 2])
    elif game_state == game_states[2]:
        text = font.render('Game Over', True, red)
        game_window.blit(text, [window_width // 2 - 100, window_height // 2])
        text = font.render(f'Final Score: {score}', True, white)
        game_window.blit(text, [window_width // 2 - 100, window_height // 2 + 50])
        text = font.render('Press R to restart', True, white)
        game_window.blit(text, [window_width // 2 - 100, window_height // 2 + 100])
    pygame.display.update()

    # Control game speed
    clock.tick(FPS)

    # Save high score
    if score > high_score:
        high_score = score
        with open('high_score.txt', 'w') as f:
            f.write(str(high_score))