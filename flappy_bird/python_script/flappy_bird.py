import pygame
import random
import sys
import essentials
class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.pipe_gap = 200
        self.running = True
        self.pipes = []
        self.score = 0
        self.clock = pygame.time.Clock()
        self.image_configs = {
            "pipes": {
                "path": "path_to_pipe_image"
            }
        }

    def create_pipes(self, pipe_image_path):
        pipe_image = pygame.image.load(pipe_image_path)
        top_pipe_height = random.randint(50, self.screen_height - self.pipe_gap - 50)
        top_pipe = pipe_image.copy()
        top_pipe = pygame.transform.flip(top_pipe, False, True)
        top_pipe_rect = top_pipe.get_rect(midbottom=(self.screen_width, top_pipe_height))

        bottom_pipe = pipe_image.copy()
        bottom_pipe_rect = bottom_pipe.get_rect(midtop=(self.screen_width, top_pipe_height + self.pipe_gap))

        return [top_pipe, bottom_pipe, top_pipe_rect, bottom_pipe_rect, False]  # Use list instead of tuple

    def generate_pipes(self):
        while self.running:
            pipes = self.create_pipes(self.image_configs["pipes"]["path"])
            self.pipes.append(pipes)
            pygame.time.wait(1500)  # Wait for 1.5 seconds before generating the next set of pipes

    def move_pipes(self):
        for pipe_set in self.pipes:
            top_pipe, bottom_pipe, top_pipe_rect, bottom_pipe_rect, passed = pipe_set

            top_pipe_rect.x -= 5  # Adjust speed as needed
            bottom_pipe_rect.x -= 5

            # Check if the pipe has passed the bird
            if not passed and top_pipe_rect.right < 50:  # 50 is the bird's x position
                self.score += 1
                pipe_set[4] = True  # Mark the pipe as passed

    def main(self):
        while self.running:
            start_time = pygame.time.get_ticks()  # Start time for the frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Move pipes
            self.move_pipes()

            # Clear the screen
            essentials.screen.fill((0, 0, 0))  # Fill the screen with black

            # Draw pipes
            for pipe_set in self.pipes:
                top_pipe, bottom_pipe, top_pipe_rect, bottom_pipe_rect, passed = pipe_set
                essentials.screen.blit(top_pipe, top_pipe_rect)
                essentials.screen.blit(bottom_pipe, bottom_pipe_rect)

            pygame.display.flip()

            # Frame rate control
            self.clock.tick(60)

# Create game instance and run main loop
game = FlappyBirdGame()
game.main()

# Quit pygame
pygame.quit()
sys.exit()