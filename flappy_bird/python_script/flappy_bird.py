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
            "flappy_bird": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png", "width": 80, "height": 40},
            "background": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/background.png", "width": 600, "height": 400}
            # Add more images and their dimensions here
        }
        
        self.images = {}
        self.load_images()

    def load_images(self):
        for key, config in self.image_configs.items():
            try:
                original_image = pygame.image.load(config["path"])
                scaled_image = pygame.transform.scale(original_image, (config["width"], config["height"]))
                self.images[key] = scaled_image
                if key == "flappy_bird":
                    pygame.display.set_icon(scaled_image)  # Set the icon of the window for flappy_bird
                print(f"Image '{key}' loaded and scaled successfully")
                print("Image size after scaling:", scaled_image.get_size())
            except pygame.error as e:
                print(f"Unable to load image at {config['path']}: {e}")
                self.images[key] = None

class Game:
    def __init__(self, essentials):
        self.essentials = essentials

    def main(self):
        while self.essentials.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False

            self.essentials.screen.fill((0, 0, 0))  # Fill the screen with black
            
            # Draw all images
            positions = {
                "flappy_bird": (50, 50),  # Example position
                "background": (0, 0)      # Example position
                # Add more positions as needed
            }
            
            for key, pos in positions.items():
                if key in self.essentials.images and self.essentials.images[key] is not None:
                    self.essentials.screen.blit(self.essentials.images[key], pos)
                else:
                    print(f"Image '{key}' not found in images dictionary")

            pygame.display.flip()  # Use flip for complete screen update
            self.essentials.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    essentials = Essentials()
    game = Game(essentials)
    game.main()
