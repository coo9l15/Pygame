import threading
import pygame
import random
import sys
from pathlib import Path
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

    def update(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.image.get_width() < 0

    def get_masks(self):
        top_pipe_pos = (self.x, self.top_height - self.image.get_height())
        bottom_pipe_pos = (self.x, self.bottom_y)
        return (self.mask_top, top_pipe_pos), (self.mask_bottom, bottom_pipe_pos)

class Essentials:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen_width = 1400
        self.screen_height = 850
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.font = pygame.font.Font("images/minecraftia/Minecraftia-Regular.ttf", 50)

        # Set up image and sound paths relative to the application's path
        self.image_configs = {
            "background": {"path":  "images/background.jpg", "width": self.screen_width + 50, "height": self.screen_height},
            "flappy_bird": {"path":  "images/flappy_bird.png", "width": 160, "height": 120},
            "try_again_button": {"path":  "images/try_again_button.png", "width": 500, "height": 300},
            "pipes": {"path":  "images/pipes.png", "width": 150, "height": 800},
            "next": {"path":  "images/next.png", "width": 400, "height": 400}
        }

        self.wavs = {
            "background":  "sounds/background.wav",
            "jump":  "sounds/jump.wav",
            "click":  "sounds/button_click.wav"
        }

        # Handle paths dynamically based on if the app is frozen or running from source
        self.application_path = self.get_application_path()

        self.images = {}

        # Initialize other game properties
        self.flappy_y = self.screen_height // 2
        self.flappy_angle = 0  # Initialize the angle of the bird
        self.bg_x = 0
        self.bg_speed = 0.5
        self.gravity = 0.4  # Gravity value for smooth fall
        self.jump_strength = -9  # Strength of the jump
        self.flappy_velocity = 0  # Velocity of the bird
        self.button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 100, 200, 100)  # Center the button and set its dimensions
        self.clock = pygame.time.Clock()

        self.load_images()
        self.load_sounds()

    def get_application_path(self):
        """Helper function to determine the correct application path depending on whether the app is frozen or not."""
        if getattr(sys, 'frozen', False):
            # If running as a bundled executable
            return os.path.dirname(sys.executable)
        else:
            # If running in a normal Python environment
            return os.path.dirname(os.path.abspath(__file__))

    def get_resource_path(self, path):
        """Helper function to get the correct path to resources."""
        base_path = Path(self.application_path)
        return base_path / path

    def load_images(self):
        """Load all images dynamically from the image_configs dictionary."""
        for image_key, image_config in self.image_configs.items():
            # Load the image using the specified path
            image_path = self.get_resource_path(image_config["path"])
            try:
                image = pygame.image.load(image_path)
            except pygame.error as e:
                print(f"Error loading image '{image_path}': {e}")

                # Handle the error, e.g., exit the program or display an error message
                sys.exit()
            image = pygame.transform.scale(image, (image_config["width"], image_config["height"]))

            # Store the processed image in the self.images dictionary
            self.images[image_key] = image

    def load_sounds(self):
        """Load sound files."""
        for key, path in self.wavs.items():
            sound_path = self.get_resource_path(path)
            self.wavs[key] = pygame.mixer.Sound(sound_path)
            
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
        pygame.mixer.init()  # Initialize the mixer
        self.music = True
        threading.Thread(target=self.home_async).start()

    def home_async(self):
        # Load the sound only once
        background_sound = pygame.mixer.Sound(self.essentials.wavs["background"])

        # Main loop for playing the sound
        while self.music:
            # Check if the sound is still playing
            if not pygame.mixer.get_busy():
                background_sound.play()
            # Adding a slight delay to prevent busy waiting
            pygame.time.delay(100)


    def reset_game(self):
        # Reset bird position and angle
        self.essentials.flappy_y = self.essentials.screen_height // 2
        self.essentials.flappy_angle = 0
        self.essentials.gravity = 0.4
        # Reset score
        self.score = 0

        # Reset pipes
        self.pipes = []

        # Reset any other relevant game state variables
        self.essentials.bg_x = 0
        self.essentials.running = True  
        self.flappy_velocity = 0

    def delete_data(self):
        # Clear the screen by filling it with a background color
        self.essentials.screen.fill((0, 0, 0))  # Fill with black color or any other background color

        # Render warning texts
        warning_text = self.essentials.font.render("This will delete all of your data", True, (255, 255, 255))
        warning_text2 = self.essentials.font.render("Are you sure?", True, (255, 255, 255))
        delete_text = self.essentials.font.render("Delete", True, (255, 255, 255))
        home_text = self.essentials.font.render("Home", True, (255, 255, 255))

        # Define button images
        button_img = self.essentials.images["try_again_button"]
        button_width = button_img.get_width()
        button_height = button_img.get_height()

        # Calculate positions for buttons to be side by side
        total_width = button_width * 2 + 20  # 20 pixels gap between buttons
        start_x = (self.essentials.screen_width - total_width) // 2
        delete_button_x = start_x
        home_button_x = start_x + button_width + 20
        button_y = (self.essentials.screen_height // 2) + 100

        # Define buttons
        self.essentials.delete_button = pygame.Rect(delete_button_x, button_y, button_width, button_height)
        self.essentials.home_button = pygame.Rect(home_button_x, button_y, button_width, button_height)

        # Get text rectangles
        warning_text_rect = warning_text.get_rect(center=(self.essentials.screen_width // 2, self.essentials.screen_height // 2))
        warning_text2_rect = warning_text2.get_rect(center=(self.essentials.screen_width // 2, self.essentials.screen_height // 2 + 50))
        delete_text_rect = delete_text.get_rect(center=self.essentials.delete_button.center)
        home_text_rect = home_text.get_rect(center=self.essentials.home_button.center)

        # Blit elements to the screen
        self.essentials.screen.blit(button_img, self.essentials.delete_button.topleft)
        self.essentials.screen.blit(button_img, self.essentials.home_button.topleft)
        self.essentials.screen.blit(warning_text, warning_text_rect)
        self.essentials.screen.blit(warning_text2, warning_text2_rect)
        self.essentials.screen.blit(delete_text, delete_text_rect)
        self.essentials.screen.blit(home_text, home_text_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.music = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound(self.essentials.wavs["click"]).play()
                    if self.essentials.delete_button.collidepoint(event.pos):
                        # Delete the stats file
                        try:
                            with open("scores.txt", "w") as file:
                                file.write("")
                        except FileNotFoundError:
                            os.mkdir("scores.txt")
                        return  # Exit the function after deleting the file
                    elif self.essentials.home_button.collidepoint(event.pos):
                        return  # Exit the function to return to the home screen

            pygame.display.flip()
            self.essentials.clock.tick(60)

    def show_stats(self):
        self.essentials.screen.fill((0, 0, 0))  # Clear the screen
        try:
            with open("scores.txt", "r") as file:
                # Read all lines, strip whitespace, and sort in reverse order
                stats = sorted([line.strip() for line in file.readlines()], reverse=True)
        except FileNotFoundError:
            os.mkdir("scores.txt")
            stats = []

        if not stats:
            no_stats_text = self.essentials.font.render("No stats available", True, (255, 255, 255))
            return_text = self.essentials.font.render("Return", True, (255, 255, 255))
            self.essentials.screen.blit(no_stats_text, (50, 50))

            button_img = self.essentials.images["try_again_button"]
            button_rect = button_img.get_rect(center=self.essentials.button.center)
            return_text_rect = return_text.get_rect(center=button_rect.center)

            self.essentials.screen.blit(button_img, button_rect.topleft)
            self.essentials.screen.blit(return_text, return_text_rect)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.Sound(self.essentials.wavs["click"]).play()
                        mouse_pos = pygame.mouse.get_pos()
                        if self.essentials.button.collidepoint(mouse_pos):
                            self.home()
                pygame.display.flip()
                self.essentials.clock.tick(60)

        current_index = 0
        limit = len(stats)

        try_again_button = self.essentials.images["try_again_button"]
        next_arrow = self.essentials.images["next"]
        back_arrow = pygame.transform.rotate(next_arrow, 180)

        button_x = self.essentials.screen_width // 2 - try_again_button.get_width() // 2
        button_y = self.essentials.screen_height // 2 + 100
        self.essentials.button = pygame.Rect(button_x, button_y, try_again_button.get_width(), try_again_button.get_height())

        next_arrow_x = self.essentials.screen_width - next_arrow.get_width() - 50
        next_arrow_y = self.essentials.screen_height - next_arrow.get_height() - 50
        next_arrow_rect = pygame.Rect(next_arrow_x, next_arrow_y, next_arrow.get_width(), next_arrow.get_height())

        back_arrow_x = 50
        back_arrow_y = self.essentials.screen_height - back_arrow.get_height() - 50
        back_arrow_rect = pygame.Rect(back_arrow_x, back_arrow_y, back_arrow.get_width(), back_arrow.get_height())

        return_text = self.essentials.font.render("Return", True, (255, 255, 255))
        next_text = self.essentials.font.render("Next Stat", True, (255, 255, 255))
        prev_text = self.essentials.font.render("Previous Stat", True, (255, 255, 255))
        return_text_rect = return_text.get_rect(center=self.essentials.button.center)

        self.essentials.screen.blit(try_again_button, (button_x, button_y))
        self.essentials.screen.blit(return_text, return_text_rect)
        if current_index < limit - 1:
            self.essentials.screen.blit(next_text, (next_arrow_x, next_arrow_y + 100))
            self.essentials.screen.blit(next_arrow, (next_arrow_x, next_arrow_y))
        if current_index > 0:
            self.essentials.screen.blit(prev_text, (back_arrow_x, back_arrow_y + 100))
            self.essentials.screen.blit(back_arrow, (back_arrow_x, back_arrow_y))

        while True:
            self.essentials.screen.fill((0, 0, 0))  # Clear the screen
            stats_text = self.essentials.font.render(f"Stats {current_index + 1}/{limit}", True, (255, 255, 255))
            score_text = self.essentials.font.render(f"Score: {stats[current_index].strip()}", True, (255, 255, 255))
            self.essentials.screen.blit(stats_text, (50, 50))
            self.essentials.screen.blit(score_text, (50, 150))

            self.essentials.screen.blit(try_again_button, (self.essentials.button.x, self.essentials.button.y))
            self.essentials.screen.blit(return_text, return_text_rect)
            if current_index < limit - 1:
                self.essentials.screen.blit(next_arrow, (next_arrow_x, next_arrow_y))
                next_text = self.essentials.font.render("Next", True, (255, 255, 255))
                next_text_rect = next_text.get_rect(center=(next_arrow_x + next_arrow.get_width() // 2, next_arrow_y - 20))
                self.essentials.screen.blit(next_text, next_text_rect)
            if current_index > 0:
                self.essentials.screen.blit(back_arrow, (back_arrow_x, back_arrow_y))
                prev_text = self.essentials.font.render("Previous", True, (255, 255, 255))
                prev_text_rect = prev_text.get_rect(center=(back_arrow_x + back_arrow.get_width() // 2, back_arrow_y - 20))
                self.essentials.screen.blit(prev_text, prev_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound(self.essentials.wavs["click"]).play()
                    mouse_pos = pygame.mouse.get_pos()
                    if self.essentials.button.collidepoint(mouse_pos):
                        self.home()
                    elif next_arrow_rect.collidepoint(mouse_pos) and current_index < limit - 1:
                        current_index += 1
                    elif back_arrow_rect.collidepoint(mouse_pos) and current_index > 0:
                        current_index -= 1

            pygame.display.flip()
            self.essentials.clock.tick(60)
    
    def home(self):
        scaled_font = pygame.font.Font("images/minecraftia/Minecraftia-Regular.ttf", 100)
        while self.essentials.running:
            self.draw(game=False)
            # Scale the bird image
            scaled_bird = pygame.transform.scale(self.essentials.images["flappy_bird"], (800, 800))

            # Draw the bird with a 45-degree upward tilt
            rotated_bird = pygame.transform.rotate(scaled_bird, 45)
            bird_x = self.essentials.screen_width // 2 - rotated_bird.get_width() // 2
            bird_y = (self.essentials.screen_height // 2 - rotated_bird.get_height()) // 2 - 80
            title = scaled_font.render("Flappy Bird", True, (255, 255, 255))
            self.essentials.screen.blit(title, (self.essentials.screen_width // 2 - 325, self.essentials.screen_height // 2 - 100))
            self.essentials.screen.blit(rotated_bird, (bird_x, bird_y))

            try_again_button = self.essentials.images["try_again_button"]
            play_button_x = (self.essentials.screen_width // 2 - try_again_button.get_width() // 2) + 400
            play_button_y = (self.essentials.screen_height // 2) + 200

            stats_button_x = (self.essentials.screen_width // 2 - try_again_button.get_width() // 2) - 400
            stats_button_y = (self.essentials.screen_height // 2) + 200

            delete_button_x = (self.essentials.screen_width // 2 - try_again_button.get_width() // 2)
            delete_button_y = (self.essentials.screen_height // 2)

            # Define buttons
            self.essentials.run_button = pygame.Rect(play_button_x, play_button_y, try_again_button.get_width(), try_again_button.get_height())
            self.essentials.stats_button = pygame.Rect(stats_button_x, stats_button_y, try_again_button.get_width(), try_again_button.get_height())
            self.essentials.delete_button = pygame.Rect(delete_button_x, delete_button_y, try_again_button.get_width(), try_again_button.get_height())

            # Blit buttons
            self.essentials.screen.blit(try_again_button, (play_button_x, play_button_y))
            self.essentials.screen.blit(try_again_button, (stats_button_x, stats_button_y))
            self.essentials.screen.blit(try_again_button, (delete_button_x, delete_button_y))

            # Render text
            play_text = self.essentials.font.render("Play", True, (255, 255, 255))
            stats_text = self.essentials.font.render("Stats", True, (255, 255, 255))
            delete_text = self.essentials.font.render("Delete Stats", True, (255, 255, 255))

            # Center text on buttons
            play_text_rect = play_text.get_rect(center=self.essentials.run_button.center)
            stats_text_rect = stats_text.get_rect(center=self.essentials.stats_button.center)
            delete_text_rect = delete_text.get_rect(center=self.essentials.delete_button.center)

            # Blit text
            self.essentials.screen.blit(play_text, play_text_rect)
            self.essentials.screen.blit(stats_text, stats_text_rect)
            self.essentials.screen.blit(delete_text, delete_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.essentials.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pygame.mixer.Sound(self.essentials.wavs["click"]).play()
                        mouse_pos = pygame.mouse.get_pos()
                        if self.essentials.run_button.collidepoint(mouse_pos):
                            self.reset_game()
                            self.run()
                        elif self.essentials.stats_button.collidepoint(mouse_pos):
                            self.show_stats()
                        elif self.essentials.delete_button.collidepoint(mouse_pos):
                            self.delete_data()
            pygame.display.flip()
            self.essentials.clock.tick(60)

    def end_game(self):
        try:
            with open("scores.txt", "r") as file:
                stats = file.readlines()
        except FileNotFoundError:
            stats = []
            os.system("touch scores.txt")
        with open("scores.txt" ,"a") as file:
            stats.append(str(self.score) + "\n")
            file.writelines(stats)
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
                    pygame.mixer.Sound(self.essentials.wavs["click"]).play()
                    mouse_pos = pygame.mouse.get_pos()
                    if self.essentials.button.collidepoint(mouse_pos):
                        self.home()
            pygame.display.flip()
            self.essentials.clock.tick(60)

    def jump(self):
        if self.jump_cooldown <= 0:
            pygame.mixer.Sound(self.essentials.wavs["jump"]).play()
            self.essentials.flappy_velocity = self.essentials.jump_strength
            self.jump_cooldown = 10  # Reset cooldown

    def generate_pipe(self):
        pipe_image = self.essentials.images["pipes"]
        new_pipe = Pipe(pipe_image, self.essentials.screen_width, self.gap_height)
        self.pipes.append(new_pipe)

    def update_pipes(self):
        for pipe in self.pipes:
            pipe.update(self.pipe_speed)

        # Remove pipes that are off the screen
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]


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
        if abs(self.essentials.bg_x) > self.essentials.images["background"].get_width():
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
        index = 3
        TIME = 0

        # Render the initial "Get Ready" message
        get_ready = self.essentials.font.render(f"Get Ready {index}", True, (255, 255, 255))

        # Main loop to display the "Get Ready" message and update the screen
        while index != 0:
            # Clear the screen and draw the background
            self.essentials.screen.blit(self.essentials.images["background"], (0, 0))

            # Draw the bird
            self.essentials.screen.blit(self.essentials.images["flappy_bird"], (50, self.essentials.flappy_y))

            # Draw the "Get Ready" message
            get_ready = self.essentials.font.render(f"Get Ready {index}", True, (255, 255, 255))
            self.essentials.screen.blit(get_ready, (self.essentials.screen_width // 2 - 150, self.essentials.screen_height // 2 - 100))

            # Update the display
            pygame.display.flip()

            # Wait for 1 second
            pygame.time.wait(1000)

            # Increment the time and index
            TIME += 1000
            if TIME % 1000 == 0:
                index -= 1

            # Tick the clock
            self.essentials.clock.tick(60)

        # Reset the game after the loop
        self.reset_game()
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
