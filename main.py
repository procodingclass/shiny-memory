import pygame, sys, random
from game import create_screen, screen_height, gameplay


screen = create_screen()
# Load image frames
player_surf = pygame.image.load("assets/joe/0.png").convert_alpha()

# scale image frames
player_surf = pygame.transform.scale(player_surf, (30, 43))

player_rect = pygame.Rect(110, screen_height - 135 ,30,43) # x, y, width, height

player_vel_x = 0
player_vel_y = 0

def key_down(event):
    global player_vel_x, player_vel_y

    if(event.type == pygame.KEYDOWN):
        if(event.key == pygame.K_RIGHT):
            player_vel_x = 5
        elif(event.key == pygame.K_LEFT):
            player_vel_x = -5
        elif(event.key == pygame.K_DOWN):
            player_vel_y = 5
        elif(event.key == pygame.K_SPACE):
            player_vel_y = -15


def key_up(event):
    global player_vel_x, player_vel_y

    if(event.type == pygame.KEYUP):
        if(event.key == pygame.K_RIGHT):
            player_vel_x = 0
        elif(event.key == pygame.K_LEFT):
            player_vel_x = 0
        elif(event.key == pygame.K_DOWN):
            player_vel_y = 0
        elif(event.key == pygame.K_SPACE):
            player_vel_y = 0

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        key_down(event)
        key_up(event)



    gameplay()

    screen.blit(player_surf,player_rect)

    # updating x and y co-ordinate
    player_rect.x += player_vel_x
    player_rect.y += player_vel_y

    pygame.display.update()
