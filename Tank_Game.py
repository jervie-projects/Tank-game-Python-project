# Akia, Jervie Martin H.
# BSIT-2B
# 2200730

import pygame
import sys
import random
# mixer helps us add an audio track in the background
from pygame import mixer

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
border_margin = 20

# Initialize Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Game ni Akia")

# Load background image
# Make sure you have a background image. Change the background image to your liking. Use creative commons images or DYI.
battle_field = pygame.image.load("Images/battlefield.jpg")

# Load tank image
# Draw your own tank or get images from the internet but use creative commons/unlicensed images.
tank_img = pygame.image.load("Images/AkiaTank.png")
surface = pygame.Surface([screen_width, screen_height])
tank_mask = pygame.mask.from_surface(tank_img)

# Akia, LabActivity1, I add this line for background music
mixer.music.load("Sounds/SoundTrack.mp3")
# Plays background music
mixer.music.play(-1)

# Tank properties
AkiaTank_width = 120
AkiaTank_height = 150
AkiaTank_x = (screen_width - AkiaTank_width) // 2
AkiaTank_y = screen_height - AkiaTank_height

# Bullet properties
bullet_width = 10
bullet_height = 20
bullet_color = blue
bullet_speed = 20
bullets = []

# Enemy properties
enemy_width = 100
enemy_height = 60
enemy_color = red
enemy_speed = 2.5
enemies = []

# Load enemy tank image
enemy_tank_img = pygame.image.load("Images/enemy_tank.png")  # Make sure you have an enemy tank image
enemy_mask = pygame.mask.from_surface(enemy_tank_img)

#This is the setting button icon
settings_icon = pygame.image.load("Images/settings.png")
settings_icon = pygame.transform.scale(settings_icon, (75, 75))

menu_open = False
show_instructions = False
font_small = pygame.font.Font(None, 30)

# Game loop
game_over = False  # Initialize game over state
blinking = False
blink_start_time = 0
fade_to_black = False
fade_start_time = 0
running = True  # The game will continue to run unless running = False
score = 0  # Initialize the score. Try fixing this.
render_text = True
game_over_sound_played = False


def draw_menu():
    menu_width, menu_height = 250, 200
    menu_x, menu_y = screen_width - menu_width - 20, 60
    # background box
    pygame.draw.rect(screen, (230, 230, 230), (menu_x, menu_y, menu_width, menu_height))
    # border
    pygame.draw.rect(screen, black, (menu_x, menu_y, menu_width, menu_height), 3)

    restart_text = font_small.render("Restart Game", True, black)
    exit_text = font_small.render("Exit Game", True, black)
    instruct_text = font_small.render("Instructions", True, black)

    screen.blit(restart_text, (menu_x + 20, menu_y + 30))
    screen.blit(instruct_text, (menu_x + 20, menu_y + 80))
    screen.blit(exit_text, (menu_x + 20, menu_y + 130))

    # return rects so we can test clicks
    return {
        "restart": pygame.Rect(menu_x + 15, menu_y + 25, 200, 40),
        "instructions": pygame.Rect(menu_x + 15, menu_y + 75, 200, 40),
        "exit": pygame.Rect(menu_x + 15, menu_y + 125, 200, 40)
    }

def draw_instructions():
    instruct_surface = pygame.Surface((screen_width - 100, screen_height - 200))
    instruct_surface.fill((245, 245, 245))
    pygame.draw.rect(instruct_surface, black, instruct_surface.get_rect(), 3)

    lines = [
        "🎮 HOW TO PLAY 🎮",
        "",
        "LEFT/RIGHT - Move Left / Right",
        "UP/DOWN - Move Up / Down",
        "SPACE - Shoot",
        "",
        "💥 You get +1 for every enemy destroyed.",
        "",
        "Press R to restart after Game Over.",
        "",
        "Click anywhere to go back."
    ]

    y_offset = 30
    for line in lines:
        text = font_small.render(line, True, black)
        instruct_surface.blit(text, (30, y_offset))
        y_offset += 40

    screen.blit(instruct_surface, (50, 100))

while running:
    settings_rect = settings_icon.get_rect(topright=(screen_width - border_margin, border_margin))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # If neither menu nor instructions are open, allow opening menu by clicking icon
            if not menu_open and not show_instructions:
                if settings_rect.collidepoint(mouse_pos):
                    menu_open = True

            # If the menu is open, check which menu item was clicked
            elif menu_open:
                buttons = draw_menu()  # draw_menu also returns the clickable rects
                if buttons["restart"].collidepoint(mouse_pos):
                    # Reset game variables (Restart)
                    render_text = True
                    mixer.music.play(-1)
                    game_over = False
                    fade_to_black = False
                    blinking = False
                    AkiaTank_x = (screen_width - AkiaTank_width) // 2
                    AkiaTank_y = screen_height - AkiaTank_height
                    score = 0
                    bullets.clear()
                    enemies.clear()
                    menu_open = False
                elif buttons["exit"].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif buttons["instructions"].collidepoint(mouse_pos):
                    show_instructions = True
                    menu_open = False

            # If instructions are showing, any click closes them
            elif show_instructions:
                show_instructions = False

            # handle keyboard (space only fires when not game_over) ---
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Akia, LabActivity1, I add this line for bullet sounds
                bullet_Sound = mixer.Sound("Sounds/ShotsFired.mp3")
                bullet_Sound.set_volume(2.0)
                bullet_Sound.play()
                bullets.append([AkiaTank_x + AkiaTank_width // 2, AkiaTank_y])

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # You still have R to restart after Game Over if desired
            if event.key == pygame.K_r and game_over:
                render_text = True
                mixer.music.play(-1)
                game_over = False
                AkiaTank_x = (screen_width - AkiaTank_width) // 2
                AkiaTank_y = screen_height - AkiaTank_height
                score = 0
                bullets.clear()
                enemies.clear()

    #User Tank movement
    tank_movement = 7
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and AkiaTank_x > border_margin:
        AkiaTank_x -= tank_movement
    if keys[pygame.K_RIGHT] and AkiaTank_x < screen_width - AkiaTank_width - border_margin:
        AkiaTank_x += tank_movement

    # Freely control the tank in up and down manner
    if keys[pygame.K_UP] and AkiaTank_y > border_margin:
        AkiaTank_y -= tank_movement
    if keys[pygame.K_DOWN] and AkiaTank_y < screen_height - AkiaTank_height - border_margin:
        AkiaTank_y += tank_movement

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Spawn enemies only when the game is active
    if not game_over and not blinking and not fade_to_black:
        # Spawn additional enemies
        min_enemies = 2  # Adjust the minimum number of enemies you want
        max_enemies = 4  # Adjust the maximum number of enemies you want

        # Determine how many new enemies to add
        enemies_to_add = min(max_enemies - len(enemies), 1)  # Add 1 enemy at a time

        # Add the specified number of new enemies
        for _ in range(enemies_to_add):
            enemies.append([random.randint(border_margin, screen_width - enemy_width - border_margin), border_margin])

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_tank_img, (enemy[0], enemy[1]))

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_speed

    # Collision detection
    bullets_to_remove = []
    enemies_to_remove = []

    for bullet in bullets:
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            if bullet_rect.colliderect(enemy_rect):

                # Akia, LabActivity1, I add this line for collision sounds
                enemy_Kill = mixer.Sound("Sounds/EnemyKill.mp3")
                enemy_Kill.set_volume(0.2)
                enemy_Kill.play()

                bullets_to_remove.append(bullet)
                enemies_to_remove.append(enemy)

                score += 1  # Increase the score when an enemy is hit

    # Remove bullets that hit enemies
    for bullet in bullets_to_remove:
        bullets.remove(bullet)
    # Remove enemies that were hit by bullets
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    # Clear the screen
    screen.fill(white)
    screen.blit(battle_field, (0, 0))

    # Draw the score
    # Akia, LabActivity1, moved this entire function outside to be displayed
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Final Score: {score}", True, black)
    if render_text:
        screen.blit(score_text, (border_margin, border_margin))  # Display the score at (20, 20)

    # Collision detection between tank and enemies
    tank_rect = pygame.Rect(AkiaTank_x, AkiaTank_y, AkiaTank_width, AkiaTank_height)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)

        offset_x = enemy_rect.x - tank_rect.x
        offset_y = enemy_rect.y - tank_rect.y

        if tank_mask.overlap(enemy_mask,(offset_x, offset_y)) and not game_over:
            mixer.music.stop()
            # Akia, LabActivity1, add a game over sound fxs
            game_over = True  # Game over if collision detected
            blinking = True
            blink_start_time = pygame.time.get_ticks()



    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_tank_img, (enemy[0], enemy[1]))

    # Draw the tank
    if blinking:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - blink_start_time

        if elapsed < 1000:
            # Every 100ms toggle visibility
            if (elapsed // 100) % 2 == 0:
                screen.blit(tank_img, (AkiaTank_x, AkiaTank_y))

        else:
            blinking = False
            enemies.clear()
            fade_to_black = True
            fade_start_time = pygame.time.get_ticks()

            if not game_over_sound_played:
                lose = mixer.Sound("Sounds/GameOver.mp3")
                lose.play()
                game_over_sound_played = True

    else:
        if not game_over:
            screen.blit(tank_img, (AkiaTank_x, AkiaTank_y))

    # Hover effect: slightly brighten settings icon when mouse is over it
    mouse_pos_now = pygame.mouse.get_pos()
    if settings_rect.collidepoint(mouse_pos_now):
        # draw the icon then a transparent surf to simulate hover
        screen.blit(settings_icon, settings_rect)
        bright_icon = pygame.Surface(settings_icon.get_size(), pygame.SRCALPHA)
        bright_icon.fill((255, 255, 255, 80))  # light overlay
        screen.blit(bright_icon, settings_rect)
    else:
        screen.blit(settings_icon, settings_rect)

    if menu_open:
        draw_menu()

    if show_instructions:
        draw_instructions()

    # Handle fade to black and game over text
    if fade_to_black:
        elapsed_fade = pygame.time.get_ticks() - fade_start_time
        fade_duration = 1500  # 1.5 seconds fade

        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill(black)

        alpha = min(255, int((elapsed_fade / fade_duration) * 255))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))

        if elapsed_fade >= fade_duration:
            # Once fade is done, show Game Over text
            game_over_text = font.render("Game Over! Press R to Restart", True, red)
            quit_text = font.render("Press ESC to Quit", True, red)
            scoreCounter = font.render(f"Score: " + str(score), True, red)

            screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2,
                                         (screen_height - game_over_text.get_height()) // 2.5))
            screen.blit(scoreCounter, ((screen_width - scoreCounter.get_width()) // 2,
                                       (screen_height - scoreCounter.get_height()) // 2))
            screen.blit(quit_text, ((screen_width - quit_text.get_width()) // 2,
                                    (screen_height - quit_text.get_height()) // 1.8))

            # Update the display
    pygame.display.update()


    # Control the frame rate
    pygame.time.delay(30)

    # Check for restart input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        # Reset game variables
        render_text = True
        mixer.music.play(-1)

        game_over = False
        fade_to_black = False
        blinking = False
        game_over_sound_played = False
        AkiaTank_x = (screen_width - AkiaTank_width) // 2
        AkiaTank_y = screen_height - AkiaTank_height
        score = 0  # Turns the score counter into 0
        bullets.clear()
        enemies.clear()


# Quit Pygame
pygame.quit()
sys.exit()
