import pygame
import sys

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
            "background": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/background.jpg", "width": 1200, "height": 400},
            "end_screen": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/end_screen.jpeg", "width": 600, "height": 400}
        }
        
        self.images = {}
        self.load_images()
        
        # Initialize background scrolling variables and bird's properties
        self.flappy_y = self.screen_height // 2
        self.flappy_angle = 0  # Initialize the angle of the bird
        self.bg_x = 0
        self.bg_speed = 0.5
        self.gravity = 0.1  # Gravity value for smooth fall
        self.jump_strength = -3.0  # Strength of the jump
        self.flappy_velocity = 0  # Velocity of the bird

    def load_images(self):
        for key, config in self.image_configs.items():
            image = pygame.image.load(config["path"])
            image = pygame.transform.scale(image, (config["width"], config["height"]))
            self.images[key] = image

    def debug(self, frame_time):
        print("Frame time:", frame_time, "ms")

class FlappyBirdGame:
    def __init__(self):
        self.essentials = Essentials()
        self.jump_cooldown = 0  # Cooldown timer to control jump frequency

    def end_game(self):
        self.essentials.screen.blit(self.essentials.images["end_screen"], (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait 2 seconds before exiting
        self.essentials.running = False

    def jump(self):
        # Apply an upward velocity when jumping
        if self.jump_cooldown <= 0:  # Check cooldown to prevent immediate repeated jumps
            self.essentials.flappy_velocity = self.essentials.jump_strength
            self.jump_cooldown = 10  # Reset cooldown

    def apply_physics(self):
        # Apply gravity
        self.essentials.flappy_velocity += self.essentials.gravity

        # Update the bird's position
        self.essentials.flappy_y += self.essentials.flappy_velocity

        # Smoothly adjust the bird's angle based on its velocity
        max_angle = 25  # Maximum tilt angle
        rotation_speed = 2  # Speed at which the bird rotates

        if self.essentials.flappy_velocity > 0:  # Bird is going up
            target_angle = -max_angle
        else:  # Bird is going down
            target_angle = max_angle

        # Smoothly interpolate the current angle towards the target angle
        if self.essentials.flappy_angle < target_angle:
            self.essentials.flappy_angle = min(self.essentials.flappy_angle + rotation_speed, target_angle)
        elif self.essentials.flappy_angle > target_angle:
            self.essentials.flappy_angle = max(self.essentials.flappy_angle - rotation_speed, target_angle)

        # Prevent the bird from going off the screen with padding
        padding = 20  # Padding to avoid immediate game over when near edges
        if self.essentials.flappy_y > self.essentials.screen_height - padding or self.essentials.flappy_y < -padding:
            self.end_game()

        # Decrease jump cooldown
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def main(self):
        while self.essentials.running:
            start_time = pygame.time.get_ticks()  # Start time for the frame

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

            # Clear the screen
            self.essentials.screen.fill((0, 0, 0))  # Fill the screen with black

            # Draw background
            bg_image = self.essentials.images["background"]
            bg_width = bg_image.get_width()
            self.essentials.screen.blit(bg_image, (int(self.essentials.bg_x), 0))
            self.essentials.screen.blit(bg_image, (int(self.essentials.bg_x + bg_width), 0))
            
            # Draw Flappy Bird with rotation
            flappy_image = pygame.transform.rotate(self.essentials.images["flappy_bird"], self.essentials.flappy_angle)
            self.essentials.screen.blit(flappy_image, (50, self.essentials.flappy_y))
            
            pygame.display.flip()

            # Frame rate control and debug
            frame_time = pygame.time.get_ticks() - start_time  # Calculate frame time
            self.essentials.debug(frame_time)  # Print frame time for debugging
            self.essentials.clock.tick(60)


# Initialize pygame
pygame.init()

# Create game instance and run main loop
game = FlappyBirdGame()
game.main()

# Quit pygame
pygame.quit()
sys.exit()
  