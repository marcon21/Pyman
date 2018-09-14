import pygame, sys
from pygame.locals import *
import random
from PIL import Image

def create_map(map_image, dictionary, block_size, width):
    """Function that, given a pixeled image of a map, a dictionary with various
    color for the relative blocks, their image and other information, the size
    of the block and the width of the monitor return a map the dimension of the
    map_image moltiplied by the block_size
    """
    image_map = Image.open(map_image)

    map_raw = list(image_map.getdata()) #getting data(color) from the image
    map = []
    x = 0
    y = 0

    for element in map_raw: #the image of the block
        surface_sprite = pygame.transform.scale(
            pygame.image.load(dictionary[element][0]),
            (block_size, block_size))

        #creating the block according to the dictionary
        block = Block(surface_sprite, x, y, dictionary[element][1])
        map.append(block)
        x += block_size
        if x == width:
            x = 0
            y += block_size
    return map

def draw_map(map_array, map_image, window): #draw the map on the screen
    map_image = pygame.image.load(map_image)
    pygame.Surface.blit(window, map_image, (0, 0))
    for block in map_array:
        block.draw(window, block.rect.x, block.rect.y)
    return


class Block(pygame.sprite.Sprite):
    """The class of the blocks in the map"""
    def __init__(self, image, x, y, wall):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wall = wall # boolean value

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
