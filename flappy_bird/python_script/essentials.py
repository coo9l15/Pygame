import pygame

# Initialize Pygame
pygame.init()
# Screen dimensions
screen_width = 1500
screen_height = 900

# Create screen and set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load("/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png"))

# Load font
font = pygame.font.Font("flappy_bird/images/minecraftia/Minecraftia-Regular.ttf", 60)

# Dictionary for images
image_configs = {
    "flappy_bird": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/flappy_bird.png", "width": 160, "height": 120},
    "background": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/background.jpg", "width": screen_width*2, "height": screen_height},
    "try_again_button": {"path": "/Users/Avee/Documents/Pygame/flappy_bird/images/try_again_button.png", "width": 500, "height": 300}
}

# Dictionary to hold loaded images
images = {}
for key, config in image_configs.items():
    if key == "font":
        continue  # Font is already loaded
    image = pygame.image.load(config["path"])
    image = pygame.transform.scale(image, (config["width"], config["height"]))
    images[key] = image

# Initialize game variables
clock = pygame.time.Clock()
running = True
flappy_y = screen_height // 2
flappy_angle = 0
bg_x = 0
bg_speed = 0.5
gravity = 0.4
jump_strength = -10
flappy_velocity = 0

# Button rectangle for collision detection
button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 100)
