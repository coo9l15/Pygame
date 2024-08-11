import pygame
import sys
import time
import threading

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
            "flappy_bird": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png", "width": 80, "height": 40},
            "background": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/background.jpg", "width": 1200, "height": 400}  # Ensure this width is >= 2 * screen_width
        }
        
        self.images = {}
        self.load_images()
        
        # Initialize background scrolling variables and bird 'y' position
        self.flappy_y = 100
        self.bg_x = 0
        self.bg_speed = 0.5

    def load_images(self):
        for key, config in self.image_configs.items():
            image = pygame.image.load(config["path"])
            image = pygame.transform.scale(image, (config["width"], config["height"]))
            self.images[key] = image

class FlappyBirdGame:
    def __init__(self):
        self.essentials = Essentials()

    def set_bg_speed(self, speed):
        # Set the speed of the background scrolling.
        self.essentials.bg_speed = speed

    def repeat(self):
        times = 0
        while times < 20:
            self.essentials.flappy_y -= 2
            times += 1
            time.sleep(0.01)

    def main(self):
        while self.essentials.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Move Flappy Bird up when spacebar is pressed
                        threading.Thread(target=self.repeat).start()

            # Update background position
            self.essentials.flappy_y += 1  # Make Flappy Bird fall down
            self.essentials.bg_x -= self.essentials.bg_speed

            # Reset background position when it moves off-screen
            bg_image = self.essentials.images["background"]
            bg_width = bg_image.get_width()
            if self.essentials.bg_x <= -bg_width:
                self.essentials.bg_x = 0

            # Draw background twice side by side
            self.essentials.screen.blit(bg_image, (int(self.essentials.bg_x), 0))
            self.essentials.screen.blit(bg_image, (int(self.essentials.bg_x + bg_width), 0))
            
            # Draw Flappy Bird
            flappy_image = self.essentials.images["flappy_bird"]
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
