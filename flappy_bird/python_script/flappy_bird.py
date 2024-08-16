import pygame
import sys

class Essentials:
    def __init__(self):
        pygame.init()
        self.screen_width = 1500
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Dictionary to hold image paths and dimensions
        self.image_configs = {
            "flappy_bird": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png", "width": 160, "height": 120},
            "background": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/background.jpg", "width": self.screen_width*2, "height": self.screen_height},
            "font": {"path": "flappy_bird/images/minecraftia/Minecraftia-Regular.ttf"},
            "try_again_button": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/try_again_button.png", "width": 500, "height": 300}
        }

        self.images = {}
        self.load_images()
        
        # Initialize background scrolling variables and bird's properties
        self.flappy_y = self.screen_height // 2
        self.flappy_angle = 0  # Initialize the angle of the bird
        self.bg_x = 0
        self.bg_speed = 0.5
        self.gravity = 0.4  # Gravity value for smooth fall
        self.jump_strength = -10  # Strength of the jump
        self.flappy_velocity = 0  # Velocity of the bird
        self.button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 100, 200, 100)  # Center the button and set its dimensions

    def load_images(self):
        for key, config in self.image_configs.items():
            if key == "font":
                self.font = pygame.font.Font(config["path"], 60)  # Load the font
            else:
                image = pygame.image.load(config["path"])
                image = pygame.transform.scale(image, (config["width"], config["height"]))
                self.images[key] = image

class FlappyBirdGame:
    def __init__(self):
        self.essentials = Essentials()
        self.jump_cooldown = 0  # Cooldown timer to control jump frequency

    def end_game(self):
        score = 0  # Example score; update this with the actual score if tracked
        self.essentials.screen.fill((0, 0, 0))  # Fill the screen with black
        font = self.essentials.font  # Load the font
        final_result = font.render(f"Score: {score}", True, (255, 255, 255))  # Render the score text
        try_again_text = font.render("Try again", True, (255, 255, 255))  # Render "Try again" text
        heading = font.render("Game Over", True, (255, 255, 255))  # Render "Game Over" text

        self.essentials.screen.blit(heading, (self.essentials.screen_width // 2 - heading.get_width() // 2, self.essentials.screen_height // 2 - heading.get_height() // 2 - 50))
        self.essentials.screen.blit(final_result, (self.essentials.screen_width // 2 - final_result.get_width() // 2, self.essentials.screen_height // 2 - final_result.get_height() // 2 + 50))

        # Center the "try again" button
        button_width = self.essentials.image_configs["try_again_button"]["width"]
        button_height = self.essentials.image_configs["try_again_button"]["height"]
        button_x = (self.essentials.screen_width - button_width) // 2
        button_y = (self.essentials.screen_height - button_height) // 2 + 200  # Adjust the y position as needed

        self.essentials.screen.blit(self.essentials.images["try_again_button"], (button_x, button_y))

        # Center the "try again" text inside the button
        text_x = button_x + (button_width - try_again_text.get_width()) // 2
        text_y = button_y + (button_height - try_again_text.get_height()) // 2
        self.essentials.screen.blit(try_again_text, (text_x, text_y))

        pygame.display.flip()

        # Event loop for the end game screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.essentials.button.collidepoint(mouse_x, mouse_y):
                        self.restart_game()
                        return  # Exit the end game screen loop
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
            self.essentials.clock.tick(60)

    def restart_game(self):
        # Reset bird's position and physics
        self.essentials.flappy_y = self.essentials.screen_height // 2
        self.essentials.flappy_velocity = 0
        self.essentials.flappy_angle = 0

        # Reset background scrolling
        self.essentials.bg_x = 0

        # Reset game state variables
        self.jump_cooldown = 0

        # Continue the game loop
        self.essentials.running = True
        self.main()

# Create game instance and run main loop
game = FlappyBirdGame()
game.main()

# Quit pygame
pygame.quit()
sys.exit()
