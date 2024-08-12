import pygame
import sys
import time

class Essentials:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Dictionary to hold image paths and dimensions
        self.image_configs = {
            "flappy_bird": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png", "width": 80, "height": 60},
            "background": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/background.jpg", "width": 1200, "height": 400}
        }
        
        self.images = {}
        self.load_images()
        
        # Initialize background scrolling variables and bird's properties
        self.flappy_y = 100
        self.flappy_angle = 0  # Initialize the angle of the bird
        self.bg_x = 0
        self.bg_speed = 0.5
        self.gravity = 0.05  # Gravity value
        self.jump_strength = -2.5 # Jump strength
        self.flappy_velocity = 0  # Velocity of the bird

    def load_images(self):
        for key, config in self.image_configs.items():
            image = pygame.image.load(config["path"])
            image = pygame.transform.scale(image, (config["width"], config["height"]))
            self.images[key] = image

class FlappyBirdGame:
    def __init__(self):
        self.essentials = Essentials()

    def jump(self):
        # Apply an upward velocity when jumping
        self.essentials.flappy_velocity = self.essentials.jump_strength

    def apply_physics(self):
        # Apply gravity over time
        self.essentials.flappy_velocity += self.essentials.gravity
        
        # Cap the falling speed to avoid sudden increases
        self.essentials.flappy_velocity = min(self.essentials.flappy_velocity, 3)
        
        # Update the bird's position
        self.essentials.flappy_y += self.essentials.flappy_velocity

        # Limit the bird's rotation based on its velocity
        if self.essentials.flappy_velocity < 0:  # Bird is going up
            self.essentials.flappy_angle = min(self.essentials.flappy_angle + 2, 30)
        else:  # Bird is going down
            self.essentials.flappy_angle = max(self.essentials.flappy_angle - 2, -20)

    def main(self):
        while self.essentials.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jump()

            # Apply physics to the bird
            self.apply_physics()

            # Update background position
            self.essentials.bg_x -= self.essentials.bg_speed
            if self.essentials.bg_x <= -self.essentials.images["background"].get_width():
                self.essentials.bg_x = 0

            # Draw background
            bg_image = self.essentials.images["background"]
            bg_width = bg_image.get_width()
            self.essentials.screen.blit(bg_image, (int(self.essentials.bg_x), 0))
            self.essentials.screen.blit(bg_image, (int(self.essentials.bg_x + bg_width), 0))
            
            # Draw Flappy Bird with rotation
            flappy_image = pygame.transform.rotate(self.essentials.images["flappy_bird"], self.essentials.flappy_angle)
            self.essentials.screen.blit(flappy_image, (50, self.essentials.flappy_y))
            
            pygame.display.flip()
            self.essentials.clock.tick(60)

# Initialize pygame
pygame.init()

# Create game instance and run main loop
game = FlappyBirdGame()
game.main()

# Quit pygame
pygame.quit()
sys.exit()
