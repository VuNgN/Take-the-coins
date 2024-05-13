import pygame
import sys
import random
from player import Player
from coin import Coin
from obstacle import Obstacle

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (135, 206, 235)  # Sky Blue
MENU_BACKGROUND_COLOR = (255, 255, 255)  # White
FONT_COLOR = (0, 0, 0)  # Black
FONT_MENU_COLOR = (255, 255, 255)
FONT_SIZE = 24
FPS = 60

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Take the Coins")

# Font
font = pygame.font.Font(None, FONT_SIZE)

# Load logo
logo_image = pygame.image.load("logo.png")
logo_rect = logo_image.get_rect()
logo_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Start screen loop
show_start_screen = True
def start_screen():
    global show_start_screen
    show_start_screen = True
    while show_start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_start_screen = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(logo_image, logo_rect)

        # Display instructions
        start_text = font.render("Press ENTER to start", True, FONT_MENU_COLOR)
        esc_text = font.render("Press ESC to quit", True, FONT_MENU_COLOR)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))
        screen.blit(esc_text, (SCREEN_WIDTH // 2 - esc_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4 + 30))

        pygame.display.flip()


# Create player
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

# Create coins
coins = pygame.sprite.Group()
for _ in range(10):
    coin = Coin(SCREEN_WIDTH, SCREEN_HEIGHT)
    coins.add(coin)

# Create obstacles
obstacles = pygame.sprite.Group()
for _ in range(5):
    obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT)
    obstacles.add(obstacle)

# Clock
clock = pygame.time.Clock()

# Game variables
points = 0
time_elapsed = 0

# Menu variables
show_menu = False
menu_options = ["Resume", "Settings", "Tutorial", "Quit"]
selected_option = 0

# Function to render the menu
def render_menu():
    screen.fill(MENU_BACKGROUND_COLOR)  # Background color for menu
    menu_text = font.render("Menu Screen", True, FONT_COLOR)
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 4))
    for i, option in enumerate(menu_options):
        text = font.render(f"{option}", True, FONT_COLOR)  # Display option with index
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4 + 40 + i * 40))

# Main game loop
while True:
    start_screen()  # Show the start screen and wait for the player to start the game
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Reset player position

    # Reset game variables
    points = 0
    time_elapsed = 0
    show_menu = False
    show_ending_screen = False
    
    running = True
    global show_end_screen
    show_end_screen = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not show_menu and not show_end_screen:
                    if event.key == pygame.K_SPACE:
                        show_menu = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif show_menu:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Resume
                            show_menu = False
                        elif selected_option == 1:  # Settings
                            pass  # Placeholder for settings
                        elif selected_option == 2:  # Tutorial
                            pass  # Placeholder for tutorial
                        elif selected_option == 3:  # Quit
                            pygame.quit()
                            sys.exit()
                elif show_end_screen:
                    if event.key == pygame.K_RETURN:
                        # Return to start screen when pressing Enter on the end screen
                        show_end_screen = False
                        points = 0
                        time_elapsed = 0
                        start_screen()  # Show start screen again

        if not show_menu and not show_end_screen:
            # Player movement
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.update(dx, dy)

            # Obstacle movement
            for obstacle in obstacles:
                obstacle.update(obstacles)

            # Collision detection with coins
            collected_coins = pygame.sprite.spritecollide(player, coins, True)
            for coin in collected_coins:
                points += 1
                coin = Coin(SCREEN_WIDTH, SCREEN_HEIGHT)
                coins.add(coin)

            # Collision detection with obstacles
            if pygame.sprite.spritecollide(player, obstacles, False):
                # Player hit an obstacle
                show_end_screen = True  # Show end screen when player hits an obstacle

            # Update time elapsed
            time_elapsed += 1 / FPS

            # Draw everything
            screen.fill(BACKGROUND_COLOR)
            screen.blit(player.image, player.rect)
            coins.draw(screen)
            obstacles.draw(screen)

            # Display points and time
            points_text = font.render(f"Points: {points}", True, FONT_COLOR)
            time_text = font.render(f"Time: {int(time_elapsed)}s", True, FONT_COLOR)
            screen.blit(points_text, (10, 10))
            screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 10))
        else:
            if show_menu:
                render_menu()
                pygame.draw.rect(screen, FONT_COLOR, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 4 + 30 + selected_option * 40, 200, 30), 2)
            elif show_end_screen:
                # Display end screen with total points and time survived
                screen.fill(BACKGROUND_COLOR)
                end_text = font.render("Game Over!", True, FONT_COLOR)
                total_points_text = font.render(f"Total Points: {points}", True, FONT_COLOR)
                time_survived_text = font.render(f"Time Survived: {int(time_elapsed)}s", True, FONT_COLOR)
                return_text = font.render("Press ENTER to return to start screen", True, FONT_MENU_COLOR)
                screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 4))
                screen.blit(total_points_text, (SCREEN_WIDTH // 2 - total_points_text.get_width() // 2, SCREEN_HEIGHT // 2))
                screen.blit(time_survived_text, (SCREEN_WIDTH // 2 - time_survived_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
                screen.blit(return_text, (SCREEN_WIDTH // 2 - return_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# Game over
pygame.quit()
sys.exit()
