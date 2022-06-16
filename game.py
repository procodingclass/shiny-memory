import pygame
import ctypes

screen_width = 700
screen_height = 400

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))

def create_screen():
    global screen
    return screen

def loadImages(images_path):
    image_list = []

    for path in images_path:
        loaded_image = pygame.image.load(path).convert_alpha()
        image_list.append(loaded_image)
    return image_list

def scaleImages(image_list, width, height):
    scaled_images = []
    if(len(image_list) == 1):
        return pygame.transform.scale(image_list[0], (width, height))

    for img in image_list:
        image = pygame.transform.scale(img, (width, height))
        scaled_images.append(image)

    return scaled_images

#Images
color_surf = loadImages(["assets/color_bg.jpg"])
background_surf = loadImages(["assets/environment.png"])
background_surf[0].set_alpha(100)

ground_surf = loadImages(["assets/ground.png"])
door_surf = loadImages(["assets/doorOpen.png"])
win_surf = loadImages(["assets/win.png"])
game_over_surf = loadImages(["assets/gameOver.png"])
spikes_surf = loadImages(["assets/spikes.png"])
platform_surf = loadImages(["assets/platform.png"])

#player_surf = loadImages(["assets/joe1.png"])
cloud_surf = loadImages(["assets/cloud.png"])
cloud_surf[0].set_alpha(200)

doorHeight=100
doorWidth=100

#Image Scaling
background_surf = scaleImages(background_surf, screen_width, 500)

color_surf = scaleImages(color_surf, screen_width, screen_height)
door_surf= scaleImages(door_surf, 100,100)
cloud_surf = scaleImages(cloud_surf, 100, 50)
game_over_surf = scaleImages(game_over_surf, 230, 150)
#player_surf = scaleImages(player_surf, 40, 63)
ground_surf = scaleImages(ground_surf, screen_width, 90)
spikes_surf = scaleImages(spikes_surf, 100, 20)



# sprites
#player_rect = pygame.Rect(620,screen_height-145,40,63)
ground_rect = pygame.Rect(0,screen_height- 88,screen_width,40)
door_rect = pygame.Rect(screen_width-130, screen_height-190, 100,100)
spikes_rect1 = pygame.Rect(230, screen_height - 110 ,100,20)
spikes_rect2 = pygame.Rect(330, screen_height - 110 ,100,20)





cloud1X = 50
cloud2X = 300
cloud3X = 550



def draw_arena():
    global color_surf, background_surf
    global ground_surf, door_surf, win_surf
    global cloud_surf, ground_rect, door_rect
    global spikes_surf, spikes_rect1, spikes_rect2
    global cloud1X, cloud2X, cloud3X
    global screen

    screen.blit(color_surf, (0, 0))
    screen.blit(background_surf, (0, -150))
    screen.blit(ground_surf, (0, screen_height-90))
    screen.blit(door_surf,door_rect)
    screen.blit(spikes_surf,spikes_rect1)
    screen.blit(spikes_surf,spikes_rect2)



    screen.blit(cloud_surf, (cloud1X, 30))
    if cloud1X < -100:
        cloud1X = screen_width
    else:
        cloud1X -= 2

    screen.blit(cloud_surf, (cloud2X, 33))
    if cloud2X < -50:
        cloud2X = screen_width
    else:
        cloud2X -= 1

    screen.blit(cloud_surf, (cloud3X, 20))
    if cloud3X < 0:
        cloud3X = screen_width
    else:
        cloud3X -= 2


    clock.tick(30)

def check_collision(static_rect, moving_rect, vel_x, vel_y):
    # x- direction
    moving_rect_props = (moving_rect.x + vel_x, moving_rect.y, moving_rect.width, moving_rect.height)
    if static_rect.colliderect(moving_rect_props):
            vel_x = 0

            #check for collision in y direction
            moving_rect_props = (moving_rect.x, moving_rect.y + vel_y, moving_rect.width, moving_rect.height)
            if static_rect.colliderect(moving_rect_props):
                #check if below the platform i.e. jumping
                if(vel_y < 0):
                    vel_y = static_rect.bottom - moving_rect.top
                elif(vel_y > 0): #check if above the platform i.e. falling
                    vel_y = static_rect.top - moving_rect.bottom

    # make player to stand on platform
    # y- direction
    static_rect_props = (static_rect.x, static_rect.y - vel_y, static_rect.width, static_rect.height)
    if(moving_rect.colliderect(static_rect_props)):
        vel_y = 0
    return vel_x, vel_y




def gameplay():
    global door_surf, win_surf, game_over_surf, door_rect
    global ground_rect, screen, spikes_rect1, spikes_rect2

    draw_arena()
    try:
        import main

        if(main.player_rect != None and main.player_surf != None):

            # collision with left wall
            if(main.player_rect.x < 0):
                main.player_rect.x = 0

            if(main.player_rect.x >= door_rect.centerx):
                screen.blit(win_surf[0],(screen_width / 2 - 140,100))
                main.player_vel_x = 0
                main.player_vel_y = 0

                img_width = int(main.player_surf.get_width() * 0.99)
                img_height = int(main.player_surf.get_height() * 0.99)

                main.player_surf = scaleImages([main.player_surf], img_width,img_height)


            if(main.player_rect.colliderect(spikes_rect1)):
                screen.blit(game_over_surf,(screen_width / 2 - 120,100))
                main.player_vel_x = 0
                main.player_vel_y = 0

            if(main.player_rect.colliderect(spikes_rect2)):
                screen.blit(game_over_surf,(screen_width / 2 - 120,100))
                main.player_vel_x = 0
                main.player_vel_y = 0

            # checking ground collision
            main.player_vel_x, main.player_vel_y = check_collision(ground_rect, main.player_rect, main.player_vel_x, main.player_vel_y)

    except:
        pass
