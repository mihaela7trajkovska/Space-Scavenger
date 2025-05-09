import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
INITIAL_ASTEROID_SPEED = 3
INITIAL_CRYSTAL_SPEED = 2
SPEED_INCREASE_RATE = 0.1
SPAWN_RATE = 60
CRYSTAL_SPAWN_RATE = 120


class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Asteroid:
    def __init__(self, image, game_speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.bottom = 0
        self.speed = INITIAL_ASTEROID_SPEED * game_speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Crystal:
    def __init__(self, image, game_speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.bottom = 0
        self.speed = INITIAL_CRYSTAL_SPEED * game_speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Scavenger")
        self.clock = pygame.time.Clock()
        self.load_resources()
        self.reset_game()

    def load_resources(self):
        # Get the correct path to assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets src directory
        assets_dir = os.path.join(current_dir, '..', 'assets')  # Go up one level and into assets

        # Debug print to verify path
        print(f"Looking for assets in: {assets_dir}")

        # Load images with correct case sensitivity
        self.spaceship_img = pygame.image.load(
            os.path.join(assets_dir, "spaceship.png")).convert_alpha()
        self.asteroid_img = pygame.image.load(
            os.path.join(assets_dir, "asteroid.png")).convert_alpha()
        self.crystal_img = pygame.image.load(
            os.path.join(assets_dir, "energy_crystal.png")).convert_alpha()

        # Load sounds
        self.background_music = pygame.mixer.Sound(
            os.path.join(assets_dir, "background_music.wav"))
        self.clash_sound = pygame.mixer.Sound(
            os.path.join(assets_dir, "clash_sound.wav"))

        # Scale images
        self.spaceship_img = pygame.transform.scale(self.spaceship_img, (50, 50))
        self.asteroid_img = pygame.transform.scale(self.asteroid_img, (40, 40))
        self.crystal_img = pygame.transform.scale(self.crystal_img, (30, 30))

    def reset_game(self):
        self.player = Player(self.spaceship_img)
        self.asteroids = []
        self.crystals = []
        self.score = 0
        self.game_speed = 1
        self.spawn_counter = 0
        self.crystal_spawn_counter = 0
        self.game_over = False
        self.background_music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                self.reset_game()
        return True

    def update(self):
        if self.game_over:
            return

        # Update player
        self.player.update()

        # Spawn asteroids
        self.spawn_counter += 1
        if self.spawn_counter >= SPAWN_RATE:
            self.asteroids.append(Asteroid(self.asteroid_img, self.game_speed))
            self.spawn_counter = 0

        # Spawn crystals
        self.crystal_spawn_counter += 1
        if self.crystal_spawn_counter >= CRYSTAL_SPAWN_RATE:
            self.crystals.append(Crystal(self.crystal_img, self.game_speed))
            self.crystal_spawn_counter = 0

        # Update game objects
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if asteroid.rect.top > SCREEN_HEIGHT:
                self.asteroids.remove(asteroid)
            elif self.player.rect.colliderect(asteroid.rect):
                self.game_over = True
                self.clash_sound.play()
                self.background_music.stop()

        for crystal in self.crystals[:]:
            crystal.update()
            if crystal.rect.top > SCREEN_HEIGHT:
                self.crystals.remove(crystal)
            elif self.player.rect.colliderect(crystal.rect):
                self.crystals.remove(crystal)
                self.score += 10
                self.game_speed += SPEED_INCREASE_RATE

    def draw(self):
        self.screen.fill(BLACK)

        # Draw game objects
        self.player.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for crystal in self.crystals:
            crystal.draw(self.screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()


def main():
    game = Game()
    running = True

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        game.clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()



