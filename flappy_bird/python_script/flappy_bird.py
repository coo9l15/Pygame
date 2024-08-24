import pygame
import random
import json
import sys
import os

"""
This game is a remake of the flappy bird game!
It allows the user to play the game, view their stats and return to the home screen.
"""

class Pipe:
    def __init__(self, image, x, gap_height):
        self.image = image
        self.x = x
        self.gap_height = gap_height
        self.top_height = random.randint(150, 450)  # Random height for the top pipe

        # Bottom pipe's position is below the gap
        self.bottom_y = self.top_height + self.gap_height

        # Create masks for collision detection
        self.mask_top = pygame.mask.from_surface(pygame.transform.flip(self.image, False, True))
        self.mask_bottom = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        # Draw the top pipe (flipped vertically)
        top_pipe = pygame.transform.flip(self.image, False, True)
        screen.blit(top_pipe, (self.x, self.top_height - self.image.get_height()))
        
        # Draw the bottom pipe
        screen.blit(self.image, (self.x, self.bottom_y))

    def get_masks(self):
        top_pipe_pos = (self.x, self.top_height - self.image.get_height())
        bottom_pipe_pos = (self.x, self.bottom_y)
        return (self.mask_top, top_pipe_pos), (self.mask_bottom, bottom_pipe_pos)


class Essentials:
    def __init__(self):
        pygame.init()
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Flappy Bird")
        pygame.display.set_icon(pygame.image.load("/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png"))
        self.clock = pygame.time.Clock()
        self.running = True

        # Define the base path
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Dictionary to hold image paths and dimensions
        self.image_configs = {
            "flappy_bird": {"path": os.path.join(self.base_path, "../images/flappy_bird.png"), "width": 160, "height": 120},
            "background": {"path": os.path.join(self.base_path, "../images/background.jpg"), "width": self.screen_width, "height": self.screen_height},
            "font": {"path": os.path.join(self.base_path, "../images/minecraftia/Minecraftia-Regular.ttf")},
            "try_again_button": {"path": os.path.join(self.base_path, "../images/try_again_button.png"), "width": 500, "height": 300},
            "pipes": {"path": os.path.join(self.base_path, "../images/pipes.png"), "width": 200, "height": 800},
            "next": {"path": os.path.join(self.base_path, "../images/next.png"), "width": 400, "height": 400}
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
            print(f"Loading {key} from {config['path']}")  # Debugging statement
            if key == "font":
                self.font = pygame.font.Font(config["path"], 60)  # Load the font
            else:
                image = pygame.image.load(config["path"])
                image = pygame.transform.scale(image, (config["width"], config["height"]))
                self.images[key] = image


class FlappyBirdGame:
    def __init__(self):
        self.essentials = Essentials()
        self.pipes = []
        self.pipe_interval = 1500  # Time interval between pipe generations in milliseconds
        self.last_pipe_time = pygame.time.get_ticks()
        self.gap_height = 250  # Gap between top and bottom pipes
        self.pipe_speed = 5  # Speed at which pipes move left
        self.jump_cooldown = 0  # Cooldown timer to control jump frequency
        self.score = 0
        # Create mask for the bird
        self.bird_mask = pygame.mask.from_surface(self.essentials.images["flappy_bird"])
        self.next_arrow = pygame.Rect(1000, 800, 100, 100)
        self.return_button = pygame.Rect(self.essentials.screen_width // 2 - 250, 800, 500, 100)

    def reset_game(self):
        # Reset bird position and angle
        self.essentials.flappy_y = self.essentials.screen_height // 2
        self.essentials.flappy_angle = 0

        # Reset score
        self.score = 0

        # Reset pipes
        self.pipes = []

        # Reset pipe speed
        self.pipe_speed = 5
        # Reset any other relevant game state variables
        self.essentials.bg_x = 0
        self.essentials.running = True  

    def show_stats(self):
        limit = 10
        self.essentials.screen.fill((0, 0, 0))  # Clear the screen
        while self.essentials.running:
            try:
                with open("/Users/Avee/Documents/Pygame/flappy_bird/python_script/scores.json", "r") as file:
                    try:
                        stats = dict(json.load(file))
                        if not stats:
                            raise ValueError("No stats available")
                    except json.JSONDecodeError:
                        raise ValueError("Error reading stats")

                count = 0
                distance = 0
                stat = self.essentials.font.render(f"{count}: {stats.get(count)} stats", True, (255, 255, 255))
                self.essentials.screen.blit(stat, (50, 50))

                # Draw the "Try Again" button and arrow
                try_again_button = self.essentials.images["try_again_button"]
                next_arrow = self.essentials.images["next"]
                button_x = self.essentials.screen_width // 2 - try_again_button.get_width() // 2
                button_y = self.essentials.screen_height // 2 + 100
                self.essentials.button = pygame.Rect(button_x, button_y, try_again_button.get_width(), try_again_button.get_height())

                print(f"Drawing button at position: ({button_x}, {button_y})")  # Debugging statement

                self.essentials.screen.blit(try_again_button, (button_x, button_y))
                self.essentials.screen.blit(next_arrow, (self.essentials.screen_width - next_arrow.get_width() - 50, self.essentials.screen_height - next_arrow.get_height() - 50))

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.essentials.running = False
                            return
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            print(f"Mouse clicked at: {mouse_pos}")  # Debugging statement
                            if self.essentials.button.collidepoint(mouse_pos):
                                print("Try Again button clicked")  # Debugging statement
                                self.reset_game()  # Reset the game
                                self.home()
                            elif self.next_arrow.collidepoint(mouse_pos):
                                self.run()

                    pygame.display.flip()
                    self.essentials.clock.tick(60)

            except (FileNotFoundError, ValueError) as e:
                no_stats_text = self.essentials.font.render(str(e), True, (255, 255, 255))
                self.essentials.screen.blit(no_stats_text, (50, 50))
                self.essentials.screen.blit(self.essentials.images["try_again_button"], self.essentials.button)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.essentials.running = False
                            return
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            print(f"Mouse clicked at: {mouse_pos}")  # Debugging statement
                            if self.essentials.button.collidepoint(mouse_pos):
                                print("Try Again button clicked")  # Debugging statement
                                self.reset_game()  # Reset the game
                                self.home()

                    pygame.display.flip()
                    self.essentials.clock.tick(60)

    def home(self):
        while self.essentials.running:
            self.draw(game=False)
            # Scale the bird image
            scaled_bird = pygame.transform.scale(self.essentials.images["flappy_bird"], (800, 800))

            # Draw the bird with a 45-degree upward tilt
            rotated_bird = pygame.transform.rotate(scaled_bird, 45)
            bird_x = self.essentials.screen_width // 2 - rotated_bird.get_width() // 2
            bird_y = (self.essentials.screen_height // 2 - rotated_bird.get_height()) // 2 + 100
            self.essentials.screen.blit(rotated_bird, (bird_x, bird_y))

            try_again_button = self.essentials.images["try_again_button"]
            play_button_x = (self.essentials.screen_width // 2 - try_again_button.get_width() // 2) + 400
            play_button_y = (self.essentials.screen_height // 2) + 100
            stats_button_x = (self.essentials.screen_width // 2 - try_again_button.get_width() // 2) - 400
            stats_button_y = (self.essentials.screen_height // 2) + 100

            # Define buttons
            self.essentials.run_button = pygame.Rect(play_button_x, play_button_y, try_again_button.get_width(), try_again_button.get_height())
            self.essentials.stats_button = pygame.Rect(stats_button_x, stats_button_y, try_again_button.get_width(), try_again_button.get_height())

            # Blit buttons
            self.essentials.screen.blit(try_again_button, (play_button_x, play_button_y))
            self.essentials.screen.blit(try_again_button, (stats_button_x, stats_button_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.essentials.run_button.collidepoint(mouse_pos):
                        self.reset_game()
                        self.run()
                    elif self.essentials.stats_button.collidepoint(mouse_pos):
                        self.show_stats()

            pygame.display.flip()
            self.essentials.clock.tick(60)

    def end_game(self):
        self.essentials.screen.fill((0, 0, 0))
        final_score = self.essentials.font.render(f"Score: {self.score}", True, (255, 255, 255))
        game_over = self.essentials.font.render("Game Over", True, (255, 255, 255))
        try_again = self.essentials.font.render("Home", True, (255, 255, 255))
        try_again_button = self.essentials.images["try_again_button"]
    
        # Calculate positions
        button_x = self.essentials.screen_width // 2 - try_again_button.get_width() // 2
        button_y = self.essentials.screen_height // 2
        text_x = button_x + (try_again_button.get_width() - try_again.get_width()) // 2
        text_y = button_y + (try_again_button.get_height() - try_again.get_height()) // 2
    
        # Blit elements to the screen
        self.essentials.screen.blit(final_score, (self.essentials.screen_width // 2 - 150, self.essentials.screen_height // 2 - 200))
        self.essentials.screen.blit(game_over, (self.essentials.screen_width // 2 - 150, self.essentials.screen_height // 2 - 100))
        self.essentials.screen.blit(try_again_button, (button_x, button_y))
        self.essentials.screen.blit(try_again, (text_x, text_y))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.essentials.button.collidepoint(mouse_pos):
                        self.home()
            pygame.display.flip()
            self.essentials.clock.tick(60)

    def jump(self):
        if self.jump_cooldown <= 0:
            self.essentials.flappy_velocity = self.essentials.jump_strength
            self.jump_cooldown = 10  # Reset cooldown

    def generate_pipe(self):
        pipe_image = self.essentials.images["pipes"]
        new_pipe = Pipe(pipe_image, self.essentials.screen_width, self.gap_height)
        self.pipes.append(new_pipe)

    def update_pipes(self):
        for pipe in self.pipes:
            pipe.x -= self.pipe_speed

        # Remove pipes that are off the screen
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.image.get_width() > 0]

    def apply_physics(self):
        # Apply gravity
        self.essentials.flappy_velocity += self.essentials.gravity

        # Update the bird's position
        self.essentials.flappy_y += self.essentials.flappy_velocity

        # Smoothly adjust the bird's angle based on its velocity
        max_up_angle = 30  # Maximum upward tilt angle
        max_down_angle = -20  # Maximum downward tilt angle
        rotation_speed = 2  # Speed at which the bird rotates

        if self.essentials.flappy_velocity < 0:  # Bird is going up
            target_angle = max_up_angle
        else:  # Bird is going down
            target_angle = max_down_angle

        # Smoothly interpolate the current angle towards the target angle
        if self.essentials.flappy_angle > target_angle:
            self.essentials.flappy_angle = max(self.essentials.flappy_angle - rotation_speed, target_angle)
        elif self.essentials.flappy_angle < target_angle:
            self.essentials.flappy_angle = min(self.essentials.flappy_angle + rotation_speed, target_angle)

        # Prevent the bird from going off the screen with padding
        padding = 20  # Padding to avoid immediate game over when near edges
        if self.essentials.flappy_y > self.essentials.screen_height - padding or self.essentials.flappy_y < padding:
            self.end_game()

        # Decrease jump cooldown timer
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def draw(self, game=False):
        # Scroll the background
        self.essentials.bg_x -= self.essentials.bg_speed
        if self.essentials.bg_x <= -self.essentials.images["background"].get_width():
            self.essentials.bg_x = 0

        # Draw the scrolling background
        self.essentials.screen.blit(self.essentials.images["background"], (self.essentials.bg_x, 0))
        self.essentials.screen.blit(self.essentials.images["background"], (self.essentials.bg_x + self.essentials.images["background"].get_width(), 0))

        if game:
            # Draw the bird with its current rotation
            rotated_bird = pygame.transform.rotate(self.essentials.images["flappy_bird"], self.essentials.flappy_angle)
            self.essentials.screen.blit(rotated_bird, (50, self.essentials.flappy_y))

            # Draw pipes
            for pipe in self.pipes:
                pipe.draw(self.essentials.screen)

            # Draw the score
            score_text = self.essentials.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.essentials.screen.blit(score_text, (10, 10))

    def run(self):
        increase = 10
        while self.essentials.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jump()

            # Generate new pipes at regular intervals
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe_time > self.pipe_interval:
                self.generate_pipe()
                self.last_pipe_time = current_time

            # Update and draw everything
            self.apply_physics()
            self.update_pipes()

            # Check for collisions with pipes
            bird_pos = (50, self.essentials.flappy_y)
            for pipe in self.pipes:
                (mask_top, top_pos), (mask_bottom, bottom_pos) = pipe.get_masks()
                if self.bird_mask.overlap(mask_top, (top_pos[0] - bird_pos[0], top_pos[1] - bird_pos[1])) or self.bird_mask.overlap(mask_bottom, (bottom_pos[0] - bird_pos[0], bottom_pos[1] - bird_pos[1])):
                    self.end_game()
                    break  # End the game immediately if a collision is detected
                if pipe.x == 50:
                    # Bird has passed the pipe successfully
                    self.score += 1

            self.draw(game=True)

            # Refresh the screen
            pygame.display.flip()
            self.essentials.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = FlappyBirdGame()
    game.home()