import pygame
import sys

class Essentials:
    def __init__ (self):
        self.screen = pygame.display.set_mode((600, 400))
        self.clock = pygame.time.Clock()
        self.running = True
        self.images = {
            "flappy_bird": pygame.image.load("flappy_bird/images/flappy_bird.png")
        }
class Game:
    # Main loop of the game
    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Flappy Bird")
        pygame.display.set_icon(images["flappy_bird"])  # Set the icon of the window
        clock = pygame.time.Clock()
        running = True
        test = pygame.Surface((100, 100))  # Create a surface with size 100x100
        test.fill((255, 255, 255))  # Fill the image with white

        while running:
            screen.fill((0, 0, 0))  # Fill the screen with black before drawing the image
            screen.blit(test, (200, 100))  # Draw the image on the screen
            screen.blit(images["flappy_bird"], (200, 200))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the game loop

            pygame.display.update()
            clock.tick(60)

        pygame.quit()  # Quit pygame properly
        sys.exit()

if __name__ == "__main__":
    # Load images
    images = {
        "flappy_bird": pygame.image.load("flappy_bird/images/flappy_bird.png")
    }

    # Create and run the game
    game = Game()
    game.main()
