import pygame, sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption("2D Water Ripple")
clock = pygame.time.Clock()

black_color = (0, 0, 0)
white_color = (255, 255, 255)
grey_color = (25, 25, 25)
red_color = (255, 100, 100)
teal_color = (100, 255, 255)
green_color = (100, 255, 100)
default_color = white_color

FPS = 60
surface_scale = 4
surface_w, surface_h = 128, 128
window_w, window_h = surface_w * surface_scale, surface_h * surface_scale
surface = pygame.Surface((surface_w, surface_h))
window = pygame.display.set_mode((window_w, window_h))

damping = 0.95
threshold = 0.01

currentBuffer = [[ 0 for i in range(surface_w)] for j in range(surface_h)]
previousBuffer = [[ 0 for i in range(surface_w)] for j in range(surface_h)]
#it = 0

def update_game():
    global currentBuffer, previousBuffer

    for row in range(1, len(previousBuffer) - 1):
        for col in range(1, len(previousBuffer[row]) - 1):

                currentBuffer[col][row] = (
                                            previousBuffer[col - 1][row] +
                                            previousBuffer[col + 1][row] +
                                            previousBuffer[col][row - 1] +
                                            previousBuffer[col][row + 1] ) / 2 - currentBuffer[col][row]

                currentBuffer[col][row] = currentBuffer[col][row] * damping

    temp = previousBuffer
    previousBuffer = currentBuffer
    currentBuffer = temp

    #global it    
    #pygame.image.save(window,"gif/" +  str(it) + "_iteration.jpeg")
    #it += 1
    
                
def pixel(surface, pos, color):
    try:
        surface.set_at(pos, color)
    except:
        pass


def draw_game():
    for row in range(len(currentBuffer)):
        for col in range(len(currentBuffer[row])):

            height = currentBuffer[col][row]
            if height < threshold: height = 0

            color1 = abs(int(default_color[0] * height))
            color2 = abs(int(default_color[1] * height))
            color3 = abs(int(default_color[2] * height))

            pixel(surface, (col, row), (color1, color2, color3))


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if pygame.mouse.get_pressed()[0]:

            pos = (int(pygame.mouse.get_pos()[0]/surface_scale), 
                   int(pygame.mouse.get_pos()[1]/surface_scale))

            # ripple seed 
            # with shape:
            #
            #    ###
            #   #####
            #   #####
            #   #####
            #    ###
            #
            
            try:

                previousBuffer[pos[0]][pos[1]] = 1
                previousBuffer[pos[0] + 1][pos[1]] = 1
                previousBuffer[pos[0] - 1][pos[1]] = 1

                previousBuffer[pos[0]][pos[1] + 1] = 1
                previousBuffer[pos[0]][pos[1] - 1] = 1
                previousBuffer[pos[0] - 1][pos[1] - 1] = 1

                previousBuffer[pos[0] + 1][pos[1] - 1] = 1
                previousBuffer[pos[0] - 1][pos[1] + 1] = 1
                previousBuffer[pos[0] + 1][pos[1] + 1] = 1

                previousBuffer[pos[0]][pos[1] - 2] = 1
                previousBuffer[pos[0] + 1][pos[1] - 2] = 1
                previousBuffer[pos[0] - 1][pos[1] - 2] = 1

                previousBuffer[pos[0]][pos[1] + 2] = 1
                previousBuffer[pos[0] + 1][pos[1] + 2] = 1
                previousBuffer[pos[0] - 1][pos[1] + 2] = 1

                previousBuffer[pos[0] + 2][pos[1] - 1] = 1
                previousBuffer[pos[0] + 2][pos[1]] = 1
                previousBuffer[pos[0] + 2][pos[1] + 1] = 1

                previousBuffer[pos[0] - 2][pos[1] - 1] = 1
                previousBuffer[pos[0] - 2][pos[1]] = 1
                previousBuffer[pos[0] - 2][pos[1] + 1] = 1
                
            except:
                pass

    update_game()
    draw_game()

    window.blit(pygame.transform.scale(surface, window.get_rect().size), (0, 0))
    pygame.display.update()
    clock.tick(FPS)