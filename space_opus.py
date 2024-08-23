import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the player
player_width, player_height = 50, 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Set up the bullets
bullet_width, bullet_height = 5, 15
bullet_speed = 10
bullets = []

# Set up the invaders
invader_width, invader_height = 50, 50
invader_speed = 2
invaders = []
invader_rows = 3
invader_cols = 10
invader_spacing_x = 20
invader_spacing_y = 20

# Set up the fast invaders
fast_invader_speed = 4
fast_invaders = []
fast_invader_rows = 1
fast_invader_cols = 5

# Set up the shooting invaders
shooting_invader_speed = 1
shooting_invaders = []
shooting_invader_rows = 1
shooting_invader_cols = 3
shooting_invader_cooldown = 60
shooting_invader_timer = 0

# Create the invaders
for row in range(invader_rows):
    for col in range(invader_cols):
        invader_x = col * (invader_width + invader_spacing_x) + 50
        invader_y = row * (invader_height + invader_spacing_y) + 50
        invader = pygame.Rect(invader_x, invader_y, invader_width, invader_height)
        invaders.append(invader)

# Create the fast invaders
for row in range(fast_invader_rows):
    for col in range(fast_invader_cols):
        fast_invader_x = col * (invader_width + invader_spacing_x) + 50
        fast_invader_y = row * (invader_height + invader_spacing_y) + 200
        fast_invader = pygame.Rect(fast_invader_x, fast_invader_y, invader_width, invader_height)
        fast_invaders.append(fast_invader)

# Create the shooting invaders
for row in range(shooting_invader_rows):
    for col in range(shooting_invader_cols):
        shooting_invader_x = col * (invader_width + invader_spacing_x) + 50
        shooting_invader_y = row * (invader_height + invader_spacing_y) + 350
        shooting_invader = pygame.Rect(shooting_invader_x, shooting_invader_y, invader_width, invader_height)
        shooting_invaders.append(shooting_invader)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player.x + player_width // 2 - bullet_width // 2
                bullet_y = player.y - bullet_height
                bullet = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
                bullets.append(bullet)

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < width - player_width:
        player.x += player_speed

    # Move the bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move the invaders
    for invader in invaders:
        invader.x += invader_speed
        if invader.x <= 0 or invader.x >= width - invader_width:
            invader_speed *= -1
            for inv in invaders:
                inv.y += invader_height // 2

    # Move the fast invaders
    for fast_invader in fast_invaders:
        fast_invader.x += fast_invader_speed
        if fast_invader.x <= 0 or fast_invader.x >= width - invader_width:
            fast_invader_speed *= -1
            for inv in fast_invaders:
                inv.y += invader_height // 2

    # Move the shooting invaders and shoot bullets
    shooting_invader_timer += 1
    if shooting_invader_timer >= shooting_invader_cooldown:
        shooting_invader_timer = 0
        for shooting_invader in shooting_invaders:
            bullet_x = shooting_invader.x + invader_width // 2 - bullet_width // 2
            bullet_y = shooting_invader.y + invader_height
            bullet = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
            bullets.append(bullet)

    for shooting_invader in shooting_invaders:
        shooting_invader.x += shooting_invader_speed
        if shooting_invader.x <= 0 or shooting_invader.x >= width - invader_width:
            shooting_invader_speed *= -1
            for inv in shooting_invaders:
                inv.y += invader_height // 2

    # Check for collisions
    for bullet in bullets:
        for invader in invaders:
            if bullet.colliderect(invader):
                bullets.remove(bullet)
                invaders.remove(invader)
        for fast_invader in fast_invaders:
            if bullet.colliderect(fast_invader):
                bullets.remove(bullet)
                fast_invaders.remove(fast_invader)
        for shooting_invader in shooting_invaders:
            if bullet.colliderect(shooting_invader):
                bullets.remove(bullet)
                shooting_invaders.remove(shooting_invader)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the player
    pygame.draw.rect(screen, WHITE, player)

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Draw the invaders
    for invader in invaders:
        pygame.draw.rect(screen, WHITE, invader)

    # Draw the fast invaders
    for fast_invader in fast_invaders:
        pygame.draw.rect(screen, (200, 200, 200), fast_invader)

    # Draw the shooting invaders
    for shooting_invader in shooting_invaders:
        pygame.draw.rect(screen, (150, 150, 150), shooting_invader)

    # Update the display
    pygame.display.flip()
    clock.tick(60)
