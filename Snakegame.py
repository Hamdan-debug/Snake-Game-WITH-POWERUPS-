import pygame
import random
import time


# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)      # Apple color
YELLOW = (255, 255, 0) # Banana color
BLUE = (0, 0, 255)     # Pineapple color
BOMB_COLOR = (128, 0, 128) # Bomb color (purple)

# Food definition
FOODS = {
    'apple': {'color': RED, 'score': 10, 'speed_change': 0},
    'banana': {'color': YELLOW, 'score': 100, 'speed_change': 5},
    'pineapple': {'color': BLUE, 'score': 1000, 'speed_change': 0},
    'bomb': {'color': BOMB_COLOR, 'score': -50, 'speed_change': -5}
}

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')


pygame.mixer.music.load('song2.mp3')  
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1) 



# Define initial parameters
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]  # Initial size of the snake
snake_direction = 'RIGHT'
change_to = snake_direction
speed = 10
score = 0
food_items = []  # List to store food items
last_spawn_time = time.time()  # Track last time food was spawned
food_spawn_interval = 2  # Time in seconds between food spawns

# Function to generate random food position
def get_random_food_position():
    return [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]

# Function to choose random food
def get_random_food():
    food_type = random.choice(list(FOODS.keys()))
    position = get_random_food_position()
    return food_type, position

# Game over function
def game_over():
    font = pygame.font.SysFont('arial', 35)
    game_over_surface = font.render('Game Over!', True, RED)
    score_surface = font.render('Your Score: ' + str(score), True, WHITE)
    restart_surface = font.render('Press R to Restart or Q to Quit', True, YELLOW)

    screen.fill(BLACK)
    screen.blit(game_over_surface, [WIDTH / 4, HEIGHT / 4])
    screen.blit(score_surface, [WIDTH / 4, HEIGHT / 3])
    screen.blit(restart_surface, [WIDTH / 4, HEIGHT / 2])
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main game loop
def main():
    global score, snake_pos, snake_body, snake_direction, speed, food_items, last_spawn_time
    
    # Reset game parameters
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]  # Initial size of the snake
    snake_direction = 'RIGHT'
    change_to = snake_direction
    speed = 10
    score = 0
    food_items = []  # Clear existing food items
    last_spawn_time = time.time()  # Reset last spawn time

    # Initial food generation
    for _ in range(3):  # Spawn 3 initial fruit items
        food_type, position = get_random_food()
        food_items.append((food_type, position))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'

        # Update the snake's direction
        snake_direction = change_to

        # Move the snake
        if snake_direction == 'UP':
            snake_pos[1] -= speed
        if snake_direction == 'DOWN':
            snake_pos[1] += speed
        if snake_direction == 'LEFT':
            snake_pos[0] -= speed
        if snake_direction == 'RIGHT':
            snake_pos[0] += speed

        # Check if the snake eats any food
        for food in food_items:
            food_type, food_position = food
            
            if snake_pos == food_position:
                food_info = FOODS[food_type]
                score += food_info['score']
                speed += food_info['speed_change']

                # Grow the snake by adding new segment(s)
                if food_info['score'] > 0:  # Only grow on valid food
                    snake_body.append(snake_body[-1])  # Add a segment at the end

                food_items.remove(food)  # Remove the eaten food
                break  # Exit the loop after consuming food

        # Update snake body
        if len(snake_body) > 0:
            # Keep the snake's length based on the position of the body and head
            if snake_body[0] != snake_pos:
                # Maintain the same length of the snake
                snake_body.pop()  

            
            snake_body.insert(0, list(snake_pos))
        else:
            snake_body.append(list(snake_pos))

        
        screen.fill(BLACK)

    
        for pos in snake_body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

        for food in food_items:
            food_type, food_position = food
            food_info = FOODS[food_type]
            pygame.draw.rect(screen, food_info['color'], pygame.Rect(food_position[0], food_position[1], 10, 10))

        
        if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= HEIGHT or
            snake_pos in snake_body[1:]):  
            game_over()

        
        font = pygame.font.SysFont('arial', 20)
        score_surface = font.render('Score: ' + str(score), True, WHITE)
        screen.blit(score_surface, [10, 10])

        
        current_time = time.time()
        if current_time - last_spawn_time > food_spawn_interval:
            food_type, position = get_random_food()
            food_items.append((food_type, position))  
            last_spawn_time = current_time  

        
        pygame.display.flip()

        pygame.time.Clock().tick(15)

if __name__ == "__main__":
    main()