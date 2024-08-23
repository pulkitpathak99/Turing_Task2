import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display with hardware surfaces and double buffering
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load sprite sheet
enemy_sheet = pygame.image.load("enemy_spritesheet.png").convert_alpha()

# Player settings
player_width = 50
player_height = 50
player_speed = 5
player_lives = 3

# Bullet settings
bullet_width = 5
bullet_height = 15
bullet_speed = 7

# Game state
level = 1
score = 0
boss_active = False

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - player_height - 10))
        self.speed = player_speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, position, enemy_type, health=1):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.type = enemy_type
        self.speed = 1 + level * 0.2
        self.time = 0
        self.shoot_cooldown = 0
        self.health = health

    def update(self):
        if self.type == "basic":
            self.rect.y += self.speed
        elif self.type == "zigzag":
            self.rect.y += self.speed
            self.rect.x += math.sin(self.time * 0.1) * 2
            self.time += 1
        elif self.type == "shooter":
            self.rect.y += self.speed * 0.5
            if self.shoot_cooldown == 0:
                self.shoot()
                self.shoot_cooldown = max(30, 60 - level * 5)
            else:
                self.shoot_cooldown -= 1
        elif self.type == "boss":
            if self.rect.y < 50:
                self.rect.y += self.speed
            else:
                self.rect.x += math.sin(self.time * 0.05) * 3
                self.time += 1
            if self.shoot_cooldown == 0:
                self.shoot()
                self.shoot_cooldown = max(15, 30 - level * 2)
            else:
                self.shoot_cooldown -= 1

        # Check if the enemy is off-screen
        if self.rect.top > HEIGHT:
            self.kill()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        bullet.image.fill(RED)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

        if self.type == "boss":
            bullet_left = Bullet(self.rect.centerx - 20, self.rect.bottom)
            bullet_right = Bullet(self.rect.centerx + 20, self.rect.bottom)
            bullet_left.image.fill(RED)
            bullet_right.image.fill(RED)
            all_sprites.add(bullet_left)
            all_sprites.add(bullet_right)
            enemy_bullets.add(bullet_left)
            enemy_bullets.add(bullet_right)


# Explosion pool for reusing explosions
class ExplosionPool:
    def __init__(self, size):
        self.pool = [Explosion() for _ in range(size)]
        self.active = []

    def get_explosion(self):
        if self.pool:
            explosion = self.pool.pop()
            self.active.append(explosion)
            return explosion
        return None

    def return_explosion(self, explosion):
        if explosion in self.active:
            self.active.remove(explosion)
            self.pool.append(explosion)


# Explosion class (for future use)
class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def reset(self, x, y):
        self.rect.topleft = (x, y)

    def update(self):
        # Explosion logic goes here
        pass


# Spawn enemies
def spawn_enemies():
    global boss_active
    enemy_width=20
    enemy_height=10
    if level % 5 == 0 and not boss_active:
        boss = Enemy(enemy_sheet.subsurface((0, 0, 64, 64)), (WIDTH // 2 - 32, -64), "boss", health=10 + level // 5 * 5)
        all_sprites.add(boss)
        enemies.add(boss)
        boss_active = True
    else:
        enemy_types = ["basic", "zigzag", "shooter"]
        for i in range(3 + level): 
            for j in range(5 + level):
                enemy_x = j * (enemy_width + 10) + 50
                enemy_y = i * (enemy_height + 10) + 50
                enemy_type = random.choice(enemy_types)
                enemy = Enemy(enemy_sheet.subsurface((0, 0, 32, 32)), (enemy_x, enemy_y), enemy_type)
                all_sprites.add(enemy)
                enemies.add(enemy)


# Draw text on the screen
def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


# Initialize player
player = Player()
all_sprites.add(player)

# Initialize explosion pool
explosion_pool = ExplosionPool(20)

# Start the game loop
clock = pygame.time.Clock()
running = True
spawn_enemies()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update all sprites
    all_sprites.update()

    # Check for collisions between bullets and enemies
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, False)
    for bullet, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.health -= 1
            if enemy.health <= 0:
                if enemy.type == "boss":
                    score += 100
                else:
                    score += 10
                enemy.kill()

    # Check for collisions between player and enemy bullets
    if pygame.sprite.spritecollideany(player, enemy_bullets):
        player_lives -= 1
        if player_lives <= 0:
            print(f"Game Over! Final Score: {score}")
            running = False

    # Check for level completion
    if not enemies:
        level += 1
        player_lives = min(player_lives + 1, 5)  # Bonus life, max 5
        boss_active = False
        spawn_enemies()

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw HUD
    draw_text(f"Score: {score}", 36, WIDTH // 2, 10)
    draw_text(f"Lives: {player_lives}", 36, 60, 10)
    draw_text(f"Level: {level}", 36, WIDTH - 60, 10)

    # Refresh the display with dirty rects
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
