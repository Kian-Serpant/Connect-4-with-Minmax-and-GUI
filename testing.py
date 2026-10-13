# RUNNING IN PYTHON 3.12, but for some reason it's called python 3.10 :(

for val in range(1,4):
    print(val)


import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 # time interval for events


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) # creates a 2D vector

# game loop - makes it run until window is closed
while running:
    # poll for event
    # pygame.QUIT event means that the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a colour to wipe away anything from last frame
    screen.fill("purple")

    # RENDER game here:
    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]: # checks if the key "w" is pressed - K_ followed by a thing means the key it checks for
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt



    # flip() the display to put your work on screen
    pygame.display.flip()
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()